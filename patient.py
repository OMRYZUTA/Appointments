from user import User


class Patient(User):
    def __init__(self, user_name, name, password):
        super().__init__(user_name, name, password)
        self.waiting_list = []
