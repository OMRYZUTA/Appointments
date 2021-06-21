import sqlite3

MEDICAL_DATABASE_NAME = 'Medical.db'
USER_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS users (
                                        id TEXT PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        password text NOT NULL);'''

USER_TABLE_NAME = 'users'


class DbConnector():
    def create_user_table(self):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(USER_TABLE_QUERY)
            sqliteConnection.commit()

    def add_user(self, ID, name, password):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            cursor.execute(
                "INSERT INTO users (id, name, password) VALUES( ?,? ,? );", (ID, name, password))

    def get_user(self, ID):
        with sqlite3.connect(MEDICAL_DATABASE_NAME) as sqliteConnection:
            cursor = sqliteConnection.cursor()
            result = cursor.execute(
                "SELECT * FROM users WHERE id = ?", [ID])
            return(tuple(result)[0])
