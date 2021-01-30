import requests
from bs4 import BeautifulSoup
import method
import time
# -----------------------------
# Class for getting quote data from the site
# (С) 2020 Russia, Kirov - Light3iro
# -----------------------------
class ParseInvesting:

    url = str('https://ru.investing.com/')
    HEADERS = dict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    })

    # / Function for sending a get request to a site / #
    # / @params string url - link to the site / #
    # / @return object response - object with content / #
    def getResponse(self, url = str()):
        response = requests.get(url, headers=self.HEADERS)
        return response

    # / Function for getting quotes by parameters / #
    # / @params dict params - custom parameters in the function / #
    # / @return dict arRussiaStocks - data about quotes in JSON format / #
    def getQuotation(self, params = dict({'type': 'russia', 'typeStats': 'equities'})):
        content = self.getResponse(self.url + f"{params['typeStats']}/{params['type']}")
        arRussiaStocks = []

        soup = BeautifulSoup(content.content, 'html.parser')
        tableEquities = soup.find('table', class_='crossRatesTbl')
        listEquities = tableEquities.find('tbody').findAll('tr')

        for stocks in listEquities:
            stockName = stocks.find('td', class_='plusIconTd').find('a').getText()
            stockValue = stocks.findAll('td')[2].getText()
            stockChangeDayPercent = stocks.findAll('td')[6].getText()

            if not method.empty([stockName, stockValue, stockChangeDayPercent]):
                arRussiaStocks.append({
                    'StockName': stockName,
                    'Value': stockValue,
                    'ChangeDayPercent': stockChangeDayPercent
                })
        return arRussiaStocks






