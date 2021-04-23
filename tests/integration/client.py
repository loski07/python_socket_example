#!/usr/bin/env python3

import socket
import random
import time


class Client:
    def __init__(self, server_port: int = 4001, server_ip: str = None) -> None:
        self.server_port = server_port
        if server_ip:
            self.server_ip = server_ip
        else:
            self.server_ip = socket.gethostbyname(socket.gethostname())

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.server_ip, self.server_port))
                for i in range(100):
                    message = "{:0>9}\n".format(random.randint(0, 999999999))
                    # print("sending: '{}'".format(message))
                    s.sendall(bytes(message, encoding='utf8'))
                    time.sleep(0.5)
                s.send(b'terminate')
            except ConnectionRefusedError:
                print("Client terminated")


if __name__ == '__main__':
    c = Client()
    c.run()
