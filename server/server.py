#!/usr/bin/env python3

import socket

PORT = 4000


class Server:

    def __init__(self) -> None:
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname)

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.hostname, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
