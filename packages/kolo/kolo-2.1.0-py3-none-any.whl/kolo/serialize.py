from __future__ import annotations

import gzip
import json
import os
import types
from cgi import parse_header
from collections.abc import Iterator
from contextlib import contextmanager
from typing import overload, Any, Dict, List, Tuple, TypeVar, TYPE_CHECKING


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict

    from django.http import HttpRequest, HttpResponse, StreamingHttpResponse

    class UserCodeCallSite(TypedDict):
        line_number: int
        call_frame_id: str

    Local = TypeVar("Local")


@contextmanager
def monkeypatch_queryset_repr():
    try:
        from django.db.models import QuerySet
    except ImportError:  # pragma: no cover
        yield
        return

    old_repr = QuerySet.__repr__

    def new_repr(queryset):
        if queryset._result_cache is None:
            return f"Unevaluated queryset for: {queryset.model}"
        return old_repr(queryset)

    QuerySet.__repr__ = new_repr  # type: ignore
    try:
        yield
    finally:
        QuerySet.__repr__ = old_repr  # type: ignore


def _serialize_local(local: "Local") -> "Local | str":
    if isinstance(local, Iterator):
        return f"Iterator object (type: {type(local)})"

    try:
        json.dumps(local)
    except (TypeError, OverflowError, ValueError):
        try:
            return repr(local)
        except Exception:
            return "SerializationError"
    return local


def serialize_function_args(args: Tuple[Any, ...]) -> Tuple[Any, ...]:
    return tuple([_serialize_local(arg) for arg in args])


def serialize_function_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    return {key: _serialize_local(value) for key, value in kwargs.items()}


def serialize_locals(locals: Dict[str, object]) -> Dict[str, object]:
    return {key: _serialize_local(value) for key, value in locals.items()}


class KoloJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return repr(obj)
        except Exception:
            return "SerializationError"


def serialize_potential_json(arg: object) -> str:
    if arg is None:
        return repr(arg)

    if isinstance(arg, Iterator):
        return f"Iterator object (type: {type(arg)})"

    try:
        return json.dumps(arg)
    except (TypeError, OverflowError, ValueError):
        try:
            return repr(arg)
        except Exception:
            return "SerializationError"


@overload
def serialize_query_data(data: None) -> None:
    """Stub method for mypy"""


@overload
def serialize_query_data(data: List[List[Any]]) -> List[List[Any]]:
    """Stub method for mypy"""


@overload
def serialize_query_data(data: List[int]) -> List[int]:
    """Stub method for mypy"""


def serialize_query_data(data):
    if not data or isinstance(data[0], int):
        return data

    data_out = []
    for rows in data:
        rows_out = []
        for row in rows:
            if isinstance(row, tuple):
                new_row: Any = serialize_function_args(row)  # pragma: no cover
            else:
                new_row = _serialize_local(row)
            rows_out.append(new_row)
        data_out.append(rows_out)
    return data_out


def decode_header_value(bytes_or_str: bytes | str) -> str:
    """
    Convert a bytes header value to text.

    Valid header values are expected to be ascii in modern times, but
    ISO-8859-1 (latin1) has historically been allowed.

    https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.4
    """
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode("latin1")
    return bytes_or_str


def get_call_frame(
    frame: types.FrameType, filepath: str, co_name: str
) -> types.FrameType | None:
    """Search back in a frame's stack for the triggering user code frame"""

    while frame.f_back is not None:
        frame = frame.f_back
        if frame.f_code.co_filename == filepath and frame.f_code.co_name == co_name:
            return frame
    return None


def get_callsite_data(
    frame: types.FrameType, call_frame_data: Dict[str, str]
) -> UserCodeCallSite | None:
    """
    Find the parent user code frame and return its frame_id and line number

    We already have the frame_id available in call_frame_data, but we don't
    know the currently active line number, so we search back in the frame
    stack using the filepath and co_name until we find the call frame itself.
    """
    call_frame = get_call_frame(
        frame, call_frame_data["filepath"], call_frame_data["co_name"]
    )
    if call_frame is None:
        return None
    return {
        "call_frame_id": call_frame_data["frame_id"],
        "line_number": call_frame.f_lineno,
    }


def frame_path(frame: types.FrameType) -> str:
    path = frame.f_code.co_filename
    try:
        relative_path = os.path.relpath(path)
    except ValueError:
        relative_path = path
    return f"{relative_path}:{frame.f_lineno}"


def decode_body(body: Any, request_headers: Dict[str, str]) -> Any:
    """Convert a request body into a json-serializable form."""
    try:
        json.dumps(body)
    except TypeError:
        if isinstance(body, bytes):
            content_type = request_headers.get("Content-Type", "")
            charset = parse_header(content_type)[1].get("charset", "utf-8")
            try:
                return body.decode(charset)
            except UnicodeDecodeError:
                return "<Binary request body>"
        return f"Error: Could not parse request body. Type: {type(body)}"
    return body


def get_content(response: HttpResponse | StreamingHttpResponse) -> str:
    if response.streaming:
        return "<Streaming Response>"

    if TYPE_CHECKING:
        assert isinstance(response, HttpResponse)
    content_encoding = response.get("Content-Encoding")
    if content_encoding == "gzip":
        content = gzip.decompress(response.content)
    else:
        content = response.content
    try:
        return content.decode(response.charset)
    except UnicodeDecodeError:
        return f"<Response with invalid charset ({response.charset})>"


def get_request_body(request: "HttpRequest") -> str:
    from django.http.request import RawPostDataException

    try:
        return request.body.decode("utf-8")
    except UnicodeDecodeError:  # pragma: no cover
        return "<Binary request body>"
    except RawPostDataException:
        return "<Request data already read>"
