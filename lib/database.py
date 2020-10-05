import yaml
import mysql.connector

class Database():
    def __init__(self):
        f = open("settings.yaml", "r")
        settings = yaml.load(f, Loader=yaml.FullLoader)
        self.host = settings['db_host']
        self.user = settings['db_user']
        self.database = settings['database']
        self.con = mysql.connector.connect(host=self.host, user=self.user)
        self.cursor = self.con.cursor()
        query = "USE " + self.database
        self.cursor.execute(query)
        self.con.commit()

    def create(self, table, rows):
        query = "CREATE TABLE IF NOT EXISTS " + table + "(" + rows + ");"
        self.cursor.execute(query)
        self.con.commit()

    def select(self, str, params=None):
        self.cursor.execute(str, params)
        return self.cursor.fetchall()

    def insert(self, str, params=None):
        self.cursor.execute(str, params)
        self.con.commit()
