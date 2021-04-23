#!/usr/bin/env python3

import argparse
import codecs
import os
import socket
import tempfile
import threading

import select
import sys
import time

try:
    from argcomplete import autocomplete
except ImportError:
    # If module argcomplete is not available, just skip the completion
    def autocomplete(_):
        pass


class Server:
    """
    Class that encapsulates all the logic of the socket example application.
    :arg self.server_socket: Socket where the server will be listening for messages.
    :arg self.socket_list: List of socket for selection.
    :arg self.unique_messages: Set of unique messages received from the clients. Only written by the main thread.
    :arg self.unique_messages_size_10s_ago: Number of unique messages received from the clients 10 seconds ago.
        Only written by the logger thread.
    :arg self.repeated_msg_num: Number of repeated messages received from the clients. Only written by the main thread.
    :arg self.repeated_msg_num_10s_ago: Number of repeated messages received from the clients 10 seconds ago.
        Only written by the logger thread.
    :arg self.end_logger: Flag to tell the logger to stop.
    """

    def __init__(self, server_port: int = 4000) -> None:
        """
        Constructor that initializes all object attributes.
        :param server_port: listening port for the server.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((socket.gethostname(), server_port))
        except OSError:
            print("The port {} is already in use, switching to 4001".format(server_port))
            self.server_socket.bind((socket.gethostname(), 4001))
        self.server_socket.listen(5)

        self.socket_list = [self.server_socket]
        self.unique_messages = set()
        self.unique_messages_size_10s_ago = 0
        self.repeated_msg_num = 0
        self.repeated_msg_num_10s_ago = 0
        self.end_logger = False

    def __del__(self) -> None:
        """
        Destructor of the object. Closes the socket list and dumps the list of messages to a file.
        """
        for sock in self.socket_list:
            sock.close()
        with open(tempfile.gettempdir() + "/numbers.log", "w") as logfile:
            for m in self.unique_messages:
                logfile.write("{}{}".format(m, os.linesep))

    def run(self) -> None:
        """
        Main method of the class. Implements the loop listening for messages from the clients.
        """
        message_size = sys.getsizeof(1) + sys.getsizeof(os.linesep)
        while True:
            readable, writable, errored = select.select(self.socket_list, [], [])
            for polled_socket in readable:
                if polled_socket is self.server_socket:
                    client_socket, address = self.server_socket.accept()
                    self.socket_list.append(client_socket)
                else:
                    raw_data = polled_socket.recv(message_size)
                    if not raw_data:
                        polled_socket.close()
                        self.socket_list.remove(polled_socket)
                    else:
                        parsed_data = codecs.decode(raw_data, 'UTF-8').split(os.linesep)
                        for m in parsed_data:
                            if 'terminate' == m:
                                # We stop analyzing the messages read from the socket. We were told to terminate.
                                self.end_logger = True
                                return
                            elif '' != m:
                                if m in self.unique_messages:
                                    self.repeated_msg_num += 1
                                self.unique_messages.add(m)

    def log_summary(self) -> None:
        """
        Method that logs the current status of received messages.
        """
        while not self.end_logger:
            current_unique_messages_size = len(self.unique_messages)
            new_unique = current_unique_messages_size - self.unique_messages_size_10s_ago
            self.unique_messages_size_10s_ago = current_unique_messages_size

            current_duplicates = self.repeated_msg_num
            new_duplicates = current_duplicates - self.repeated_msg_num_10s_ago
            self.repeated_msg_num_10s_ago = current_duplicates
            print("Received {} unique numbers, {} duplicates. Unique total: {}".format(
                new_unique, new_duplicates, current_unique_messages_size))
            time.sleep(10)


def parse_command_line():
    """
    Parses the user input.
    :return: argparse.Namespace with the user input.
    """
    parser = argparse.ArgumentParser(
        description="Server that listens for numbers in a given port and writes them to a file.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-p", "--port", required=False, default=4000, action="store", type=int,
                        help="Port were the server will be listening.")

    autocomplete(parser)
    return parser.parse_args()


def main() -> None:
    """Main function of the module. Runs the server."""
    args = parse_command_line()
    server = Server(args.port)

    # Run logging thread every 10 seconds
    logger = threading.Timer(10, server.log_summary)
    logger.start()

    server.run()


if __name__ == '__main__':
    main()
