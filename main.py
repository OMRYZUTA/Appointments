from db_connector import DbConnector


def main():
    DbConnector.create_user_table()
    DbConnector.create_appointment_table()


if __name__ == '__main__':
    main()
