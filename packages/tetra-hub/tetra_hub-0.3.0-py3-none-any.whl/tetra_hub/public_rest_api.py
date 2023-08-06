from __future__ import annotations
import datetime
import os
import json
import threading
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin
import posixpath
import requests
import configparser
from tqdm import tqdm
from contextlib import nullcontext
from dataclasses import dataclass
from types import SimpleNamespace
from typing import List
import numpy as np
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from . import public_api_pb2 as api_pb
from . import api_status_codes
from pathlib import Path
from collections import OrderedDict

UNKNOWN_ERROR = "Unknown error."
API_VERSION = "v1"

# Used for error message feedback
CASUAL_CLASSNAMES = {
    api_pb.ProfileJob: "job",
    api_pb.Model: "model",
    api_pb.User: "user",
}

DEFAULT_CONFIG_PATH = "~/.tetra/client.ini"

Shapes = Union[
    List[Tuple[int, ...]],
    "OrderedDict[str, Tuple[int, ...]]",
    List[Tuple[str, Tuple[int, ...]]],
    Dict[str, Tuple[int, ...]],
]

DatasetEntries = Union[
    "OrderedDict[str, List[np.ndarray]]",
    "OrderedDict[str, np.ndarray]",
    Dict[str, List[np.ndarray]],
    Dict[str, np.ndarray],
]


def get_config_path(expanduser=True):
    path = os.environ.get("TETRA_CLIENT_INI", DEFAULT_CONFIG_PATH)
    if expanduser:
        path = os.path.expanduser(path)
    return path


@dataclass
class ClientConfig:
    """
    Configuration information, such as your API token, for use with
    :py:class:`.Client`.

    Parameters
    ----------
    api_url
        URL of the API backend endpoint.
    web_url
        URL of the web interface.
    api_token
        API token. Available through the web interface under the "Account" page.
    """

    api_url: str
    web_url: str
    api_token: str


class APIException(Exception):
    """
    Excpetion for the python REST API.

    Parameters
    ----------
    message : str
        Message of the failure. If None, sets it automatically based on
        `status_code`.
    status_code : int
        API status code (a superset of HTTP status codes).
    """

    def __init__(self, message=None, status_code=None):
        if message is None:
            if status_code is not None:
                # Some common error codes have custom messages
                if status_code == api_status_codes.HTTP_401_UNAUTHORIZED:
                    message = "API authentication failure; please check your API token."
                elif status_code == api_status_codes.HTTP_429_TOO_MANY_REQUESTS:
                    message = "Too Many Requests: please slow down and try again soon."
                elif status_code == api_status_codes.API_CONFIGURATION_MISSING_FIELDS:
                    config_path = get_config_path(expanduser=False)
                    message = f"Required fields are missing from your {config_path}."
                elif status_code == api_status_codes.HTTP_413_REQUEST_ENTITY_TOO_LARGE:
                    message = "The uploaded asset is too large. Please contact us for workarounds."
                else:
                    message = f"API request returned status code {status_code}."
            else:
                message = UNKNOWN_ERROR

        super().__init__(message)
        self.status_code = status_code


def _response_as_protobuf(
    response: requests.Response, protobuf_class: Any, obj_id: Optional[int] = None
) -> Any:
    if (
        api_status_codes.is_success(response.status_code)
        and response.headers.get("Content-Type") == "application/x-protobuf"
    ):
        pb = protobuf_class()
        pb.ParseFromString(response.content)
        return pb
    elif (
        response.status_code == api_status_codes.HTTP_404_NOT_FOUND
        and obj_id is not None
    ):
        prefix = ""
        class_name = CASUAL_CLASSNAMES.get(protobuf_class)
        if class_name is not None:
            prefix = class_name.capitalize() + " "

        raise APIException(
            f"{prefix}ID {obj_id} could not be found. It may not exist or you may not have permission to view it.",
            status_code=response.status_code,
        )
    else:
        raise APIException(status_code=response.status_code)


def _prepare_offset_limit_query(offset: int, limit: int | None) -> str:
    extras = []
    if offset > 0:
        extras.append(f"offset={offset}")
    if limit is not None:
        extras.append(f"limit={limit}")
    if extras:
        return "?" + "&".join(extras)
    else:
        return ""


