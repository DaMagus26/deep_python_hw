import unittest
from unittest import mock
import sys
from model import SomeModel, predict_message_mood


class TestPredictMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.model = mock.Mock(spec=SomeModel)

    def test_invalid_model(self) -> None:
        with self.assertRaises(TypeError):
            predict_message_mood('text', object())

    def test_invalid_thrash(self):
        self.model.predict.return_value = 0.2
        with self.assertRaises(RuntimeError):
            predict_message_mood('text',
                                 model=self.model,
                                 bad_thresholds=0.5,
                                 good_thresholds=0.3)

        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 bad_thresholds=-1,
                                 good_thresholds=0),
            'отл'
        )

        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 bad_thresholds=1,
                                 good_thresholds=1.1),
            'неуд'
        )

    def test_good_message(self) -> None:
        self.model.predict.return_value = 0.7
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model), 'отл')
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 good_thresholds=0.65), 'отл')

    def test_bad_messages(self) -> None:
        self.model.predict.return_value = 0.2
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model), 'неуд')
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 bad_thresholds=0.21), 'неуд')

    def test_ok_messages(self) -> None:
        self.model.predict.return_value = 0.3
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model), 'норм')
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 bad_thresholds=0.3), 'норм')
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 good_thresholds=0.3), 'норм')
        self.assertEqual(
            predict_message_mood('text',
                                 model=self.model,
                                 bad_thresholds=0.3,
                                 good_thresholds=0.3), 'норм')

    def test_invalid_message(self) -> None:
        self.model.predict.return_value = 0.3
        with self.assertRaises(TypeError):
            print(predict_message_mood(None, model=self.model))


if __name__ == '__main__':
    unittest.main()
