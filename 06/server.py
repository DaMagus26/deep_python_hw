import socket
from socket import gethostbyname, gethostname
import threading
import json
from concurrent.futures import ThreadPoolExecutor
import logging
import argparse
from collections import Counter
import re
from typing import Optional
import requests
from bs4 import BeautifulSoup


class Server:
    def __init__(
        self,
        num_workers: int,
        host: Optional[str] = None,
        port: Optional[int] = None,
        top_results: Optional[int] = 7,
        debug: Optional[bool] = False,
    ) -> None:
        # Validations
        ip_regex = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$")
        if num_workers < 1:
            raise ValueError("num_workers must be greater than 0")
        if host and not isinstance(host, str):
            raise TypeError(f"host must be a string: {host}")
        if host and not ip_regex.match(host):
            raise ValueError(f"invalid host address: {host}")
        if port and (
            not isinstance(port, int) or (port and (port > 65535 or port < 0))
        ):
            raise ValueError(f"invalid port: {port}")
        if top_results < 0:
            raise ValueError("top results must be a positive number")

        self._num_workers = num_workers
        self._host = host or gethostbyname(gethostname())
        self._port = port or 65432
        self._top_results = top_results
        self._total_processed = 0
        self._debug = debug

    def start(self) -> None:
        with ThreadPoolExecutor(max_workers=self._num_workers) as executor:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self._host, self._port))
                server_socket.listen()
                logging.info(f"Server is listening on {self._host}:{self._port}")
                try:
                    while True:
                        conn, _ = server_socket.accept()
                        logging.debug(f"Accepted connection from {conn}")
                        url = conn.recv(1024).decode().strip()
                        executor.submit(self._process_connection, conn, url)
                        if self._debug:
                            break
                except KeyboardInterrupt:
                    logging.info("Shutting down server...")
                    server_socket.close()

    def _process_connection(
        self,
        conn: socket.socket,
        url: str,
    ) -> None:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url=url, headers=headers, timeout=10)
            if response.status_code == 200:
                self._total_processed += 1
                print(
                    f"({threading.current_thread().name}) Total URLs processed: ",
                    self._total_processed,
                )
                soup = BeautifulSoup(response.text, "html.parser")
                most_common_words = self._most_common_words(soup)
                conn.send(most_common_words.encode())
                logging.debug(
                    f"({threading.current_thread().name}) Response sent to {conn}"
                )
            else:
                logging.error(
                    f"({threading.current_thread().name}) Requests error:"
                    f"{response.status_code=}"
                )
                conn.send(b"{}")
        except Exception as err:
            logging.error(
                f"({threading.current_thread().name}) Error occurred:"
                f"{err}: {err.args}"
            )
            return

    def _most_common_words(
        self,
        soup: BeautifulSoup,
    ) -> str:
        words = soup.get_text().split()
        counter = Counter(words)
        return json.dumps(dict(counter.most_common(self._top_results)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(prog="Server application")
    parser.add_argument("-n", "--num_workers", type=int)
    parser.add_argument("-k", "--top_k", default=7, type=int)
    parser.add_argument("--host", type=str, default=gethostbyname(gethostname()))
    parser.add_argument("--port", type=int, default=65432)
    arguments = parser.parse_args()

    server = Server(
        num_workers=arguments.num_workers,
        top_results=arguments.top_k,
        host=arguments.host,
        port=arguments.port,
    )
    server.start()
