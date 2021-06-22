from user import User
from db_connector import DbConnector
import sqlite3


class LoginSystem():

    @staticmethod
    def Login(user_name, password):
        pass

    @staticmethod
    def SignUp(user_name, name, password):
        try:
            DbConnector.add_user(User(user_name, name, password))

        except sqlite3.IntegrityError:  # user already exist
            return False

        return True
