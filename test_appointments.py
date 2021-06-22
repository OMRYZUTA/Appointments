import os
from patient import Patient
import sqlite3
import unittest
import uuid
import time

from sqlite3 import Error
from user import User
from doctor import Doctor
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
        self.patient_avi = Patient(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        self.patient_jon = Patient(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.patient_yosi = Patient(YOSI_USER_NAME, YOSI_NAME, YOSI_PASSWORD)

    def test_user(self):
        self.assertEqual(AVI_NAME, self.patient_avi.name)
        self.assertEqual(AVI_USER_NAME, self.patient_avi.user_name)
        self.assertEqual(AVI_PASSWORD, self.patient_avi.password)

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
        user_jon = User(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        user_tuple = DbConnector.get_user(user_jon.user_name)
        (user_name, name) = user_tuple
        self.assertEqual(user_name, user_jon.user_name)
        self.assertEqual(name, user_jon.name)

    def test_auth_jon(self):
        user_tuple = DbConnector.auth_user(
            JON_USER_NAME, JON_PASSWORD)
        (user_name, name) = user_tuple
        self.assertEqual(user_name, JON_USER_NAME)
        self.assertEqual(name, JON_NAME)

    def test_doctor_init(self):
        doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        self.assertEqual(doctor.name, AVI_NAME)
        self.assertEqual(doctor.user_name, AVI_USER_NAME)

    def test_doctor_TryTreat(self):
        doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        result = doctor.try_treat(self.patient_avi)
        self.assertTrue(result)

    def test_doctor_TryTreat_delay(self):
        doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        doctor.try_treat(self.patient_yosi)
        result = doctor.try_treat(self.patient_jon)
        for i in range(5):
            time.sleep(1)
        self.assertFalse(result)
        for i in range(100):
            time.sleep(1)
        result = doctor.try_treat(self.patient_jon)
        self.assertTrue(result)

    def test_doctor_TryTreat_waiting_list_add(self):
        doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        doctor.try_treat(self.patient_yosi)
        for i in range(10):
            time.sleep(1)
        result = doctor.try_treat(self.patient_jon)
        self.assertFalse(result)
        waiting_list = doctor.waiting_list
        self.assertEqual(len(waiting_list), 1)
        result = doctor.try_treat(self.patient_jon)
        self.assertEqual(len(waiting_list), 2)

    def test_doctor_init(self):
        patient = Patient(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.assertEqual(patient.name, JON_NAME)
        self.assertEqual(patient.user_name, JON_USER_NAME)


if __name__ == "__main__":
    unittest.main()
