import socket
import base64
HOST = "localhost"  # The server's hostname or IP address
PORT = 42751  # The port used by the server
ENCODING = "ascii"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(base64.encodebytes("GET subfolder1 PTTP/1.0".encode(ENCODING)))
    data = base64.decodebytes(s.recv(1024)).decode(ENCODING)

print(f"Received: {data}")