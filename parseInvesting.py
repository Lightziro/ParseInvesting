from bs4 import BeautifulSoup
import datetime
from custom import method
from custom import Request
from stockMarket import StockMarket


# -----------------------------
# Class for getting quote data from the site
# (С) 2020 Russia, Kirov - Light3iro
# -----------------------------
class ParseQuotation:
    url = str('https://ru.investing.com/')

    listStocksName = {
        'Сбербанк': {'type': 'Stock', 'code': 'sberbank_rts'},
        'Яндекс': {'type': 'Stock', 'code': 'yandex?cid=102063'},
        'Роснефть': {'type': 'Stock', 'code': 'rosneft_rts'},
        'ГМК Норильский Никель': {'type': 'Stock', 'code': 'gmk-noril-nickel_rts'},
        'Полюс': {'type': 'Stock', 'code': 'polyus-zoloto_rts'},
        'Транснефть': {'type': 'Stock', 'code': 'transneft-p_rts'},
        'Газпром': {'type': 'Stock', 'code': 'gazprom_rts'},
        'Лукойл': {'type': 'Stock', 'code': 'lukoil_rts'},
        'ВТБ': {'type': 'Stock', 'code': 'vtb_rts'},
        'Аэрофлот': {'type': 'Stock', 'code': 'aeroflot'},
        'Магнит': {'type': 'Stock', 'code': 'magnit_rts'},
        'Coca Cola': {'type': 'Stock', 'code': 'coca-cola-co'},
        'Nike': {'type': 'Stock', 'code': 'nike'},
        'Walt Disney': {'type': 'Stock', 'code': 'disney'},
        'НОВАТЭК': {'type': 'Stock', 'code': 'novatek_rts'},
        'МТС': {'type': 'Stock', 'code': 'mts_rts'},
        'РУСАЛ': {'type': 'Stock', 'code': 'united-company-rusal-plc%60'},
        'Северсталь': {'type': 'Stock', 'code': 'severstal_rts'},
        'Татнефть': {'type': 'Stock', 'code': 'tatneft_rts'},
        'Интер РАО': {'type': 'Stock', 'code': 'inter-rao-ees_mm'},


        'ММВБ': {'type': 'Index', 'code': 'mcx'},
        'S&P 500': {'type': 'Index', 'code': 'us-spx-500-futures'},

        'Нефть Brent': {'type': 'Futures', 'code': 'brent-oil'},
        'Нефть WTI': {'type': 'Futures', 'code': 'crude-oil'},
        'Золото': {'type': 'Futures', 'code': 'gold'},

        'USD': {'type': 'Currency', 'code': 'usd-rub'},
    }

    @classmethod
    def getListQuotation(cls, params=dict({'type': 'russia', 'typeStats': 'equities'})):
        """
        Function for getting quotes by parameters
        :param params: custom parameters in the function
        :return: data about quotes in JSON format
        """
        content = Request.getResponse(cls.url + f"{params['typeStats']}/{params['type']}")
        arInfo = []

        soup = BeautifulSoup(content.content, 'html.parser')
        tableEquities = soup.find('table', class_='crossRatesTbl')
        listEquities = tableEquities.find('tbody').findAll('tr')

        for stocks in listEquities:
            stockName = stocks.find('td', class_='plusIconTd').find('a').getText()
            stockValue = method.convertToFloat(stocks.findAll('td')[2].getText())
            stockChangeDayPercent = method.convertToFloat(stocks.findAll('td')[6].getText())
            volume = method.convertToFloat(stocks.findAll('td')[7].getText())

            if not method.empty([stockName, stockValue, stockChangeDayPercent, volume]):
                arInfo.append({
                    'StockName': stockName,
                    'Value': stockValue,
                    'ChangeDayPercent': float(stockChangeDayPercent),
                    'Volume': volume
                })
        return arInfo

    # def sortResult(self, arInfo = [], key = str('ChangeDayPercent')):
    #     sortProcess = True
    #     while sortProcess:
    #         sortProcess = False
    #         for i in range(len(arInfo)-1):
    #             if arInfo[i][key] < arInfo[i+1][key]:
    #                 arInfo[i], arInfo[i+1] = arInfo[i+1], arInfo[i]
    #                 sortProcess = True
    #     return arInfo

    @classmethod
    def getQuotationByCode(cls, params=dict()):
        """
        Function for getting a quote by code
        :param params: custom parameters in the function
        :return: data about quotes in JSON format
        """
        content = Request.getResponse(cls.url + f"{params['type']}/{params['code']}")
        arInfo = []

        soup = BeautifulSoup(content.content, 'html.parser')
        dataBlock = soup.find('div', class_='current-data').find('div', class_='top bold inlineblock')

        name = soup.find('h1', class_='float_lang_base_1 relativeAttr').getText()
        value = method.convertToFloat(dataBlock.find('span', class_='arial_26').getText())
        changeDayPercent = method.convertToFloat(dataBlock.find('span', class_='parentheses').getText())
        changeDayValue = method.convertToFloat(dataBlock.findAll('span', class_='arial_20')[0].getText())

        if not method.empty([name, value, changeDayPercent]):
            arInfo = {
                'Name': name,
                'Value': value,
                'ChangeDayPercent': changeDayPercent,
                'ChangeDayValue': changeDayValue
            }
        return arInfo

    @classmethod
    def getQuotationByName(cls, name=str()):
        if method.in_array(name, cls.listStocksName):
            stocksData = cls.listStocksName[name]
            stocksCode = stocksData['code']

            if stocksData['type'] == 'Index':
                params = {'type': 'indices'}
            elif stocksData['type'] == 'Stock':
                params = {'type': 'equities'}
            elif stocksData['type'] == 'Futures':
                params = {'type': 'commodities'}
            elif stocksData['type'] == 'Currency':
                params = {'type': 'currencies'}

            params.update({'code': stocksCode})
            return cls.getQuotationByCode(params)

    @classmethod
    def getQuotationSP500(cls):
        params = {'type': 'StocksFilter?noconstruct=1&smlID=595&sid=&tabletype=price&index_id=166',
                  'typeStats': 'equities'}
        result = cls.getListQuotation(params)
        return result

    @classmethod
    def getQuotationsDowJones(cls):
        params = {'type': 'americas', 'typeStats': 'equities'}
        result = cls.getListQuotation(params)
        return result

    @classmethod
    def getQuotationsNasdaq100(cls):
        params = {'type': 'StocksFilter?noconstruct=1&smlID=595&sid=&tabletype=price&index_id=20',
                  'typeStats': 'equities'}
        result = cls.getListQuotation(params)
        return result

    @classmethod
    def getQuotationsMOEX(cls):
        params = {'type': 'StocksFilter?noconstruct=1&smlID=10144&sid=&tabletype=price&index_id=13666',
                  'typeStats': 'equities'}
        result = cls.getListQuotation(params)
        return result

    @classmethod
    def getQuotationsRTS(cls):
        params = {'type': 'russia', 'typeStats': 'equities'}
        result = cls.getListQuotation(params)
        return result

