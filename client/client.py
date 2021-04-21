#!/usr/bin/env python3

import socket
import random


class Client:
    def __init__(self, server_port: int = 4000, server_ip: str = None) -> None:
        self.server_port = server_port
        if server_ip:
            self.server_ip = server_ip
        else:
            self.server_ip = socket.gethostbyname(socket.gethostname())

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            for i in range(10):
                message = "{}\n".format(random.randint(0, 999999999))
                # print("sending: '{}'".format(message))
                s.sendall(bytes(message, encoding='utf8'))
            s.send(b'terminate')


if __name__ == '__main__':
    c = Client()
    c.run()
