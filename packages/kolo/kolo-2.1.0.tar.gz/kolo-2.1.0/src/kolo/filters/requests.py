from __future__ import annotations

import os
import time
import types
from typing import Dict, List, TYPE_CHECKING, Tuple

import ulid

from ..serialize import decode_body, decode_header_value


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict

    class ApiRequest(TypedDict):
        frame_id: str
        method: str
        url: str
        method_and_full_url: str
        body: str | None
        headers: Dict[str, str]
        timestamp: float | str
        type: Literal["outbound_http_request"]

    class BaseApiResponse(TypedDict):
        frame_id: str
        timestamp: float | str
        status_code: int
        headers: Dict[str, str]
        type: Literal["outbound_http_response"]
        method: str
        url: str
        method_and_full_url: str

    class ApiResponse(BaseApiResponse, total=False):
        body: str


def get_full_url(frame_locals) -> str:
    scheme = frame_locals["self"].scheme
    host = frame_locals["self"].host
    port = frame_locals["self"].port
    url = frame_locals["url"]
    return f"{scheme}://{host}:{port}{url}"


class ApiRequestFilter:
    co_names: Tuple[str, ...] = ("urlopen", "request")
    urllib3_filename = os.path.normpath("urllib3/connectionpool")
    requests_filename = os.path.normpath("requests/sessions")

    def __init__(self, config) -> None:
        self.config = config
        self.last_response: ApiResponse | None = None
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return (callable_name == "urlopen" and self.urllib3_filename in filepath) or (
            event == "return"
            and callable_name == "request"
            and self.requests_filename in filepath
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        frame_locals = frame.f_locals

        if event == "call":
            request_headers = {
                key: decode_header_value(value)
                for key, value in frame_locals["headers"].items()
            }

            full_url = get_full_url(frame_locals)
            method = frame_locals["method"].upper()
            method_and_full_url = f"{method} {full_url}"

            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(frame)] = frame_id
            api_request: ApiRequest = {
                "frame_id": frame_id,
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "body": decode_body(frame_locals["body"], request_headers),
                "headers": request_headers,
                "timestamp": time.time(),
                "type": "outbound_http_request",
            }
            return api_request

        assert event == "return"

        if frame.f_code.co_name == "urlopen":
            full_url = get_full_url(frame_locals)
            method = frame_locals["method"].upper()
            method_and_full_url = f"{method} {full_url}"

            response = frame_locals["response"]
            api_response: ApiResponse = {
                "frame_id": self._frame_ids[id(frame)],
                "headers": dict(response.headers),
                "method": method,
                "method_and_full_url": method_and_full_url,
                "status_code": response.status,
                "timestamp": time.time(),
                "type": "outbound_http_response",
                "url": full_url,
            }
            self.last_response = api_response
            return api_response
        else:
            response = frame_locals["resp"]
            assert self.last_response is not None
            self.last_response["body"] = response.text
