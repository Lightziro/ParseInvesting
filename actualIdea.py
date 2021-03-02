from DB import DB

class Idea():

    TABLE_NAME = 'ActualStock'
    lastError = ''

    @classmethod
    def GetList(cls, arParams = dict()):

        db = DB()
        arList = []
        sql = f'SELECT name, code, priceRelease, priceBuy, priceSell, income, dateCreate, dateClose FROM {cls.TABLE_NAME}'
        try:
            db.send(sql)
        except:
            del db
            db = DB()
            db.send.execute(sql)
        for (name, code, priceRelease, priceBuy, priceSell, income, dateCreate, dateClose) in db.send:
            arList.append({
                'NAME': name,
                'CODE': code,
                'PRICE_RELEASE': float(priceRelease),
                'PRICE_BUY': float(priceBuy),
                'PRICE_SELL': float(priceSell),
                'INCOME': float(income),
                'DATE_CREATE': dateCreate,
                'DATE_CLOSE': dateClose,
            })
        return arList