#!/usr/bin/env python3

import socket
import codecs

PORT = 4000


class Server:

    def __init__(self, server_port: int = 4000) -> None:
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.hostname)
        self.server_port = server_port
        self.clients = []

    def run(self) -> None:
        termination_request = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.hostname, self.server_port))
            s.listen()
            conn, addr = s.accept()
            self.clients.append({'connection': conn, 'address': addr, 'messages_received': []})
            while not termination_request:
                for c in self.clients:
                    raw_msg = c['connection'].recv(1024)
                    messages = codecs.decode(raw_msg, 'UTF-8').split('\n')
                    for msg in messages:
                        if 'terminate' in msg:
                            termination_request = True
                            self.log_summary()
                            self.terminate()
                        else:
                            c['messages_received'].append(msg)

    def log_summary(self):
        for c in self.clients:
            print("Number of messages sent by {}: {}".format(c['address'], len(c['messages_received'])))

    def terminate(self):
        for c in self.clients:
            c['connection'].close()
            print("connection {} closed".format(c['connection']))


if __name__ == '__main__':
    s = Server()
    s.run()
