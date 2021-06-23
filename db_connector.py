import sqlite3

MEDICAL_DATABASE_NAME = 'Medical.db'
USER_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS users (
                                        user_name TEXT PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        password text NOT NULL);'''

USER_TABLE_NAME = 'users'
APPOINTMENT_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS appointments (
                                        patient_user_name TEXT NOT NULL,
                                        doctor_user_name TEXT NOT NULL,
                                        date text NOT NULL,
                                        id text PRIMARY KEY);'''

APPOINTMENT_TABLE_NAME = 'appointments'


class DbConnector():
    @staticmethod
    def create_user_table():
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(USER_TABLE_QUERY)
            sqliteConnection.commit()

    @staticmethod
    def create_appointment_table():
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(APPOINTMENT_TABLE_QUERY)
            sqliteConnection.commit()

    @staticmethod
    def add_appointment(appointment):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO appointments (patient_user_name, doctor_user_name, date, id) VALUES( ?,? ,?, ?);", (appointment.patient_user_name, appointment.doctor_user_name, appointment.appointment_date, appointment.appointment_id))

    @staticmethod
    def add_user(user):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO users (user_name, name, password) VALUES( ?,? ,? );", (user.user_name, user.name, user.password))

    @staticmethod
    def get_appointments_by_patient_user_name(patient_user_name):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT * FROM appointments WHERE patient_user_name = ?", [patient_user_name])
            return tuple(result)

    @staticmethod
    def get_user(user_name):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT user_name, name FROM users WHERE user_name = ?", [user_name])
            return(tuple(result)[0])

    @staticmethod
    def auth_user(user_name, password):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT user_name, name FROM users WHERE user_name = ? AND password = ?", [user_name, password])
            return(tuple(result)[0])
