import time
from user import User
import threading
import random


class Doctor(User):
    def __init__(self, user_name, name, password):
        super().__init__(user_name, name, password)
        self.is_busy = False
        self.waiting_list = []

    def treat_patient(self):
        self.is_busy = True
        for i in range(random.randint(50, 100)):
            time.sleep(1)
        self.is_busy = False

    def try_treat(self, patient):
        result = False
        if (not self.is_busy):
            threading.Thread(target=self.treat_patient).start()
            result = True
        else:
            self.waiting_list.append(patient)
        return result
