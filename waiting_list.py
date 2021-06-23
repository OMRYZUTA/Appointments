
class WaitingList():
    def __init__(self, doctor_name, patients_list):
        self.doctor_name = doctor_name
        self.patients_list = patients_list

    def get_waiting_list_for_patient(self):
        return list(map(lambda patient: patient.user_name, self.patients_list))
