import os
import sqlite3
import unittest
import uuid


from sqlite3 import Error
from user import User
from login_system import LoginSystem
from db_connector import DbConnector

AVI_NAME = 'Avi Cohen'
AVI_PASSWORD = '123456'

YOSI_NAME = 'Yosi Cohen'
YOSI_PASSWORD = '323243'

JON_NAME = 'Jon Cohen'
JON_PASSWORD = '234332'

MEDICAL_DATABASE_NAME = 'Medical.db'


class TestAppointments(unittest.TestCase):
    def setUp(self):
        self.user_avi = User(uuid.uuid1(), AVI_NAME, AVI_PASSWORD)
        self.login_system = LoginSystem()
        self.db_connector = DbConnector()

    def test_user(self):
        self.assertEqual(AVI_NAME, self.user_avi.name)
        self.assertEqual(AVI_PASSWORD, self.user_avi.password)

    def test_login_system_sign_up(self):
        self.user_yosi = self.login_system.SignUp(
            uuid.uuid1(), YOSI_NAME, YOSI_PASSWORD)
        self.assertEqual(YOSI_NAME, self.user_yosi.name)
        self.assertEqual(YOSI_PASSWORD, self.user_yosi.password)

    def test_database_exists(self):
        self.assertTrue(os.path.isfile(MEDICAL_DATABASE_NAME))

    def test_jon_in_database(self):
        self.user_jon = self.login_system.SignUp(
            uuid.uuid1(), JON_NAME, JON_PASSWORD)
        self.db_connector.add_user(
            self.user_jon.ID, self.user_jon.name, self.user_jon.password)
        user_tuple = self.db_connector.get_user(self.user_jon.ID)
        (id,name,password) = user_tuple
        jon = User(id,name,password)
        self.assertEqual(jon.ID, self.user_jon.ID)


if __name__ == "__main__":
    unittest.main()