def _load_default_api_config(verbose=False) -> ClientConfig:
    """
    Load a default ClientConfig from default locations.

    Parameters
    ----------
    verbose : bool
        Print where config file is loaded from.

    Returns
    -------
    config : ClientConfig
        API authentication configuration.
    """
    # Load from default config path
    config = configparser.ConfigParser()
    # Client config should be in ~/.tetra/client.ini
    tilde_config_path = get_config_path(expanduser=False)
    config_path = os.path.expanduser(tilde_config_path)
    if verbose:
        print(f"Loading Client config from {tilde_config_path} ...")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"{tilde_config_path} not found. Please go to the Account page to "
            "find instructions of how to install your API key."
        )
    config.read([config_path])
    try:
        client_config = config["api"]

        api_config = ClientConfig(
            api_url=client_config["api_url"],
            web_url=client_config["web_url"],
            api_token=client_config["api_token"],
        )
    except KeyError:
        raise APIException(
            status_code=api_status_codes.API_CONFIGURATION_MISSING_FIELDS
        )
    return api_config


def _auth_header(
    content_type: str = "application/x-protobuf", config: Optional[ClientConfig] = None
) -> dict:
    if config is None:
        config = _load_default_api_config()
    header = {
        "Authorization": f"token {config.api_token}",
        "Content-Type": content_type,
    }
    return header


def _api_url(*rel_paths, config: Optional[ClientConfig] = None) -> str:
    if config is None:
        config = _load_default_api_config()
    return urljoin(config.api_url, posixpath.join("api", API_VERSION, *rel_paths, ""))


def _get_token(api_url, email, password):
    url = urljoin(
        api_url, posixpath.join("api", API_VERSION, "users", "auth", "login", "")
    )
    data = {"email": email, "password": password}
    header = {"Content-Type": "application/json"}
    response = requests.post(url, headers=header, data=json.dumps(data))
    if api_status_codes.is_success(response.status_code):
        return json.loads(response.content)["key"]
    elif response.status_code == 400:
        raise ValueError("Failed to log in: Wrong Username / Password")
    else:
        raise APIException(status_code=response.status_code)


def _create_named_tensor(name: str, shape: Tuple[int, ...]) -> api_pb.NamedTensorType:
    tensor_type_list = []
    for i in shape:
        tensor_type_list.append(i)
    tensor_type_pb = api_pb.TensorType(
        shape=tensor_type_list, dtype=api_pb.TensorDtype.TENSOR_DTYPE_FLOAT32
    )
    return api_pb.NamedTensorType(name=name, tensor_type=tensor_type_pb)


def _list_shapes_to_tensor_type_list_pb(
    input_shapes: Shapes,
) -> api_pb.NamedTensorTypeList:

    tensor_type_pb_list = []

    if isinstance(input_shapes, dict):
        input_shapes = OrderedDict(sorted(input_shapes.items()))
        if isinstance(input_shapes, OrderedDict):
            for name, shape in input_shapes.items():
                named_tensor_type_pb = _create_named_tensor(name, shape)
                tensor_type_pb_list.append(named_tensor_type_pb)
    if isinstance(input_shapes, list):
        if isinstance(input_shapes[0][0], int):
            for index, shape in enumerate(input_shapes):
                named_tensor_type_pb = _create_named_tensor(
                    f"input_{index+1}", shape  # type: ignore
                )
                tensor_type_pb_list.append(named_tensor_type_pb)
        else:
            for name_and_shape in input_shapes:
                name, shape = name_and_shape
                named_tensor_type_pb = _create_named_tensor(name, shape)  # type: ignore
                tensor_type_pb_list.append(named_tensor_type_pb)

    return api_pb.NamedTensorTypeList(types=tensor_type_pb_list)


def _tensor_type_list_pb_to_list_shapes(
    tensor_type_list_pb: api_pb.NamedTensorTypeList,
) -> List[Tuple[str, Tuple[int, ...]]]:
    shapes_list = []
    for named_tensor_type in tensor_type_list_pb.types:
        shape = []
        for d in named_tensor_type.tensor_type.shape:
            shape.append(d)
        shapes_list.append((named_tensor_type.name, tuple(shape)))
    return shapes_list


