from db_connector import DbConnector


def main():
    db_connector = DbConnector()
    db_connector.create_user_table()


if __name__ == '__main__':
    main()
