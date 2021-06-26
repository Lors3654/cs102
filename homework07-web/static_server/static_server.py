import mimetypes
import os
import pathlib
import time
import typing as tp
from datetime import datetime
from urllib.parse import quote, unquote, urlparse, urlunparse

from httpserver import (
    BaseHTTPRequestHandler,
    BaseRequestHandler,
    HTTPRequest,
    HTTPResponse,
    HTTPServer,
)


def url_normalize(path: str) -> str:
    parts = urlparse(path)
    return urlunparse(parts._replace(path=quote(parts.path)))


class StaticHTTPRequestHandler(BaseHTTPRequestHandler):
    def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        # NOTE: https://tools.ietf.org/html/rfc3986
        # NOTE: echo -n "GET / HTTP/1.0\r\n\r\n" | nc localhost 5000
        content: bytes = b""
        status: int = 200
        headers: tp.Dict[str, str] = dict()
        content_type: tp.Optional[str] = "text/html"

        if request.method not in [b"GET", b"HEAD"]:
            content = b"No methods available"
            status = 405
            headers = {
                "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Server": "Custom HTTP Server",
                "Content-Length": str(len(content)),
                "Content-Type": "text/plain",
                "Allow": "GET, HEAD",
            }

        else:
            url = request.url.decode(encoding="utf-8")  # url_normalize()
            parsed_url = urlparse(unquote(url))
            path = (
                parsed_url.path + "index.html" if parsed_url.path.endswith("/") else parsed_url.path
            )
            path = self.server.document_root + path  # type: ignore

            if os.path.isfile(path) and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        content = f.read()
                    content_type = mimetypes.guess_type(url)[0]
                except OSError:
                    status = 404
                    print("Invalid file requested", parsed_url.path)
                except Exception as e:
                    status = 404
                    print("Unexpected error:", e)
            else:
                status = 404
                print("Invalid path requested", path)

            headers = {
                "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "Server": "Custom HTTP Server",
                "Content-Length": str(len(content)),
                "Content-Type": "text/html" if content_type is None else content_type,
            }

            if request.method == b"HEAD":  # zerofy content if head request
                content = b""

        response = self.response_klass(status=status, headers=headers, body=content)

        return response


class StaticServer(HTTPServer):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        backlog_size: int = 1,
        max_workers: int = 1,
        timeout: tp.Optional[float] = 5,
        request_handler_cls: tp.Type[StaticHTTPRequestHandler] = StaticHTTPRequestHandler,
        document_root: pathlib.Path = pathlib.Path("."),
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            backlog_size=backlog_size,
            max_workers=max_workers,
            timeout=timeout,
            request_handler_cls=request_handler_cls,
        )
        self.document_root = document_root


if __name__ == "__main__":
    document_root = pathlib.Path("static") / "root"
    server = StaticServer(
        timeout=60,
        document_root=document_root,
        request_handler_cls=StaticHTTPRequestHandler,
    )
    server.serve_forever()
