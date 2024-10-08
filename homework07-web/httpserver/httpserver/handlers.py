from __future__ import annotations

import http
import socket
import typing as tp
from datetime import datetime

from httptools import HttpRequestParser  # type: ignore
from httptools.parser.errors import HttpParserCallbackError  # type: ignore
from httptools.parser.errors import HttpParserError  # type: ignore
from httptools.parser.errors import HttpParserInvalidMethodError  # type: ignore
from httptools.parser.errors import HttpParserInvalidStatusError  # type: ignore
from httptools.parser.errors import HttpParserInvalidURLError  # type: ignore
from httptools.parser.errors import HttpParserUpgrade  # type: ignore

from .request import HTTPRequest  # type: ignore
from .response import HTTPResponse  # type: ignore

if tp.TYPE_CHECKING:
    from .server import TCPServer  # type: ignore

Address = tp.Tuple[str, int]


class BaseRequestHandler:
    def __init__(self, socket: socket.socket, address: Address, server: TCPServer) -> None:
        self.socket = socket
        self.address = address
        self.server = server

    def handle(self) -> None:
        self.close()

    def close(self) -> None:
        self.socket.close()


class EchoRequestHandler(BaseRequestHandler):
    def handle(self) -> None:
        try:
            data = self.socket.recv(1024)
        except (socket.timeout, BlockingIOError):
            pass
        else:
            self.socket.sendall(data)
        finally:
            self.close()


class BaseHTTPRequestHandler(BaseRequestHandler):
    request_klass = HTTPRequest
    response_klass = HTTPResponse

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = HttpRequestParser(self)

        self._url: bytes = b""
        self._headers: tp.Dict[bytes, bytes] = {}
        self._body: bytes = b""
        self._parsed = False

    def handle(self) -> None:
        request = self.parse_request()
        if request:
            try:
                response = self.handle_request(request)
            except Exception:
                # TODO: log exception
                response = self.response_klass(status=500, headers={}, body=b"")
        else:
            response = self.response_klass(status=400, headers={}, body=b"")
        self.handle_response(response)
        self.close()

    def parse_request(self) -> tp.Optional[HTTPRequest]:
        while not self._parsed:
            try:
                data = self.socket.recv(1024)
                if not data:
                    print("Break")
                    break
                self.parser.feed_data(data)

            except socket.timeout:
                print("timeout")
                break
            except (
                HttpParserCallbackError,
                HttpParserError,
                HttpParserInvalidStatusError,
                HttpParserInvalidMethodError,
                HttpParserInvalidURLError,
                HttpParserUpgrade,
            ):
                print("parser error")
        if self._parsed:
            response = self.request_klass(
                method=self.parser.get_method(),
                url=self._url,
                headers=self._headers,
                body=self._body,
            )
        return response

    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        return self.response_klass(status=405, headers={}, body=b"")

    def handle_response(self, response: HTTPResponse) -> None:
        self.socket.sendall(response.to_http1())

    def on_url(self, url: bytes) -> None:
        self._url = url
        print("on_url complete", url)

    def on_header(self, name: bytes, value: bytes) -> None:
        self._headers[name] = value
        print("on_header complete", name, value)

    def on_body(self, body: bytes) -> None:
        self._body = body
        print("on_body complete", body)

    def on_message_complete(self) -> None:
        self._parsed = True
        print("on_message_complete complete")
