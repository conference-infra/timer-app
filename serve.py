import contextlib
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os
import socket
import sys

# this script is "python -m http.server" but serves
# html pages without ".html"
# this mirrors the behavior on github pages

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        path = super().translate_path(path)
        if not os.path.exists(path):
            html_path = path + '.html'
            if os.path.exists(html_path):
                return html_path
        return path


if __name__ == '__main__':
    def _get_best_family(*address):
        infos = socket.getaddrinfo(
            *address,
            type=socket.SOCK_STREAM,
            flags=socket.AI_PASSIVE,
        )
        family, type, proto, canonname, sockaddr = next(iter(infos))
        return family, sockaddr

    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    DualStackServer.address_family, addr = _get_best_family(None, 8000)
    with DualStackServer(addr, partial(Handler, directory='public')) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
