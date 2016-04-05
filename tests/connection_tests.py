from unittest import TestCase

from ircb.connection import Connection

class ConectionTests(TestCase):
    """
    Test the connection.Connection class
    """

    def test_decode(self):
        con_obj = Connection()
        self.assertEqual(
            "line",
            con_obj.decode("line".encode(encoding='UTF-8', errors='strict'))
        )
        self.assertEqual(
            "line",
            con_obj.decode("line".encode(encoding='latin-1', errors='strict'))
        )