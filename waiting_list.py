import uuid
from db_connector import DbConnector
import datetime


class WaitingList():
    def __init__(self, doctor_user_name, patients_list=None):
        self.doctor_user_name = doctor_user_name
        self.patients_list = patients_list
        self.id = str(uuid.uuid1())

    def get_waiting_list_for_patient(self):
        return list(map(lambda patient: patient.user_name, self.patients_list))

    def remove_patient(self, patient):
        if patient in self.patients_list:
            self.patients_list.remove(patient)
            DbConnector.remove_waiting_list_member(
                self.doctor_user_name, patient.user_name, self.id)

    def append_patient(self, patient):
        if(self.patients_list == None):
            self.patients_list = []
        self.patients_list.append(patient)
        DbConnector.add_waiting_list_member(
            self.doctor_user_name, patient.user_name, self.id, str(datetime.datetime.now()))

    def is_empty(self):
        return (self.patients_list == None or len(self.patients_list) == 0)

    def get_next_patient(self):
        next_patient = None
        if not self.is_empty():
            next_patient = self.patients_list[0]
        return next_patient
