from user import User
from db_connector import DbConnector
from appointment import Appointment


class Patient(User):
    def __init__(self, user_name, name, password):
        super().__init__(user_name, name, password)
        self.waiting_lists = {}

    def began_appointment(self, appointment):
        self.waiting_lists.pop(appointment.doctor_user_name, None)
        DbConnector.add_appointment(appointment)

    def remove_from_waiting_list(self, doctor_user_name):
        result = False
        if(doctor_user_name in self.waiting_lists.keys()):
            self.waiting_lists[doctor_user_name].remove_patient(self)
            result = True
        return result

    def add_waiting_list(self, waiting_list):
        self.waiting_lists[waiting_list.doctor_user_name] = waiting_list
