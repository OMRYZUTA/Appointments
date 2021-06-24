
class AppointmentScheduler():

    def __init__(self, doctors_list):
        self.doctors_list = doctors_list

    def get_available_doctors(self):
        return list(filter(lambda x:  not x.is_busy, self.doctors_list))
