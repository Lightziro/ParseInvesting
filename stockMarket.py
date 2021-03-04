import datetime


class StockMarket():
    time = datetime.datetime.now()
    workTimeMarket = {
        'RUSSIA': {'WITH': datetime.datetime(time.year, time.month, time.day, 10, 1),
                   'UNTIL': datetime.datetime(time.year, time.month, time.day, 18, 45)
                   },
        'USA': {
            'WITH': datetime.datetime(time.year, time.month, time.day, 17, 30),
            'UNTIL': datetime.datetime(time.year, time.month, time.day, 23, 45)
        },
    }
    buttonMarket = {
                       'USA': '🇱🇷 Американский рынок - сейчас',
                       'RUSSIA': '🇷🇺 Российский рынок - сейчас'
                   }
    currentStockMarket = {
        'USA': ['Apple', 'Microsoft', 'Facebook', 'Tesla'],
        'RUSSIA': ['Сбербанк', 'Газпром', 'Polymetal', 'ВТБ'],
    }

    def __init__(self, typeMarket = None):
        self.typeName = typeMarket
        self.workTime = None
        self.buttonText = None
        self.currentStock = None
        self.workTimeWith = None
        self.workTimeUntil = None
        self.settingsMarket()

    def settingsMarket(self):
        """
        Configuring properties when initializing an object
        """
        self.getMarketWorkTime()
        self.getButtonMarket()
        self.getCurrentStock()

    def getMarketWorkTime(self):
        """
        Assigns the exchange opening time to the object property
        """
        marketTime = self.workTimeMarket[self.typeName]
        self.workTimeWith = marketTime['WITH']
        self.workTimeUntil = marketTime['UNTIL']

    def getCurrentStock(self):
        """
        Assigns the current promotions to the object property
        """
        self.currentStock = self.currentStockMarket[self.typeName]

    def getButtonMarket(self):
        self.buttonText = self.buttonMarket[self.typeName]

