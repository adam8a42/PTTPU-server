import socket
import sys
import os
import threading
import base64
IP = sys.argv[1]
DIR = sys.argv[2]
def PTTP_operation(PORT):
    ENCODING = "ascii"
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #IPv4, TCP
            s.bind( (IP, PORT) ) #PTTP(U)
            s.listen()
            connection_socket, address = s.accept()
            with connection_socket as conn:
                input = (conn.recv(1024).decode(ENCODING)).split()
                if input[0] == "GET" and input[2] == "PTTP/1.0":
                    input = input[1] 
                    path = DIR + '/' + input
                    print(path)
                    if os.path.isfile(path):
                        with open(path, encoding=ENCODING) as file:
                            data = file.read()
                            conn.sendall(data.encode(ENCODING))
                    elif os.path.isdir(path):
                        ls = ""
                        for line in os.listdir(path):
                            ls += f"{line}\n"
                        conn.sendall(ls.encode(ENCODING))
                    else:
                        conn.sendall(b"ERROR1")
                else:
                    conn.sendall(b"ERROR2")
def PTTPU_operation(PORT):
    ENCODING = "ascii"
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #IPv4, TCP
            s.bind( (IP, PORT) ) #PTTP(U)
            s.listen()
            connection_socket, address = s.accept()
            with connection_socket as conn:
                input = (base64.decodebytes(conn.recv(1024)).decode(ENCODING)).split()
                if input[0] == "GET" and input[2] == "PTTP/1.0":
                    input = input[1]
                    path = DIR + '/' + input
                    print(path)
                    if os.path.isfile(path):
                        with open(path, encoding=ENCODING) as file:
                            data = file.read()
                            conn.sendall(base64.encodebytes(data.encode(ENCODING)))
                    elif os.path.isdir(path):
                        ls = ""
                        for line in os.listdir(path):
                            ls += f"{line}\n"
                        conn.sendall(base64.encodebytes(ls.encode(ENCODING)))
                    else:
                        conn.sendall(base64.encodebytes(b"ERROR1"))
                else:
                    conn.sendall(base64.encodebytes(b"ERROR2"))
                



class PTTP(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        PTTP_operation(42750)
            
class PTTPU(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        PTTPU_operation(42751)

def main():
    threadPTTP = PTTP(0,"PTTP", 0)
    threadPTTP.start()
    threadPTTPU = PTTPU(1,"PTTPU", 1)
    threadPTTPU.start()

if __name__ == "__main__":
    main()

