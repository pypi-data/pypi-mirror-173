"""mse_lib_sgx.http_server module."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import threading
import time
from typing import Union

import nacl

from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate

CERT: Union[SGXCertificate, SelfSignedCertificate, None] = None
EXIT_EVENT = threading.Event()


class SGXHTTPRequestHandler(BaseHTTPRequestHandler):
    """SGX HTTP server to unseal encrypted application."""

    def do_GET(self):
        """GET /."""
        msg: bytes = b"Waiting for sealed symmetric key..."
        self.send_response(200)
        self.send_header("Content-Length", str(len(msg)))
        self.end_headers()
        self.wfile.write(msg)

    def do_POST(self):
        """POST /."""
        content_length: int = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        print(body)
        if len(body) >= 48:  # minimum seal box lenght
            try:
                if CERT is not None:
                    msg = CERT.unseal(body)
                    print(msg)
                    self.send_response_only(200)
                    self.end_headers()
                    EXIT_EVENT.set()
            except (nacl.exceptions.CryptoError, nacl.exceptions.TypeError):
                self.send_response_only(401)
                self.end_headers()
        else:
            self.send_response_only(401)
            self.end_headers()


def serve(hostname: str, port: int, certificate: Union[SGXCertificate,
                                                       SelfSignedCertificate]):
    """Serve simple SGX HTTP server."""
    global CERT  # pylint: disable=global-statement

    CERT = certificate

    httpd = HTTPServer((hostname, port), SGXHTTPRequestHandler)

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(
        certfile=str(certificate.cert_path.resolve()),
        keyfile=str(certificate.key_path.resolve()),
    )

    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    threading.Thread(target=kill_event, args=(httpd,)).start()
    httpd.serve_forever()


def kill_event(httpd: HTTPServer):
    """Kill HTTP server in a thread if `EXIT_EVENT` is set."""
    while True:
        if EXIT_EVENT.is_set():
            httpd.shutdown()
            return

        time.sleep(1)
