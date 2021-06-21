import unittest


class TestAppointments(unittest.TestCase):
    def test_good(self):
        self.assertEqual("foo".upper(), "FOO")


if __name__ == "__main__":
    unittest.main()
