from db_connector import DbConnector
from tkinter import *
from login_system import LoginSystem


class Controller():

    @staticmethod
    def run():
        Controller.create_database()
        Controller.run_menu()

    @staticmethod
    def create_database():
        DbConnector.create_user_table()
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
        5. exit"""
        user_input = input(msg)
        Controller.operate_main_menu_answer(user_input)

    @staticmethod
    def operate_main_menu_answer(user_input):
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
            Controller.run_menu()

    @staticmethod
    def operate_doctor_sign_up():
        msg = "please insert your unique user name:"
        user_name = input(msg)
        msg = "please insert your name:"
        name = input(msg)
        msg = "please insert your password:"
        password = input(msg)
        sign_up_result = LoginSystem.doctor_sign_up(user_name, name, password)
        if(sign_up_result):
            Controller.operate_doctor_screen(user_name, name, password)
        else:
            Controller.run_menu()

    @staticmethod
    def operate_doctor_screen(user_name, name, password):
        pass
    

    @staticmethod
    def operate_doctor_login():
        pass
    @staticmethod
    def operate_patient_sign_up():
        pass
    @staticmethod
    def operate_patient_login():
        pass