_get_unique_path_lock = threading.Lock()


def _get_unique_path(dst_path):
    name, ext = os.path.splitext(dst_path)

    _get_unique_path_lock.acquire()
    if os.path.exists(dst_path):
        now = str(datetime.datetime.now().time()).replace(":", ".")
        dst_path = f"{name}_{now}{ext}"

    # Write empty file (to be overwritten later), for thread safety.
    open(dst_path, "a").close()

    _get_unique_path_lock.release()

    name = os.path.basename(dst_path)

    return dst_path, name


def _convert_inputs_to_tensor_type_list_pb(
    inputs: OrderedDict[str, List["np.ndarray"]]
) -> api_pb.NamedTensorTypeList:
    tensor_type_pb_list = []
    for name, tensor in inputs.items():
        named_tensor_type_pb = _create_named_tensor(name, tensor[0].shape)
        tensor_type_pb_list.append(named_tensor_type_pb)
    return api_pb.NamedTensorTypeList(types=tensor_type_pb_list)


def _do_input_shapes_match(
    input_shapes: Shapes,
    tensor_type_list: api_pb.NamedTensorTypeList,
):
    inputs_tensor_type_list = _tensor_type_list_pb_to_list_shapes(tensor_type_list)
    inputs_shapes_tensor_type_list = _tensor_type_list_pb_to_list_shapes(
        _list_shapes_to_tensor_type_list_pb(input_shapes)
    )

    input_names_match = [False] * len(inputs_tensor_type_list)
    for i, (input_name, input_tensor_shape) in enumerate(inputs_tensor_type_list):
        for _, (input_shape_name, input_shape) in enumerate(
            inputs_shapes_tensor_type_list
        ):
            if input_name == input_shape_name:
                input_names_match[i] = True
                if input_tensor_shape != input_shape:
                    return False
    return all(input_names_match)


def _download_file(url: str, filename: str, dst_path: str, verbose: bool) -> str:
    dst_path = os.path.expanduser(dst_path)  # Expand ~ to user home in path.

    # If no filename is provided, use the filename given to us by the parent
    if os.path.isdir(dst_path):
        dst_path = os.path.join(dst_path, filename)

        # Append suffix if dst file exists.
        dst_path, filename = _get_unique_path(dst_path)

    # Verify dst parent dir exists. The same error thrown by open() called
    # below would include the model name, which is confusing.
    parent_dir = os.path.dirname(dst_path)
    if parent_dir and not os.path.exists(parent_dir):
        raise ValueError(f"Download directory '{parent_dir}' does not exist.")

    response = requests.get(url, stream=True)
    if api_status_codes.is_success(response.status_code):
        file_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        if verbose:
            tqdm_context = tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=block_size,
                colour="magenta",
                desc=filename,
            )
        else:
            tqdm_context = nullcontext()

        with tqdm_context as progress_bar:
            with open(dst_path, "wb") as fd:
                for data in response.iter_content(block_size):
                    written_data = fd.write(data)
                    if progress_bar:
                        progress_bar.update(written_data)
    else:
        raise APIException(status_code=response.status_code)

    return dst_path


# These helper functions are placed in a utils namespace
# so as not to confuse with core API functions
utils = SimpleNamespace(
    response_as_protobuf=_response_as_protobuf,
    prepare_offset_limit_query=_prepare_offset_limit_query,
    load_default_api_config=_load_default_api_config,
    auth_header=_auth_header,
    api_url=_api_url,
    list_shapes_to_tensor_type_list_pb=_list_shapes_to_tensor_type_list_pb,
    tensor_type_list_pb_to_list_shapes=_tensor_type_list_pb_to_list_shapes,
    get_unique_path=_get_unique_path,
    download_file=_download_file,
    convert_inputs_to_tensor_type_list_pb=_convert_inputs_to_tensor_type_list_pb,
    do_input_shapes_match=_do_input_shapes_match,
)


