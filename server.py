import socket
import os
from logger import Log
from config import *

class MdToHtmlConverter:
    @staticmethod
    def get_md_from_html(md_file: str) -> str:
        #TODO: process md file before compiling html file.

        page_title = "No Title md file"
        html_body = ""

        prev_char = ''
        for line in md_file.splitlines():
            for char in line:
                if char == '*' and prev_char == "*":

        for line in md_file.split("\n"):
            if line.startswith("# "):
                html_body += f"<h1>{line[2:]}</h1>\n"
            elif line.startswith("## "):
                html_body += f"<h2>{line[3:]}</h2>\n"
            elif line.startswith("### "):
                html_body += f"<h3>{line[4:]}</h3>\n"
            elif line.startswith("#### "):
                html_body += f"<h4>{line[5:]}</h4>\n"
            elif line.startswith("##### "):
                html_body += f"<h5>{line[6:]}</h5>\n"  
            elif line.startswith("###### "):
                html_body += f"<h6>{line[7:]}</h6>\n"
            else:
                html_body += "<p>" + line + "</p>" + "\n"
        print(md_file.splitlines())
        print("End print")

        html_body = html_body.replace("**", "<b>")
        html_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
</head>
<body>
"""
        html_tail = """\n</body>
</html>"""
        return_html = html_head + html_body + html_tail
        return return_html.encode()

class Server:
    def __init__(self):
        # Setup the socket.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if VERBOSE: Log.success("Initialized Server")

    def start(self):
        """Binds the ip and port then sets the server to listen to requests."""
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(MAX_CLIENTS)
        Log.success(f"Started Server! at http://{IP}:{PORT}")

    def send_data_to_client(self, client_socket, response):
        """Sends data to the client"""

        # This shoulden't be used, failsafe.
        if isinstance(response, str):
            response = response.encode()

        # Send the data
        client_socket.sendall(response)
        client_socket.close()

    def check(self):
        # Wait and accept a client connection.
        client_socket, client_address = self.server_socket.accept()

        # Receive the client's request.
        client_request = client_socket.recv(MAX_RECV_SIZE).decode()

        # Process the client's request.
        headers = client_request.split('\n')

        # Make sure the client sent correct headers.
        if not headers or len(headers[0].split()) < 2:
            client_socket.close()
            Log.error("Client failed to send correct headers, aborting.")
            return
        
        http_method = headers[0].split()[0]
        request_path = Path(str(BASE_DIR) + headers[0].split()[1])

        abs_request_path = request_path.absolute()

        # Set file to serve.
        file_to_serve = None
        if request_path.is_dir():
            file_to_serve = request_path.joinpath("index.md")
        else:
            file_to_serve = abs_request_path
        
        # Make sure the file should be served:
        base_dir = os.path.abspath(BASE_DIR)
        full_path = os.path.abspath(os.path.normpath(file_to_serve))

        if not full_path.startswith(base_dir + os.sep):
            response = "HTTP/1.1 403 FORBIDDEN\r\n\r\n403 FORBIDDEN"
            self.send_data_to_client(client_socket, response)
            return
        
        if VERBOSE: Log.message(f"Client requests: {full_path} from: {headers[1]}")

        # Try to serve the file.
        try:
            with open(full_path, "rb") as f:
                content = f.read()

            header = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Length: {len(MdToHtmlConverter.get_md_from_html(content.decode()))}\r\n"
                "\r\n"
            ).encode()

            response = header + MdToHtmlConverter.get_md_from_html(content.decode())

        # If item not found
        except FileNotFoundError:
            response = "HTTP/1.1 404 NOTFOUND \r\n\r\n" + "404 not found"

        self.send_data_to_client(client_socket, response)

if __name__ == "__main__":
    server = Server()
    server.start()
    while True: server.check()