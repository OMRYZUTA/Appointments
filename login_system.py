from user import User
from doctor import Doctor
from patient import Patient
from db_connector import DbConnector
import sqlite3


class LoginSystem():

    @staticmethod
    def patient_log_in(user_name, password):
        try:
            patient = None
            result = DbConnector.auth_patient(user_name, password)
            if len(result) != 0:
                result = result[0]
                patient = Patient(
                    user_name=result[0], name=result[1], password=result[2])
            return patient

        except sqlite3.IntegrityError:  # patient isn't exist
            return None

    def doctor_log_in(user_name, password):
        try:
            doctor = None
            result = DbConnector.auth_doctor(user_name, password)
            if len(result) != 0:
                result = result[0]
                doctor = Doctor(
                    user_name=result[0], name=result[1], password=result[2])
            return doctor

        except sqlite3.IntegrityError:  # doctor isn't exist
            return None

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
