import sqlite3

MEDICAL_DATABASE_NAME = 'Medical.db'
USER_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS users (
                                        user_name TEXT PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        password text NOT NULL);'''

USER_TABLE_NAME = 'users'


class DbConnector():
    @staticmethod
    def create_user_table():
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(USER_TABLE_QUERY)
            sqliteConnection.commit()

    @staticmethod
    def add_user(user):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO users (user_name, name, password) VALUES( ?,? ,? );", (user.user_name, user.name, user.password))
                
    @staticmethod
    def get_user(user_name):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT * FROM users WHERE user_name = ?", [user_name])
            return(tuple(result)[0])
