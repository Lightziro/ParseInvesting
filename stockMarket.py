import datetime

class stockMarket:

    time = datetime.datetime.now()
    typeMarket = []

    ruMarket = {
        'textButton': '🇷🇺 Российский рынок - сейчас',
        'workTime': {
            'workWith': datetime.datetime(time.year, time.month, time.day, 10, 1),
            'workUntil': datetime.datetime(time.year, time.month, time.day, 18, 45),
        },
        'typeName': 'Russia',
        'currentStock': ['Сбербанк', 'Газпром', 'Polymetal', 'ВТБ']
    }
    usMarket = {
        'textButton': '🇱🇷 Американский рынок - сейчас',
        'workTime': {
            'workWith': datetime.datetime(time.year, time.month, time.day, 17, 30),
            'workUntil': datetime.datetime(time.year, time.month, time.day, 23, 45),
        },
        'typeName': 'USA',
        'currentStock': ['Apple', 'Microsoft', 'Facebook', 'Tesla']
    }

    def __init__(self):
        self.typeMarket = [self.ruMarket, self.usMarket]
