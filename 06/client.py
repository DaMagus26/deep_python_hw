import threading
import socket
from typing import Sequence, Any, List
import logging
import argparse
import os
import re


class Client:
    def __init__(
            self,
            urls: Sequence[Sequence[str]],
            num_threads: int,
            server_host: str,
            server_port: int,
    ) -> None:
        # Validations
        ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$")
        if not isinstance(urls, Sequence):
            raise TypeError('urls must be a sequence')
        if num_threads < 1:
            raise ValueError("num_workers must be greater than 0")
        if server_host and not isinstance(server_host, str):
            raise TypeError(f"host must be a string: {server_host}")
        if server_host and not ip_regex.match(server_host):
            raise ValueError(f"invalid host address: {server_host}")
        if server_port and (not isinstance(server_port, int) or
                            (server_port and (server_port > 65535 or server_port < 0))):
            raise ValueError(f"invalid port: {server_port}")

        self.urls = urls
        self.num_threads = num_threads
        self.server_host = server_host
        self.server_port = server_port

    def _send_requests(
            self,
            urls: Sequence[str],
    ) -> None:
        for url in urls:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.server_host, self.server_port))
                    client_socket.sendall(url.encode())
                    response = client_socket.recv(1024).decode()
                    print(f"{url}: {response}")
            except Exception as err:
                logging.error(f"Error while sending request to {url}: {str(err)}")

    @staticmethod
    def _partition_list(
            sequence: Sequence[Any],
            parts: int,
    ) -> List[Sequence]:
        if parts > len(sequence):
            raise RuntimeError('parts must be less than len(sequence)')
        step = len(sequence) // parts + (1 if len(sequence) % parts else 0)
        result = [
            sequence[i:min(i + step, len(sequence))]
            for i in range(0, len(sequence), step)
        ]
        result += [[]] * (parts - len(result))
        return result

    def start(
            self
    ) -> None:
        try:
            threads = []
            for url_batch in self._partition_list(self.urls, self.num_threads):
                thread = threading.Thread(target=self._send_requests, args=(url_batch,))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            logging.info('Client was interrupted by user')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(prog="Server application")
    parser.add_argument(
        "--urls",
        type=str,
        default="urls.txt",
    )
    parser.add_argument(
        "-n",
        "--num_threads",
        type=int, default=1,
    )
    parser.add_argument(
        "--host",
        type=str, default="192.168.1.8",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=65432,
    )
    arguments = parser.parse_args()

    if not os.path.exists(arguments.urls):
        raise OSError('No such path:', arguments.urls)
    with open(arguments.urls, 'r', encoding='UTF-8') as f:
        urls_list = [url.strip() for url in f.readlines()]

    client = Client(
        urls=urls_list,
        num_threads=arguments.num_threads,
        server_host=arguments.host,
        server_port=arguments.port,
    )
    client.start()
