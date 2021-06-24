from db_connector import DbConnector


def main():
    DbConnector.create_user_table()
    DbConnector.create_appointment_table()
    DbConnector.create_doctor_table()
    DbConnector.create_patient_table()
    DbConnector.create_waiting_list_member_table()


if __name__ == '__main__':
    main()
