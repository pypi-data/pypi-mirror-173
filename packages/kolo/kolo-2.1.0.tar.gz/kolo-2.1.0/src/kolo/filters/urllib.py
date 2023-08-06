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

    class ApiResponse(TypedDict):
        frame_id: str
        timestamp: float | str
        status_code: int
        headers: Dict[str, str]
        type: Literal["outbound_http_response"]
        method: str
        url: str
        method_and_full_url: str


class UrllibFilter:
    co_names: Tuple[str, ...] = ("do_open",)
    urllib_filename = os.path.normpath("urllib/request")

    def __init__(self, config) -> None:
        self.config = config
        self.last_response: ApiResponse | None = None
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return (
            frame.f_code.co_name == "do_open"
            and self.urllib_filename in frame.f_code.co_filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        request = frame.f_locals["req"]
        full_url = request.full_url
        method = request.get_method()
        method_and_full_url = f"{method} {full_url}"
        if event == "call":
            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(frame)] = frame_id
            request_headers = {
                key: decode_header_value(value) for key, value in request.header_items()
            }

            api_request: ApiRequest = {
                "frame_id": frame_id,
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "body": decode_body(request.data, request_headers),
                "headers": request_headers,
                "timestamp": time.time(),
                "type": "outbound_http_request",
            }
            return api_request

        elif event == "return":  # pragma: no branch
            response = frame.f_locals["r"]
            api_response: ApiResponse = {
                "frame_id": self._frame_ids[id(frame)],
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "timestamp": time.time(),
                "status_code": response.status,
                "headers": dict(response.headers),
                "type": "outbound_http_response",
            }
            return api_response
