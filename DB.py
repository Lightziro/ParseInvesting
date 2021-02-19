import mysql.connector
class DB:

    hostDB = '141.8.192.26'
    userDB = 'a0514245_shop'
    passwordDB = 'Tuscano32'
    dataBaseDB = 'a0514245_shop'

    def __init__(self):
        try:
            db = mysql.connector.connect(host=self.hostDB, user=self.userDB, password=self.passwordDB, database=self.dataBaseDB)
            self.datebase = db
            self.send = db.cursor()
        except mysql.connector.Error as err:
            self.error = err
            print(self.error)

    def __del__(self):
        del self.datebase
        del self.send


