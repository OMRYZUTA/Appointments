from user import User
from doctor import Doctor
from patient import Patient
from db_connector import DbConnector
import sqlite3


class LoginSystem():

    @staticmethod
    def Login(user_name, password):
        pass

    @staticmethod
    def doctor_sign_up(user_name, name, password):
        try:
            DbConnector.add_doctor(Doctor(user_name, name, password))

        except sqlite3.IntegrityError:  # user already exist
            return False

        return True

    @staticmethod
    def patient_sign_up(user_name, name, password):
        try:
            DbConnector.add_patient(Patient(user_name, name, password))

        except sqlite3.IntegrityError:  # user already exist
            return False

        return True

    @staticmethod
    def SignUp(user_name, name, password):
        try:
            DbConnector.add_user(User(user_name, name, password))

        except sqlite3.IntegrityError:  # user already exist
            return False

        return True
