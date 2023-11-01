import json
import unittest
from unittest import mock
from collections import namedtuple
import warnings
import server


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        server.logging.basicConfig(level=server.logging.CRITICAL)
        warnings.filterwarnings("ignore")

    def test_invalid_worker_number(self):
        with self.assertRaises(ValueError):
            _ = server.Server(0)

    def test_not_string_host(self):
        with self.assertRaises(TypeError):
            _ = server.Server(3, host=10.23)

    def test_invalid_host(self):
        with self.assertRaises(ValueError):
            _ = server.Server(3, host="123.123.123.123.123")
        with self.assertRaises(ValueError):
            _ = server.Server(3, host="123.123.123.123.")
        with self.assertRaises(ValueError):
            _ = server.Server(3, host="300.123.123.123")
        with self.assertRaises(ValueError):
            _ = server.Server(3, host="255.123.123,123")
        with self.assertRaises(ValueError):
            _ = server.Server(3, host="255. 123. 123. 123")

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            _ = server.Server(3, port=10000.0)
        with self.assertRaises(ValueError):
            _ = server.Server(3, port=-10000)
        with self.assertRaises(ValueError):
            _ = server.Server(3, port="10000")
        with self.assertRaises(ValueError):
            _ = server.Server(3, port=70000)

    def test_invalid_top_results(self):
        with self.assertRaises(ValueError):
            _ = server.Server(3, top_results=-1)

    @mock.patch("server.BeautifulSoup")
    def test_most_common_words_short(self, soup_mock):
        soup_mock.get_text = lambda: "mock mock stock poke"
        test_server = server.Server(3)
        result = test_server._most_common_words(soup_mock)
        true_result = '{"mock": 2, "stock": 1, "poke": 1}'
        self.assertEqual(result, true_result)

    @mock.patch("server.BeautifulSoup")
    def test_most_common_words_long(self, soup_mock):
        soup_mock.get_text = lambda: (
            "mock mock mock stock stock poke poke stroke "
            "stroke talk talk walk walk stalk stalk chalk"
        )
        test_server = server.Server(3)
        result = test_server._most_common_words(soup_mock)
        true_result = json.dumps(
            {
                "mock": 3,
                "stock": 2,
                "poke": 2,
                "stroke": 2,
                "talk": 2,
                "walk": 2,
                "stalk": 2,
            }
        )
        self.assertEqual(result, true_result)

    @mock.patch.object(server.socket.socket, "accept")
    @mock.patch.object(server.socket.socket, "recv")
    @mock.patch.object(server.ThreadPoolExecutor, "submit")
    def test_server(self, submit_mock, recv_mock, accept_mock):
        recv_mock.return_value = b"https://docs.python.org/3/library/socketserver.html"
        accept_mock.return_value = server.socket.socket(), None
        test_server = server.Server(3, debug=True)
        test_server.start()
        self.assertTrue(submit_mock.called)

    @mock.patch("server.requests.get")
    @mock.patch.object(server.socket.socket, "send")
    @mock.patch("server.socket.socket")
    def test_valid_url(self, socket_mock, send_mock, get_mock):
        response = namedtuple("Response", ["status_code", "text"])
        response.text = "sample text"
        response.status_code = 200
        get_mock.return_value = response
        conn = socket_mock.return_value
        conn.send = send_mock

        test_server = server.Server(3, debug=True)
        test_server._process_connection(conn, "https://example.com")
        self.assertEqual(test_server._total_processed, 1)
        self.assertEqual(conn.send.call_args, mock.call(b'{"sample": 1, "text": 1}'))

    @mock.patch("server.requests")
    @mock.patch.object(server.socket.socket, "send")
    @mock.patch("server.socket.socket")
    def test_valid_url_with_error(self, socket_mock, send_mock, requests_mock):
        def raise_error(*args, **kwargs):
            raise ConnectionError("Oops")

        response = namedtuple("Response", ["status_code", "text"])
        response.text = "sample text"
        response.status_code = 200
        requests_mock.get = raise_error
        conn = socket_mock.return_value

        test_server = server.Server(3, debug=True)
        test_server._process_connection(conn, "https://example.com")
        self.assertEqual(test_server._total_processed, 0)
        self.assertEqual(send_mock.call_args, None)

    @mock.patch("server.requests.get")
    @mock.patch.object(server.socket.socket, "send")
    @mock.patch("server.socket.socket")
    def test_valid_url_with_no_response(self, socket_mock, send_mock, get_mock):
        response = namedtuple("Response", ["status_code", "text"])
        response.text = "sample text"
        response.status_code = 404
        get_mock.return_value = response
        conn = socket_mock.return_value
        conn.send = send_mock

        test_server = server.Server(3, debug=True)
        test_server._process_connection(conn, "https://example.com")
        self.assertEqual(test_server._total_processed, 0)
        self.assertEqual(send_mock.call_args, mock.call(b"{}"))


if __name__ == "__main__":
    unittest.main()
