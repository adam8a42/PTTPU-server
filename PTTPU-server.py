#!/bin/python3
import socket
import sys
import os
import threading
import base64
import time
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
                #Checking the command
                if len(input) != 3:
                    path = DIR

                elif input[0] == "GET" and input[2] == "PTTP/1.0":
                    input = input[1] 
                    path = DIR + input
                    print("path = ")

                else: #incorrect command
                    conn.sendall(b"ERROR1: Wrong command")
                    while(conn.recv(1024)):
                            time.sleep(0.01)
                    conn.close()

                #checking files
                if os.path.isfile(path):
                    with open(path, encoding=ENCODING) as file:
                        data = file.read() + "<<PTTP END>>"
                        print(data.encode(ENCODING))
                        conn.sendall(data.encode(ENCODING))
                        while(conn.recv(1024)):
                            time.sleep(0.01)
                        conn.close()

                elif os.path.isdir(path):
                    ls = ""
                    for line in os.listdir(path):
                        ls += f"{line}\n"
                    ls += "<<PTTP END>>"
                    conn.sendall(ls.encode(ENCODING))
                    while(conn.recv(1024)):
                        time.sleep(0.01)
                    conn.close()

                else: #no file or directory
                    conn.sendall(b"ERROR2: File/directory does not exist")
                    while(conn.recv(1024)):
                        time.sleep(0.01)
                    conn.close()
def PTTPU_operation(PORT):
    ENCODING = "ascii"
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #IPv4, TCP
            s.bind( (IP, PORT) ) #PTTP(U)
            s.listen()
            connection_socket, address = s.accept()
            with connection_socket as conn:
                input = (base64.decodebytes(conn.recv(1024)).decode(ENCODING)).split()
                if len(input) != 3:
                    path = DIR

                elif input[0] == "GET" and input[2] == "PTTP/1.0":
                    input = input[1]
                    path = DIR + input
                    print(path)

                else:
                    conn.sendall(base64.encodebytes(b"ERROR1: Wrong command"))
                    while(conn.recv(1024)):
                            time.sleep(0.01)
                    conn.close()

                if os.path.isfile(path):
                    with open(path, encoding=ENCODING) as file:
                        data = file.read() + "<<PTTP END>>"
                        conn.sendall(base64.encodebytes(data.encode(ENCODING)))
                        while(conn.recv(1024)):
                            time.sleep(0.01)
                        conn.close()
                elif os.path.isdir(path):
                    ls = ""
                    for line in os.listdir(path):
                        ls += f"{line}\n"
                    ls += "<<PTTP END>>"
                    conn.sendall(base64.encodebytes(ls.encode(ENCODING)))
                    while(conn.recv(1024)):
                        time.sleep(0.01)
                    conn.close()
                else:
                    conn.sendall(base64.encodebytes(b"ERROR2: File/directory does not exist"))
                    while(conn.recv(1024)):
                        time.sleep(0.01)
                    conn.close()
                



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

