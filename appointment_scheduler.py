from db_connector import DbConnector
from login_system import LoginSystem


class AppointmentScheduler():

    def __init__(self):
        doctors_list = DbConnector.get_doctors_list()
        self.doctors_list = list(map(
            lambda x: LoginSystem.doctor_log_in(x[0], x[1]), doctors_list))
        self.doctor_dict = dict(
            map(lambda x: (x.user_name, x), self.doctors_list))

    def get_available_doctors(self):
        return list(filter(lambda x: not x.is_busy, self.doctors_list))

    def make_appointment(self, doctor_user_name, patient):
        treated = self.doctor_dict[doctor_user_name].try_treat(patient)
        result = 'entered to waiting list'
        if(treated):
            result = 'being treated'
        return result

    def cancel_appointment(self, doctor_user_name, patient):
        removed = False
        if(patient.remove_from_waiting_list(doctor_user_name)):
            treated = self.doctor_dict[doctor_user_name].waiting_list.remove_patient(
                patient)
            result = 'removed from waiting list'
        else:
            result = "already began the appointment, can't cancel"
        return result

    def is_doctor_exist(self, doctor_user_name):
        return doctor_user_name in self.doctor_dict.keys()

    def get_doctor_waiting_list(self, doctor_user_name):
        return self.doctor_dict[doctor_user_name].waiting_list
