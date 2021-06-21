import os
import sqlite3
import unittest
import uuid


from sqlite3 import Error
from user import User
from login_system import LoginSystem
from db_connector import DbConnector

AVI_NAME = 'Avi Cohen'
AVI_USER_NAME = 'Avi1984'
AVI_PASSWORD = '123456'

YOSI_NAME = 'Yosi Cohen'
YOSI_USER_NAME = 'YOSI_IS_THE_KING!11'
YOSI_PASSWORD = '323243'

JON_NAME = 'Jon Cohen'
JON_USER_NAME = 'Johny_Boy'
JON_PASSWORD = '234332'

MEDICAL_DATABASE_NAME = 'Medical.db'


class TestAppointments(unittest.TestCase):
    def setUp(self):
        self.user_avi = User(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)

    def test_user(self):
        self.assertEqual(AVI_NAME, self.user_avi.name)
        self.assertEqual(AVI_USER_NAME, self.user_avi.user_name)
        self.assertEqual(AVI_PASSWORD, self.user_avi.password)

    def test_login_system_sign_up(self):
        yosi_sign_up_result = LoginSystem.SignUp(
            YOSI_USER_NAME, YOSI_NAME, YOSI_PASSWORD)
        self.assertFalse(yosi_sign_up_result)

    def test_database_exists(self):
        self.assertTrue(os.path.isfile(MEDICAL_DATABASE_NAME))

    def test_jon_in_database(self):
        jon_sign_up_result = LoginSystem.SignUp(
            JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.assertFalse(jon_sign_up_result)
        self.user_jon = User(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        user_tuple = DbConnector.get_user(self.user_jon.user_name)
        (user_name, name, password) = user_tuple
        jon = User(user_name, name, password)
        self.assertEqual(jon.user_name, self.user_jon.user_name)


if __name__ == "__main__":
    unittest.main()