def get_auth_user(config: Optional[ClientConfig] = None) -> api_pb.User:
    """
    Get authenticated user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    user_pb : User
        Get authenticated user information.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("users", "auth", "user", config=config)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    # Note, the API returns a JSON right now, but we will translate this to a
    # protobuf
    content = json.loads(response.content)
    if api_status_codes.is_success(response.status_code):
        user_pb = api_pb.User(
            id=content["pk"],
            first_name=content.get("first_name", ""),
            last_name=content.get("last_name", ""),
            email=content["email"],
        )
        return user_pb
    else:
        raise APIException(status_code=response.status_code)


def get_user(user_id: int, config: Optional[ClientConfig] = None) -> api_pb.User:
    """
    Get user information.

    Parameters
    ----------
    user_id : int
        User ID.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    user_pb : User
       User information as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("users", str(user_id), config=config)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.User, obj_id=user_id)


def get_user_list(
    offset: int = 0, limit: int | None = None, config: Optional[ClientConfig] = None
) -> api_pb.UserList:
    """
    Get user information.

    Parameters
    ----------
    offset : int
        Offset the query.
    limit : int
        Limit query response size.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    user_list_pb : UserList
       User list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("users", config=config)
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.UserList)


def get_device_list(
    name: str = "",
    os: str = "",
    attributes: List[str] = [],
    select: bool = False,
    config: Optional[ClientConfig] = None,
) -> api_pb.DeviceList:
    """
    Get list of active devices.

    Parameters
    ----------
    name : str
        Only devices with this exact name will be returned.
    os : str
        Only devices with an OS version that is compatible with this os are returned
    attributes : List[str]
        Only devices that have all requested properties are returned.
    select: bool
        whether to return a list or a single device
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    device_list_pb : DeviceList
       Device list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("devices", config=config)
    url += f"?name={name}&os={os}&select={select}"
    for attr in attributes:
        url += f"&attributes={attr}"
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.DeviceList)


def create_profile_job(
    profile_job_pb: api_pb.ProfileJob, config: Optional[ClientConfig] = None
) -> api_pb.CreateUpdateResponse:
    """
    Create new profile job.

    Parameters
    ----------
    job_pb : ProfileJob
        Protobuf object with new profile job.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("jobs", config=config)
    header = utils.auth_header(config=config)
    job_pb = api_pb.Job(profile_job=profile_job_pb)
    response = requests.post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    return utils.response_as_protobuf(response, api_pb.CreateUpdateResponse)


def create_validation_job(
    validation_job_pb: api_pb.ValidationJob, config: Optional[ClientConfig] = None
) -> api_pb.CreateUpdateResponse:
    """
    Create new validation job.

    Parameters
    ----------
    job_pb : ValidationJob
        Protobuf object containing properties for the new validation job
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("jobs", config=config)
    header = utils.auth_header(config=config)
    job_pb = api_pb.Job(validation_job=validation_job_pb)
    response = requests.post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    return utils.response_as_protobuf(response, api_pb.CreateUpdateResponse)


def get_job(job_id: str, config: Optional[ClientConfig] = None) -> api_pb.Job:
    """
    Get job information.

    Parameters
    ----------
    job_id : str
        Job ID.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    job_pb : ProfileJob
        Profile job as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("jobs", str(job_id), config=config)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Job, obj_id=job_id)


def get_job_list(
    offset: int = 0,
    limit: int | None = None,
    config: Optional[ClientConfig] = None,
    states: List["api_pb.JobState.ValueType"] = [],
) -> api_pb.JobList:
    """
    Get list of jobs visible to the authenticated user.

    Parameters
    ----------
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    list_pb : JobList
        List of jobs as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("jobs", config=config)

    # TODO: better API for joining optional query strings.
    offset_limit_query = utils.prepare_offset_limit_query(offset, limit)
    states_query = f"state={','.join([str(x) for x in states])}" if states else ""
    if states_query:
        if offset_limit_query:
            states_query = "&" + states_query
        else:
            states_query = "?" + states_query
    url += offset_limit_query + states_query

    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.JobList)


