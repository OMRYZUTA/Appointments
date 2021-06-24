
class AppointmentScheduler():

    def __init__(self, doctors_list):
        self.doctors_list = doctors_list

    def get_available_doctors(self):
        return list(filter(lambda x: True if not x.is_busy else False, self.doctors_list))
