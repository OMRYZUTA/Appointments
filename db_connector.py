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
                                        id text PRIMARY KEY,
                                        FOREIGN KEY (patient_user_name) REFERENCES patients(user_name),
                                        FOREIGN KEY (doctor_user_name) REFERENCES doctors(user_name)
                                        );'''

DOCTOR_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS doctors (
                                        user_name TEXT PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        password text NOT NULL);'''

PATIENT_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS patients (
                                        user_name TEXT PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        password text NOT NULL);'''

WAITING_LIST_MEMBERS_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS waiting_list_members (
                                        doctor_user_name NOT NULL,
                                        patient_user_name TEXT NOT NULL,
                                        id text NOT NULL,
                                        date text NOT NULL,
                                        FOREIGN KEY (patient_user_name) REFERENCES patients(user_name),
                                        FOREIGN KEY (doctor_user_name) REFERENCES doctors(user_name));'''


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
    def create_waiting_list_member_table():
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(WAITING_LIST_MEMBERS_TABLE_QUERY)
            sqliteConnection.commit()

    @staticmethod
    def create_doctor_table():
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(DOCTOR_TABLE_QUERY)
            sqliteConnection.commit()

    @staticmethod
    def create_patient_table():
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(PATIENT_TABLE_QUERY)
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
    def add_doctor(doctor):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO doctors (user_name, name, password) VALUES( ?,? ,? );", (doctor.user_name, doctor.name, doctor.password))

    @staticmethod
    def add_patient(patient):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO patients (user_name, name, password) VALUES( ?,? ,? );", (patient.user_name, patient.name, patient.password))

    @staticmethod
    def add_waiting_list_member(doctor_user_name, patient_user_name, waiting_list_id, date):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO waiting_list_members (doctor_user_name, patient_user_name, id, date) VALUES(?, ?, ?, ?);", (doctor_user_name, patient_user_name, waiting_list_id, date))

    @staticmethod
    def get_appointments_by_patient_user_name(patient_user_name):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT * FROM appointments WHERE patient_user_name = ?", [patient_user_name])
            return tuple(result)

    @staticmethod
    def get_appointments_get_waiting_list_members_by_list_id(waiting_list_id):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT * FROM waiting_list_members WHERE id = ?", [waiting_list_id])
            return tuple(result)

    @staticmethod
    def get_user(user_name):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT user_name, name FROM users WHERE user_name = ?", [user_name])
            return(tuple(result)[0])

    @staticmethod
    def auth_patient(user_name, password):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT user_name, name, password FROM patients WHERE user_name = ? AND password = ?", [user_name, password])
            return(tuple(result))

    @staticmethod
    def auth_doctor(user_name, password):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT user_name, name, password FROM doctors WHERE user_name = ? AND password = ?", [user_name, password])
            return(tuple(result))