def get_job_results(
    job_id: str, config: Optional[ClientConfig] = None
) -> api_pb.JobResult:
    """
    Get job results, if available.

    Parameters
    ----------
    job_id : int
        Job ID as integer.
    config : ClientConfig
        API authentication configuration.

    Results
    -------
    res_pb : ProfileJobResult
        Result is returned as a protobuf object. Or None if results are not available.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    header = utils.auth_header(config=config)
    url = utils.api_url("jobs", str(job_id), "result", config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.JobResult, obj_id=job_id)


# Workaround for mypy having trouble with globals https://github.com/python/mypy/issues/5732
last: int


def _upload_asset(
    endpoint: str,
    path: str | Path,
    name: Optional[str] = None,
    model_type: "api_pb.ModelType.ValueType" = api_pb.ModelType.MODEL_TYPE_UNSPECIFIED,
    verbose: bool = True,
    config: Optional[ClientConfig] = None,
) -> api_pb.CreateUpdateResponse:
    """
    Helper upload function for models, datasets, etc.
    """
    path = os.path.expanduser(path)  # Expand home directory prefix.

    if config is None:
        config = utils.load_default_api_config()

    try:
        total_size = os.path.getsize(path)
    except FileNotFoundError:
        raise

    global last
    last = 0
    if verbose:
        tqdm_context = tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            colour="magenta",
        )

        def update_progress(monitor):
            global last
            # Your callback function
            tqdm_context.update(monitor.bytes_read - last)
            last = monitor.bytes_read

    else:

        def update_progress(monitor):
            pass

    upload_url = utils.api_url(endpoint, config=config)

    with open(path, "rb") as asset_file:
        fields = {
            "data": ("filename", asset_file, "application/octet-stream"),
            "name": name or os.path.basename(path),
        }
        if endpoint == "models":
            fields["model_type"] = api_pb.ModelType.Name(model_type)
        mpe = MultipartEncoder(fields=fields)
        mpm = MultipartEncoderMonitor(mpe, update_progress)
        header = utils.auth_header(content_type=mpm.content_type, config=config)
        response = requests.post(upload_url, data=mpm, headers=header)

    update_progress(SimpleNamespace(bytes_read=total_size))

    response_pb = api_pb.CreateUpdateResponse()
    if api_status_codes.is_success(response.status_code):
        response_pb.ParseFromString(response.content)
        return response_pb
    elif response.headers["Content-Type"] == "application/json":
        if response.status_code == api_status_codes.HTTP_401_UNAUTHORIZED:
            # Use the default description for 401
            raise APIException(status_code=response.status_code)
        else:
            raise APIException(response.content, status_code=response.status_code)
    else:
        raise APIException("Unexpected HTTP content type on failure response.")


def upload_model(
    path: str | Path,
    name: Optional[str] = None,
    model_type: "api_pb.ModelType.ValueType" = api_pb.ModelType.MODEL_TYPE_UNSPECIFIED,
    verbose: bool = True,
    config: Optional[ClientConfig] = None,
) -> api_pb.CreateUpdateResponse:
    """
    Upload a model

    Parameters
    ----------
    path : str or Path
        Local path to the model file.
    name : str
        Name of the model. If None, uses basename of path.
    model_type : api_pb.ModelType
        Type of the model.
    verbose : bool
        If true, will show progress bar in standard output.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    return _upload_asset(
        endpoint="models",
        path=path,
        name=name,
        model_type=model_type,
        verbose=verbose,
        config=config,
    )


def upload_dataset(
    path: str | Path,
    name: Optional[str] = None,
    verbose: bool = True,
    config: Optional[ClientConfig] = None,
) -> api_pb.CreateUpdateResponse:
    """
    Upload data

    Parameters
    ----------
    path : str or Path
        Local path to the model file.
    name : str
        Name of the model. If None, uses basename of path.
    verbose : bool
        If true, will show progress bar in standard output.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    return _upload_asset(
        endpoint="datasets", path=path, name=name, verbose=verbose, config=config
    )


def get_dataset(
    dataset_id: int, config: Optional[ClientConfig] = None
) -> api_pb.Dataset:
    """
    Get info about an uploaded dataset.

    Parameters
    ----------
    dataset_id : int
        Dataset ID.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    dataset_pb : Dataset
        Dataset info as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("datasets", str(dataset_id), config=config)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Dataset, obj_id=dataset_id)


