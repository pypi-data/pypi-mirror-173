import mysql.connector


class MysqlConnection:
    def __init__(self, host, database, user, password):
        self.connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        self.cursor = self.connection.cursor()
        self.sql_logging = []

    def p(self):
        print("Se")

    def fetch_all(self, func):
        SELF = self

        def inner():
            res = func()
            SELF.p()

        return inner

    def __del__(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
