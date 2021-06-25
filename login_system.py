from user import User
from doctor import Doctor
from patient import Patient
from db_connector import DbConnector
import sqlite3
from waiting_list import WaitingList


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
                patient.waiting_lists = LoginSystem.parse_patient_waiting_lists(
                    user_name)
            return patient

        except sqlite3.IntegrityError:  # patient isn't exist
            return None

    def doctor_log_in(user_name, password):
        try:
            doctor = None
            result = DbConnector.auth_doctor(user_name, password)
            if len(result) != 0:
                waiting_list = LoginSystem.parse_doctor_waiting_list(user_name)
                result = result[0]
                doctor = Doctor(
                    user_name=result[0], name=result[1], password=result[2], waiting_list=waiting_list)
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
            return True

        except sqlite3.IntegrityError:  # user already exist
            return False

        return True

    @staticmethod
    def parse_doctor_waiting_list(doctor_user_name):
        waiting_list = DbConnector.get_waiting_list_members_by_doctor_user_name(
            doctor_user_name)
        waiting_list_members = list(
            map(lambda patient: Patient(patient[0]), waiting_list))
        waiting_list = WaitingList(doctor_user_name, waiting_list_members)
        return waiting_list

    @staticmethod
    def parse_patient_waiting_lists(user_name):
        waiting_lists = {}
        waiting_list_members = DbConnector.get_waiting_list_members_by_patient_user_name(
            user_name)
        for member in waiting_list_members:
            waiting_lists[member[0]] = LoginSystem.parse_doctor_waiting_list(
                member[0])
        return waiting_lists