def get_dataset_list(
    offset: int = 0, limit: int | None = None, config: Optional[ClientConfig] = None
) -> api_pb.DatasetList:
    """
    Get list of datasets visible to the authenticated user.


    Parameters
    ----------
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    list_pb : DatasetList
        Dataset list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("datasets", config=config)
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.DatasetList)


def get_model(model_id: int, config: Optional[ClientConfig] = None) -> api_pb.Model:
    """
    Get info about an uploaded model.

    Parameters
    ----------
    model_id : int
        Model ID.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    model_pb : Model
        Model info as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("models", str(model_id), config=config)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Model, obj_id=model_id)


def get_model_list(
    offset: int = 0, limit: int | None = None, config: Optional[ClientConfig] = None
) -> api_pb.ModelList:
    """
    Get list of models visible to the authenticated user.


    Parameters
    ----------
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    list_pb : ModelList
        Model list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("models", config=config)
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config=config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.ModelList)


def download_model_info(
    model_id: str, config: Optional[ClientConfig] = None
) -> api_pb.FileDownloadURL:
    """
    Get download information for a previously uploaded model.

    Parameters
    ----------
    model_id : int
        Model ID.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    response : api_pb.FileDownloadURL
        Download information.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("models", str(model_id), "download", config=config)
    header = utils.auth_header(config=config)
    return utils.response_as_protobuf(
        requests.get(url, headers=header), api_pb.FileDownloadURL
    )


def download_model(
    model_id: str,
    file_path: str,
    verbose: bool = True,
    config: Optional[ClientConfig] = None,
) -> str:
    """
    Download a previously uploaded model.

    Parameters
    ----------
    model_id : int
        Model ID.
    file_path : str
        file location to store model to
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    response = download_model_info(model_id, config)
    return utils.download_file(response.url, response.filename, file_path, verbose)


def download_compiled_model(
    job_id: str,
    file_path: str,
    verbose: bool = True,
    config: Optional[ClientConfig] = None,
) -> str:
    """
    Download compiled model to file.

    Parameters
    ----------
    job_id : int
        Job ID.
    file_path : str
        file location to store compiled model to
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    # fetch compiled model
    url = utils.api_url("jobs", str(job_id), "download_compiled_model", config=config)
    header = utils.auth_header(config=config)
    response = utils.response_as_protobuf(
        requests.get(url, headers=header), api_pb.FileDownloadURL
    )
    return utils.download_file(response.url, response.filename, file_path, verbose)


__all__ = [
    "utils",
    "APIException",
    "ClientConfig",
    "Shapes",
    "get_auth_user",
    "get_user",
    "get_user_list",
    "get_dataset",
    "get_dataset_list",
    "get_device_list",
    "create_profile_job",
    "get_job",
    "get_job_list",
    "get_job_results",
    "create_validation_job",
    "upload_dataset",
    "upload_model",
    "download_model",
    "download_compiled_model",
    "get_model",
    "get_model_list",
]


def download_dataset_info(
    dataset_id: str, config: Optional[ClientConfig] = None
) -> api_pb.FileDownloadURL:
    """
    Get download information for a previously uploaded dataset.

    Parameters
    ----------
    dataset_id : int
        Dataset ID.
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    response : api_pb.FileDownloadURL
        Download information.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if config is None:
        config = utils.load_default_api_config()
    url = utils.api_url("datasets", str(dataset_id), "download_data", config=config)
    header = utils.auth_header(config=config)
    return utils.response_as_protobuf(
        requests.get(url, headers=header), api_pb.FileDownloadURL
    )


def download_dataset(
    dataset_id: str,
    file_path: str,
    verbose: bool = True,
    config: Optional[ClientConfig] = None,
) -> str:
    """
    Download a previously uploaded dataset.

    Parameters
    ----------
    dataset_id : int
        Dataset ID.
    file_path : str
        file location to store model to
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    response = download_dataset_info(dataset_id, config)
    return utils.download_file(response.url, response.filename, file_path, verbose)
