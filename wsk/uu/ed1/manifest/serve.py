# openssl req -new -x509 -keyout cert.pem -out cert.pem -days 365 -nodes

import ssl, socketserver
from http.server import SimpleHTTPRequestHandler

# class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def end_headers(self):
#         self.send_header("Access-Control-Allow-Origin", "*")
#         print("sending header")
#         http.server.SimpleHTTPRequestHandler.end_headers(self)


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        return super(CORSRequestHandler, self).end_headers()


# httpd = HTTPServer(('localhost', 8003), CORSRequestHandler)
# httpd.serve_forever()


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem")  # PUT YOUR cert.pem HERE
server_address = ("0.0.0.0", 3443)  # CHANGE THIS IP & PORT
handler = CORSRequestHandler  # CORSRequestHandlerSimpleHTTPRequestHandler
with socketserver.TCPServer(server_address, handler) as httpd:
    print(f"starting server on https://{server_address[0]}:{server_address[1]}/")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()


# #!/usr/bin/env python3
# from http.server import HTTPServer, SimpleHTTPRequestHandler, test
# import sys


# class CORSRequestHandler(SimpleHTTPRequestHandler):
#     def end_headers(self):
#         self.send_header("Access-Control-Allow-Origin", "*")
#         SimpleHTTPRequestHandler.end_headers(self)


# if __name__ == "__main__":
#     test(
#         CORSRequestHandler,
#         HTTPServer,
#         port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000,
#     )
