import socket
import sys
import os


IP = sys.argv[1]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #IPv4, TCP
    s.bind( (IP, 42750) ) #PTTP
    s.listen()
    connection_socket, address = s.accept()
    with connection_socket as conn:
        input = conn.recv(1024).decode("utf-8")
        path = f"./files/" + input
        print(path)
        if os.path.isfile(path):
            with open(path) as file:
                data = file.read()
                conn.sendall(data.encode("utf-8"))
        elif os.path.isdir(path):
            conn.sendall(os.listdir(path))
        else:
             conn.sendall(b"ERROR1")
    



