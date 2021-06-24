import time
from user import User
import threading
import random
from waiting_list import WaitingList
from appointment import Appointment
import datetime
import uuid


class Doctor(User):
    def __init__(self, user_name, name, password):
        super().__init__(user_name, name, password)
        self.is_busy = False
        self.waiting_list = WaitingList(user_name)

    def treat_patient(self):
        self.is_busy = True
        while self.current_patient is not None:
            self.current_patient.began_appointment(Appointment(
                self.current_patient.user_name, self.user_name, str(datetime.datetime.now()), str(uuid.uuid1())))
            for i in range(random.randint(50, 100)):
                time.sleep(1)
            self.waiting_list.remove_patient(self.current_patient)
            self.current_patient = self.waiting_list.get_next_patient()
        self.is_busy = False

    def try_treat(self, patient):
        result = False
        if (not self.is_busy):
            self.current_patient = patient
            threading.Thread(target=self.treat_patient).start()
            result = True
        else:
            self.waiting_list.append_patient(patient)
            patient.add_waiting_list(self.waiting_list)
        return result
