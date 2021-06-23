from user import User


class Patient(User):
    def __init__(self, user_name, name, password):
        super().__init__(user_name, name, password)
        self.waiting_list = {}

    def began_appointment(self, doctor_user_name, appointment_date):
        self.waiting_list.pop(doctor_user_name, None)
        print(
            f'{self.user_name} got appointment with {doctor_user_name} at {appointment_date}')
