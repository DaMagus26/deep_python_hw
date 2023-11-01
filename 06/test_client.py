import unittest
import warnings
import client


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        client.logging.basicConfig(level=client.logging.CRITICAL)
        warnings.filterwarnings("ignore")

    def test_invalid_worker_number(self):
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=0, server_host="192.168.1.8", server_port=65432
            )

    def test_not_string_host(self):
        with self.assertRaises(TypeError):
            _ = client.Client(
                [], num_threads=1, server_host=192.0, server_port=65432
            )

    def test_invalid_host(self):
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123.123.123", server_port=65432
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123.123.", server_port=65432
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="300.123.123.123", server_port=65432
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123,123", server_port=65432
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123. 123. 123.123", server_port=65432
            )

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123.123.123", server_port=65432.
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123.123.123", server_port=-65432
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123.123.123", server_port='65432'
            )
        with self.assertRaises(ValueError):
            _ = client.Client(
                [], num_threads=1, server_host="123.123.123.123.123", server_port=70432
            )

    def test_partitioning(self):
        test_list = [1, 2, 3, 4, 5, 6]
        true_result6 = [[1], [2], [3], [4], [5], [6]]
        true_result4 = [[1, 2], [3, 4], [5, 6], []]
        true_result2 = [[1, 2, 3], [4, 5, 6]]
        true_result1 = [[1, 2, 3, 4, 5, 6]]
        self.assertListEqual(
            client.Client._partition_list(test_list, 6), true_result6
        )
        self.assertListEqual(
            client.Client._partition_list(test_list, 4), true_result4
        )
        self.assertListEqual(
            client.Client._partition_list(test_list, 2), true_result2
        )
        self.assertListEqual(
            client.Client._partition_list(test_list, 1), true_result1
        )
        with self.assertRaises(RuntimeError):
            _ = client.Client._partition_list(test_list, 7)


if __name__ == "__main__":
    unittest.main()
