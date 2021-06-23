from user import User
from db_connector import DbConnector
from appointment import Appointment


class Patient(User):
    def __init__(self, user_name, name, password):
        super().__init__(user_name, name, password)
        self.waiting_list = {}

    def began_appointment(self, appointment):
        self.waiting_list.pop(appointment.doctor_user_name, None)
        DbConnector.add_appointment(appointment)
