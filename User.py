from custom import method
from DB import DB

db = DB()


class User:

    def __init__(self, telegramID = str()):
        global db
        sql = "SELECT id, lastName, firstName, telegramId, dateLastMessage, dateRegister " \
              "FROM telegramData WHERE telegramId = %(telegramID)s"
        params = { 'telegramID': telegramID }
        try:
            db.send.execute(sql, params)
        except:
            del db
            db = DB()
            db.send.execute(sql, params)
        for (id, lastName, firstName, telegramId, dateLastMessage, dateRegister) in db.send:
            self.id = id
            if lastName is not None:
                self.lastName = lastName
            self.firstName = firstName
            self.fullName = self.getFullName()
            self.telegramId = telegramId
            self.dateLastMessage = dateLastMessage
            self.dateRegister = dateRegister


    def getFullName(self):
        fullName = str()
        if self.lastName is not None:
            fullName = self.firstName + ' ' + self.lastName
        else:
            fullName = self.firstName
        return fullName

    def removeQuotation(self, arField = []):
        """
        Function for removing quotation from the user's table
        :param arField: Array with the code and the name of the quotation
        :return: False if the stock is not found, True if it is found
        """

        global db
        if method.is_array(arField):
            # Checking quotation in table with user
            sql = "SELECT * FROM QuotationUser WHERE idUser = %(id)s AND code = %(code)s"
            params = {'id': self.id, 'code': arField['codeQuotation']}
            db.send.execute(sql, params)
            result = db.send.fetchall()
            if len(result) == 0:
                return False
            # Deleting a quotation from a user's table
            sql = "DELETE FROM QuotationUser WHERE idUser = %(id)s AND code = %(code)s"
            try:
                db.send.execute(sql, params)
                db.datebase.commit()
            except Exception:
                del db
                db = DB()
                db.send.execute(sql, params)
                db.datebase.commit()
            return True


    def addQuotation(self, arField = []):
        global db
        if method.is_array(arField):
            sql = "INSERT INTO QuotationUser (idUser, name, code) VALUES (%(id)s, %(name)s, %(code)s)"
            params = {
                'id': self.id,
                'name': arField['nameQuotation'],
                'code': arField['codeQuotation'],
            }
            try:
                db.send.execute(sql, params)
                db.datebase.commit()
            except Exception:
                del db
                db = DB()
                db.send.execute(sql, params)
                db.datebase.commit()
            return True

    def getQuotation(self):
        arFieldQuotation = []
        global db
        sql = "SELECT name, code FROM QuotationUser WHERE idUser = %(id)s"
        params = {
            'id': self.id
        }
        db.send.execute(sql, params)
        for (name, code) in db.send:
            arFieldQuotation.append({
                'name': name,
                'code': code,
            })
        return arFieldQuotation

    @staticmethod
    def checkUserDB(telegramId=str()):
        global db
        sql = "SELECT id FROM telegramData WHERE telegramId = %(telegramID)s"
        params = {'telegramID': telegramId}
        try:
            db.send.execute(sql, params)
        except:
            del db
            db = DB()
            db.send.execute(sql, params)
        result = db.send.fetchall()
        if len(result) == 0:
            return False

    @staticmethod
    def registerUserDB(userData=[]):
        global db
        sql = "INSERT INTO telegramData (firstName, userName, language, telegramId, dateLastMessage, dateRegister) " \
              "VALUES (%(firstName)s, %(userName)s, %(language)s, %(telegramId)s, %(dateLastMessage)s, %(dateRegister)s)"

        params = {
            'firstName': userData.first_name,
            'userName': userData.username,
            'language': userData.language_code,
            'telegramId': userData.id,
            'dateLastMessage': method.getNowDate(),
            'dateRegister': method.getNowDate()
        }
        result = db.send.execute(sql, params)
        db.datebase.commit()

    def updateDateLastMessage(self):
        global db
        sql = "UPDATE telegramData SET dateLastMessage = %(newDate)s WHERE telegramId = %(telegramId)s"
        params = {
            'newDate': method.getNowDate(),
            'telegramId': self.telegramId
        }
        try:
            db.send.execute(sql, params)
            db.datebase.commit()
        except Exception:
            del db
            db = DB()
            db.send.execute(sql, params)
            db.datebase.commit()

        self.dateLastMessage = method.getNowDate()

