import requests
from bs4 import BeautifulSoup
import custom
import time
import re
import datetime
# -----------------------------
# Class for getting quote data from the site
# (С) 2020 Russia, Kirov - Light3iro
# -----------------------------
method = custom.method()
class ParseInvesting:

    url = str('https://ru.investing.com/')
    HEADERS = dict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    })

    listStocksName = {
        'Сбербанк': {'type': 'Stock', 'code': 'sberbank_rts'},
        'Яндекс': {'type': 'Stock', 'code': 'yandex?cid=102063' },
        'Роснефть': {'type': 'Stock', 'code': 'rosneft_rts' },
        'ГМК Норильский Никель': {'type': 'Stock', 'code': 'gmk-noril-nickel_rts' },
        'Полюс': {'type': 'Stock', 'code': 'polyus-zoloto_rts' },
        'ВТБ': {'type': 'Stock', 'code': 'vtb_rts' },
        'Аэрофлот': {'type': 'Stock', 'code': 'aeroflot' },
        'Магнит': {'type': 'Stock', 'code':  'magnit_rts' },
        'ММВБ': {'type': 'Index', 'code': 'mcx'},
        'S&P 500': {'type': 'Index', 'code': 'us-spx-500-futures'},
        'Нефть Brent': {'type': 'Futures', 'code': 'brent-oil'},
        'Нефть WTI': {'type': 'Futures', 'code': 'crude-oil'},
        'Золото' : {'type': 'Futures', 'code': 'gold'},
        'USD' : {'type': 'Currency', 'code': 'usd-rub'},
    }

    def getResponse(self, url = str()):
        """
        Function for sending a get request to a site
        :param url: link to the site
        :return: object with content
        """
        response = requests.get(url, headers=self.HEADERS)
        return response

    def getListQuotation(self, params = dict({'type': 'russia', 'typeStats': 'equities'})):
        """
        Function for getting quotes by parameters
        :param params: custom parameters in the function
        :return: data about quotes in JSON format
        """
        content = self.getResponse(self.url + f"{params['typeStats']}/{params['type']}")
        arInfo = []

        soup = BeautifulSoup(content.content, 'html.parser')
        tableEquities = soup.find('table', class_='crossRatesTbl')
        listEquities = tableEquities.find('tbody').findAll('tr')

        for stocks in listEquities:
            stockName = stocks.find('td', class_='plusIconTd').find('a').getText()
            stockValue = stocks.findAll('td')[2].getText()
            stockChangeDayPercent = re.sub('%|[+]', '', stocks.findAll('td')[6].getText()).replace(',', '.')
            volume = stocks.findAll('td')[7].getText()

            if not method.empty([stockName, stockValue, stockChangeDayPercent, volume]):
                arInfo.append({
                    'StockName': stockName,
                    'Value': stockValue,
                    'ChangeDayPercent': float(stockChangeDayPercent),
                    'Volume': volume
                })
        return arInfo

    def sortResult(self, arInfo = [], key = str('ChangeDayPercent')):
        sortProcess = True
        while sortProcess:
            sortProcess = False
            for i in range(len(arInfo)-1):
                if arInfo[i][key] < arInfo[i+1][key]:
                    arInfo[i], arInfo[i+1] = arInfo[i+1], arInfo[i]
                    sortProcess = True
        return arInfo

    def getQuotationByCode(self, params = dict()):
        """
        Function for getting a quote by code
        :param params: custom parameters in the function
        :return: data about quotes in JSON format
        """
        content = self.getResponse(self.url + f"{params['type']}/{params['code']}")
        arInfo = []

        soup = BeautifulSoup(content.content, 'html.parser')
        dataBlock = soup.find('div', class_='current-data').find('div', class_='top bold inlineblock')

        name = soup.find('h1', class_='float_lang_base_1 relativeAttr').getText()
        value = dataBlock.find('span', class_='arial_26').getText()
        changeDayPercent = dataBlock.find('span', class_='parentheses').getText()
        changeDayValue = dataBlock.findAll('span', class_='arial_20')[0].getText()

        if not method.empty([name, value, changeDayPercent]):
            arInfo = {
             'Name': name ,
             'Value': value,
             'ChangeDayPercent': changeDayPercent,
             'ChangeDayValue': changeDayValue
            }
        return arInfo

    def getQuotationByName(self, name = str()):
        if method.in_array(name, self.listStocksName):
            stocksData = self.listStocksName[name]
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
            return self.getQuotationByCode(params)

    def getQuotationSP500(self):
        params = {'type': 'StocksFilter?noconstruct=1&smlID=595&sid=&tabletype=price&index_id=166', 'typeStats': 'equities'}
        result = self.getListQuotation(params)
        return result

    def getQuotationsDowJones(self):
        params = {'type': 'americas', 'typeStats': 'equities'}
        result = self.getListQuotation(params)
        return result

    def getQuotationsNasdaq100(self):
        params = {'type': 'StocksFilter?noconstruct=1&smlID=595&sid=&tabletype=price&index_id=20', 'typeStats': 'equities'}
        result = self.getListQuotation(params)
        return result

    def getQuotationsMOEX(self):
        params = {'type': 'StocksFilter?noconstruct=1&smlID=10144&sid=&tabletype=price&index_id=13666', 'typeStats': 'equities'}
        result = self.getListQuotation(params)
        return result

    def getQuotationsRTS(self):
        params = {'type': 'russia', 'typeStats': 'equities'}
        result = self.getListQuotation(params)
        return result


    def getFullMessageSituation(self, params = dict({'type': 'Russia'})):

        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M')
        if params['type'] == 'Russia':
            index = self.getQuotationByName('ММВБ')
            indexName = 'индекс Мосбиржи'
            quotations = self.getQuotationsMOEX()
            listActualStocks = ['Сбербанк', 'Газпром', 'Polymetal', 'ВТБ']

        elif params['type'] == 'USA':
            index = self.getQuotationByName('S&P 500')
            indexName = 'индекс S&P 500'
            quotations = self.getQuotationSP500()
            listActualStocks = ['Apple', 'Microsoft', 'Facebook', 'Tesla']

        messageMoexSituation = "По состоянию на " + nowTime + f", {indexName} снизился на " + index['ChangeDayValue'] + \
                      f" пунктов ({index['ChangeDayPercent']}) и текущее его состояние {index['Value']} пунктов.\n"

        messageTextLeaderFall = "\nЛидеры падения: \n"
        for i in range(0,5):
            stocks = sorted(quotations, key=lambda item: item['ChangeDayPercent'])[i]
            messageTextLeaderFall += stocks['StockName'] + f" - цена {stocks['Value']} руб. ({stocks['ChangeDayPercent']}%).\n"

        messageTextLeaderGrowth = "\nЛидеры роста: \n"
        for i in range(0,5):
            stocks = sorted(quotations, reverse=True, key=lambda item: item['ChangeDayPercent'])[i]
            messageTextLeaderGrowth += stocks['StockName'] + f" - цена {stocks['Value']} руб. ({stocks['ChangeDayPercent']}%).\n"

        messageTextActualCurrent = "\nЦена актуально торгуемых акций: \n"
        for i in range(len(quotations)):
            stocks = quotations[i]
            if method.in_array(stocks['StockName'], listActualStocks):
                messageTextActualCurrent += stocks['StockName'] + f" - цена {stocks['Value']} руб. ({stocks['ChangeDayPercent']}%).\n"

        resultStr = messageMoexSituation + messageTextLeaderFall + messageTextLeaderGrowth + messageTextActualCurrent

        return resultStr



