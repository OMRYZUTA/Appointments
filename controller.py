import os
from db_connector import DbConnector
from login_system import LoginSystem
from doctor import Doctor
from patient import Patient
import time
from appointment_scheduler import AppointmentScheduler


class Controller():
    appointment_scheduler = AppointmentScheduler()

    @staticmethod
    def run():
        Controller.create_database()
        Controller.run_menu()

    @staticmethod
    def create_database():
        DbConnector.create_appointment_table()
        DbConnector.create_doctor_table()
        DbConnector.create_patient_table()
        DbConnector.create_waiting_list_member_table()

    @staticmethod
    def run_menu():
        msg = """Welcome to Medical appointments
        please enter the option number you want:
        1. Doctor sign up
        2. Doctor log in
        3. Patient sign up
        4. Patient log in
        5. exit\n"""
        user_input = input(msg)
        Controller.clear_console()
        Controller.operate_main_menu_answer(user_input)

    @staticmethod
    def operate_main_menu_answer(user_input):
        appointment_scheduler = AppointmentScheduler()
        if(user_input == '1'):
            Controller.operate_doctor_sign_up()
        elif(user_input == '2'):
            Controller.operate_doctor_login()
        elif(user_input == '3'):
            Controller.operate_patient_sign_up()
        elif(user_input == '4'):
            Controller.operate_patient_login()
        elif(user_input != '5'):
            print(f"{user_input} is wrong input, try again")
            Controller.clear_console()
            Controller.run_menu()

    @staticmethod
    def operate_doctor_sign_up():
        msg = "please insert your unique user name:"
        user_name = input(msg)
        Controller.clear_console()
        msg = "please insert your name:"
        name = input(msg)
        Controller.clear_console()
        msg = "please insert your password:"
        password = input(msg)
        Controller.clear_console()
        sign_up_result = LoginSystem.doctor_sign_up(user_name, name, password)
        if(sign_up_result):
            Controller.operate_doctor_screen(user_name, name)
        else:
            print('sign up failed, please choose another user name')
            Controller.clear_console(2)
            Controller.run_menu()

    @staticmethod
    def operate_doctor_screen(user_name, name):
        msg = f"""Welcome {name}, please select from the following:
        1. watch waiting list
        2. exit \n"""
        result = input(msg)
        if result == '1':
            Controller.show_waiting_list(user_name, name)
            Controller.clear_console(5)
            Controller.operate_doctor_screen(
                user_name, name)

        elif(result == '2'):
            print('going to main menu')
            Controller.clear_console()
            Controller.run_menu()

    @staticmethod
    def show_waiting_list(user_name):
        waiting_list = Controller.appointment_scheduler.get_doctor_waiting_list(
            user_name)
        if(waiting_list.is_empty()):
            print('waiting list is empty, going back..')
            Controller.clear_console()
        else:
            print(f"{user_name}'s waiting list:")
            for patient in waiting_list.get_waiting_list_for_patient():
                print(patient)

    @staticmethod
    def operate_doctor_login():
        msg = "please insert your unique user name:"
        user_name = input(msg)
        Controller.clear_console()
        msg = "please insert your password:"
        password = input(msg)

        doctor = LoginSystem.doctor_log_in(user_name, password)
        if(doctor == None):
            print('incorrect user name or password')
            Controller.clear_console()
            Controller.run_menu()
        else:
            Controller.operate_doctor_screen(doctor.user_name, doctor.name)

    @staticmethod
    def operate_patient_sign_up():
        msg = "please insert your unique user name:"
        user_name = input(msg)
        Controller.clear_console()
        msg = "please insert your name:"
        name = input(msg)
        Controller.clear_console()
        msg = "please insert your password:"
        password = input(msg)
        Controller.clear_console()
        sign_up_result = LoginSystem.patient_sign_up(user_name, name, password)
        if(sign_up_result):
            Controller.operate_patient_screen(
                Patient(user_name=user_name, name=name))
        else:
            print('sign up failed, please choose another user name')
            Controller.clear_console(2)
            Controller.run_menu()

    @ staticmethod
    def operate_patient_login():
        msg = "please insert your unique user name:"
        user_name = input(msg)
        Controller.clear_console()
        msg = "please insert your password:"
        password = input(msg)

        patient = LoginSystem.patient_log_in(user_name, password)
        if(patient == None):
            print('incorrect user name or password')
            Controller.clear_console()
            Controller.run_menu()
        else:
            Controller.operate_patient_screen(patient)

    def operate_patient_screen(patient):
        msg = f"""Welcome {patient.name}, please select from the following:
        1. Watch all doctors
        2. Watch all available doctors
        3. Watch waiting lists
        4. Make an appointment
        5. Cancel appointment
        6. Exit \n"""
        choice = input(msg)
        if choice == '1':
            Controller.show_doctors_list(
                Controller.appointment_scheduler.doctors_list)
            Controller.clear_console(5)
            Controller.operate_patient_screen(patient)
        elif choice == '2':
            Controller.show_doctors_list(
                Controller.appointment_scheduler.get_available_doctors())
            Controller.clear_console(5)
            Controller.operate_patient_screen(patient)
        elif choice == '3':
            Controller.show_waiting_lists(patient)
        elif choice == '4':
            Controller.make_appointment(patient)
        elif choice == '5':
            Controller.cancel_appointment(patient)
        elif choice == '6':
            print('going to main menu')
            Controller.clear_console()
            Controller.run_menu()

    @ staticmethod
    def show_waiting_lists(patient):
        if len(patient.waiting_lists) == 0:
            print('You have no waiting lists, going back')
            choice = 'q'
            Controller.clear_console(2)
        else:
            print(f"{patient.name}'s waiting lists:")
            for waiting_list in patient.waiting_lists.keys():
                print(f"{waiting_list}")
            choice = input(
                'enter the doctor user you want to see, or enter q to go back:')
        if (choice == 'q'):
            Controller.operate_patient_screen(patient)
        else:
            Controller.show_waiting_list(choice)
            Controller.clear_console(5)
            Controller.operate_patient_screen(
                patient)

    @ staticmethod
    def make_appointment(patient):
        choice = input(
            """Please enter the doctor user name you want to be treated with or q to go back to  patient screen:\n""")
        if choice == 'q':
            Controller.operate_patient_screen(patient)
        elif(not Controller.appointment_scheduler.is_doctor_exist(choice)):
            print(f"{choice} is not in system, Please try again")
            Controller.make_appointment(patient)
        else:
            result = Controller.appointment_scheduler.make_appointment(
                choice, patient)
            print(f"you are {result}")
            Controller.clear_console(5)
            Controller.operate_patient_screen(patient)

    @ staticmethod
    def cancel_appointment(patient):
        choice = input(
            """Please enter the doctor user name you want to cancel the appointment with or q to go back to  patient screen:\n""")
        if choice == 'q':
            Controller.operate_patient_screen(patient)
        elif(not Controller.appointment_scheduler.is_doctor_exist(choice)):
            print(f"{choice} is not in system, Please try again")
            Controller.cancel_appointment(patient)
        else:
            result = Controller.appointment_scheduler.cancel_appointment(
                choice, patient)
            print(f"you are {result}")
            Controller.clear_console(5)
            Controller.operate_patient_screen(patient)

    @ staticmethod
    def show_doctors_list(doctors):
        i = 1
        for doctor in doctors:
            print(f"{i}. {doctor.user_name} -{doctor.name}")
            i += 1

    @ staticmethod
    def clear_console(delay=1):
        time.sleep(delay)
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
