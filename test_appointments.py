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
from appointment_scheduler import AppointmentScheduler

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

    def test_login_system_doctor_sign_up(self):
        avi_sign_up_result = LoginSystem.doctor_sign_up(
            AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        self.assertFalse(avi_sign_up_result)

    def test_login_system_patient_sign_up(self):
        yosi_sign_up_result = LoginSystem.patient_sign_up(
            YOSI_USER_NAME, YOSI_NAME, YOSI_PASSWORD)
        self.assertFalse(yosi_sign_up_result)

    def test_login_system_patient_log_in(self):
        yosi_log_in_result = LoginSystem.patient_log_in(
            YOSI_USER_NAME, YOSI_PASSWORD)
        self.assertEqual(yosi_log_in_result.user_name, YOSI_USER_NAME)

    def test_login_system_doctor_log_in(self):
        waiting_list = WaitingList(AVI_USER_NAME)
        waiting_list.append_patient(self.patient_jon)
        avi_log_in_result = LoginSystem.doctor_log_in(
            AVI_USER_NAME, AVI_PASSWORD)
        self.assertEqual(avi_log_in_result.user_name, AVI_USER_NAME)
        self.assertEqual(
            avi_log_in_result.waiting_list.get_next_patient().user_name, JON_USER_NAME)
        waiting_list.remove_patient(self.patient_jon)

    def test_database_exists(self):
        self.assertTrue(os.path.isfile(MEDICAL_DATABASE_NAME))

    def test_jon_in_database(self):
        jon_sign_up_result = LoginSystem.patient_sign_up(
            JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.assertFalse(jon_sign_up_result)

    def test_doctor_init(self):
        doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
        self.assertEqual(doctor.name, AVI_NAME)
        self.assertEqual(doctor.user_name, AVI_USER_NAME)

    # def test_doctor_TryTreat(self):
    #     doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
    #     result = doctor.try_treat(self.doctor_avi)
    #     self.assertTrue(result)

    # def test_doctor_TryTreat_delay(self):
    #     doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
    #     doctor.try_treat(self.patient_yosi)
    #     result = doctor.try_treat(self.patient_jon)
    #     for i in range(5):
    #         time.sleep(1)
    #     self.assertFalse(result)
    #     for i in range(100):
    #         time.sleep(1)
    #     result = doctor.try_treat(self.patient_jon)
    #     self.assertTrue(result)

    # def test_doctor_TryTreat_waiting_list_add(self):
    #     doctor = Doctor(AVI_USER_NAME, AVI_NAME, AVI_PASSWORD)
    #     doctor.try_treat(self.patient_yosi)
    #     for i in range(10):
    #         time.sleep(1)
    #     result = doctor.try_treat(self.patient_jon)
    #     self.assertFalse(result)
    #     waiting_list = doctor.waiting_list
    #     self.assertEqual(len(waiting_list), 1)
    #     result = doctor.try_treat(self.patient_jon)
    #     self.assertEqual(len(waiting_list), 2)

    def test_patient_init(self):
        patient = Patient(JON_USER_NAME, JON_NAME, JON_PASSWORD)
        self.assertEqual(patient.name, JON_NAME)
        self.assertEqual(patient.user_name, JON_USER_NAME)

    def test_waiting_list_init(self):
        waiting_list = WaitingList(self.doctor_avi.user_name, [
                                   self.patient_jon, self.patient_yosi])
        self.assertEqual(waiting_list.doctor_user_name,
                         self.doctor_avi.user_name)
        self.assertEqual(
            waiting_list.patients_list[0].user_name, JON_USER_NAME)
        self.assertEqual(
            waiting_list.patients_list[1].user_name, YOSI_USER_NAME)

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
        waiting_list.remove_patient(self.patient_yosi)

    def test_appointment_in_db(self):
        AVI_JON_APPOINTMENT_DATE = str(datetime.datetime.now())
        AVI_JON_APPOINTMENT_ID = str(uuid.uuid1())
        appointment = Appointment(
            JON_USER_NAME, AVI_USER_NAME, AVI_JON_APPOINTMENT_DATE, AVI_JON_APPOINTMENT_ID)
        self.patient_jon.began_appointment(appointment)
        appointment_tuple = DbConnector.get_appointments_by_patient_user_name(
            JON_USER_NAME)
        for appointment_tup in appointment_tuple:
            self.assertEqual(appointment_tup[0], JON_USER_NAME)

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

    def test_remove_from_list(self):
        self.patient_jon.waiting_lists[AVI_USER_NAME] = WaitingList(
            AVI_USER_NAME, [self.patient_yosi, self.patient_jon])
        result = self.patient_jon.remove_from_waiting_list(AVI_USER_NAME)
        self.assertTrue(result)

    def test_remove_from_list_fails(self):
        self.patient_jon.waiting_lists[AVI_USER_NAME] = WaitingList(
            AVI_USER_NAME, [self.patient_jon, self.patient_yosi])
        self.patient_jon.began_appointment(Appointment(
            JON_USER_NAME, AVI_USER_NAME, str(datetime.datetime.now), str(uuid.uuid1())))
        result = self.patient_jon.remove_from_waiting_list(AVI_USER_NAME)
        self.assertFalse(result)

    def test_appointment_scheduler_init(self):
        appScheduler = AppointmentScheduler([self.doctor_avi])
        doctor_list = appScheduler.get_available_doctors()
        self.assertEqual(doctor_list[0].user_name, AVI_USER_NAME)

    def test_waiting_list_in_db(self):
        self.doctor_avi.is_busy = True
        self.doctor_avi.try_treat(self.patient_yosi)
        DbConnector.add_waiting_list_member(
            self.doctor_avi.user_name, self.patient_yosi.user_name, self.doctor_avi.waiting_list.id, str(datetime.datetime.now()))
        list_tuple = DbConnector.get_waiting_list_members_by_doctor_user_name(
            AVI_USER_NAME)
        self.assertTrue(len(list_tuple) >= 1)

    def test_waiting_list_is_empty(self):
        waiting_list = WaitingList(self.doctor_avi.user_name, [
                                   self.patient_jon, self.patient_yosi])
        waiting_list.remove_patient(self.patient_yosi)
        waiting_list.remove_patient(self.patient_jon)
        self.assertTrue(waiting_list.is_empty())

    # def test_doctor_treat_two_patients(self):
    #     self.doctor_avi.try_treat(self.patient_jon)
    #     for i in range(8):
    #         time.sleep(1)
    #     self.doctor_avi.try_treat(self.patient_yosi)
    #     for i in range(150):
    #         time.sleep(1)
    #     appointment_tuple = DbConnector.get_appointments_by_patient_user_name(
    #         YOSI_USER_NAME)
    #     self.assertEqual((appointment_tuple[0])[0], YOSI_USER_NAME)


if __name__ == "__main__":
    unittest.main()
