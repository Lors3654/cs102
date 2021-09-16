import typing as tp

from httpserver import BaseHTTPRequestHandler, HTTPServer  # type:ignore

from .request import WSGIRequest  # type:ignore
from .response import WSGIResponse  # type:ignore

ApplicationType = tp.Any


class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[ApplicationType] = None

    def set_app(self, app: ApplicationType) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[ApplicationType]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        environ = request.to_environ()
        environ["SERVER_NAME"] = self.address[0]
        environ["SERVER_PORT"] = self.address[1]
        response = WSGIResponse()
        body_iterable = self.server.app(environ, response.start_response)
        response.body = b"".join(body_iterable)
        return response
