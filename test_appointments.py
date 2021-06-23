import os
from patient import Patient
import sqlite3
import unittest
import uuid
import time
import datetime

from sqlite3 import Error
from user import User
from doctor import Doctor
from login_system import LoginSystem
from db_connector import DbConnector
from waiting_list import WaitingList
from appointment import Appointment
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
        self.doctor_avi = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        self.patient_jon = Patient(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.patient_yosi = Patient(YOSI_USER_NAME, YOSI_NAME, YOSI_PASSWORD)

    def test_user(self):
        self.assertEqual(AVI_NAME, self.doctor_avi.name)
        self.assertEqual(AVI_USER_NAME, self.doctor_avi.user_name)
        self.assertEqual(AVI_PASSWORD, self.doctor_avi.password)

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
        result = doctor.try_treat(self.doctor_avi)
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

    def test_patient_init(self):
        patient = Patient(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.assertEqual(patient.name, JON_NAME)
        self.assertEqual(patient.user_name, JON_USER_NAME)

    def test_waiting_list_init(self):
        waiting_list = WaitingList(self.doctor_avi.user_name, [
                                   JON_USER_NAME, YOSI_USER_NAME])
        self.assertEqual(waiting_list.doctor_name, self.doctor_avi.user_name)
        self.assertEqual(waiting_list.patients_list[0], JON_USER_NAME)
        self.assertEqual(waiting_list.patients_list[1], YOSI_USER_NAME)

    def test_patient_began_appointment(self):
        AVI_JON_APPOINTMENT_DATE = str(datetime.datetime.now())
        AVI_JON_APPOINTMENT_ID = str(uuid.uuid1())
        appointment = Appointment(
            JON_USER_NAME, AVI_USER_NAME, AVI_JON_APPOINTMENT_DATE, AVI_JON_APPOINTMENT_ID)
        self.patient_jon.began_appointment(appointment)

    def test_waiting_list_add_patient(self):
        waiting_list = WaitingList(
            self.doctor_avi.user_name, [self.patient_jon])
        waiting_list.patients_list.append(self.patient_yosi)
        user_name_list = waiting_list.get_waiting_list_for_patient()
        self.assertEqual(user_name_list[0], self.patient_jon.user_name)
        self.assertEqual(user_name_list[1], self.patient_yosi.user_name)

    def test_appointment_in_db(self):
        AVI_JON_APPOINTMENT_DATE = str(datetime.datetime.now())
        AVI_JON_APPOINTMENT_ID = str(uuid.uuid1())
        appointment = Appointment(
            JON_USER_NAME, AVI_USER_NAME, AVI_JON_APPOINTMENT_DATE, AVI_JON_APPOINTMENT_ID)
        self.patient_jon.began_appointment(appointment)
        appointment_tuple = DbConnector.get_appointments_by_patient_user_name(
            JON_USER_NAME)
        for appointment_tup in appointment_tuple:
            print(appointment_tup)

    def test_appointment_init(self):
        # sqlite cast from datetime to str.
        AVI_JON_APPOINTMENT_DATE = str(datetime.datetime.now())
        AVI_JON_APPOINTMENT_ID = str(uuid.uuid1())
        appointment = Appointment(
            JON_USER_NAME, AVI_USER_NAME, AVI_JON_APPOINTMENT_DATE, AVI_JON_APPOINTMENT_ID)
        self.assertEqual(appointment.patient_user_name, JON_USER_NAME)
        self.assertEqual(appointment.doctor_user_name, AVI_USER_NAME)
        self.assertEqual(appointment.appointment_date,
                         AVI_JON_APPOINTMENT_DATE)
        self.assertEqual(appointment.appointment_id, AVI_JON_APPOINTMENT_ID)


if __name__ == "__main__":
    unittest.main()
