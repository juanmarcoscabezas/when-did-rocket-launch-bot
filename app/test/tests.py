import unittest
from bot.utils import bisect


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.chat_data = {
            "chat_id": 1234,
            "left": 0,
            "right": 10,
            "mid": 7,
            "attempts": 0,
            "finished": False,
        }

    def test_bisect_positive(self):
        new_data = bisect(chat=self.chat_data.copy(), message='yes')
        self.assertEqual(first=new_data['right'], second=self.chat_data['mid'])
        self.assertEqual(first=new_data['left'], second=self.chat_data['left'])
        self.assertEqual(first=new_data['mid'], second=4)

    def test_bisect_negative(self):
        new_data = bisect(chat=self.chat_data.copy(), message='no')
        self.assertEqual(first=new_data['left'], second=self.chat_data['mid'])
        self.assertEqual(first=new_data['right'],
                         second=self.chat_data['right'])
        self.assertEqual(first=new_data['mid'], second=9)
