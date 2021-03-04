from custom import method
from parseInvesting import ParseQuotation
import datetime

class ConvertInMessage:

    @staticmethod
    def convertListIdea(arListIdea = dict):
        message = 'Актуальные идеи на сегодняшний день: \n'

        for idea in arListIdea:
            typeIdea = 'Продажа' if (float(idea['PRICE_SELL']) - float(idea['PRICE_BUY']) < 0) else 'Покупка'
            typeSmile = '📉' if typeIdea in 'Продажа' else '📈'

            message += f'{typeSmile} Идея: {typeIdea} акции {idea["NAME"]} {typeSmile} \n'

            if typeIdea in 'Покупка':
                message += f'       💰Цена покупки: {idea["PRICE_BUY"]};\n'
                message += f'       💰Цена продажи: {idea["PRICE_SELL"]};\n'
            else:
                message += f'       💰Цена продажи: {idea["PRICE_BUY"]};\n'
                message += f'       💰Цена покупки: {idea["PRICE_CELL"]};\n'
            message += f'       💸Потенциальная доходность: {idea["INCOME"]}%;\n'
            message += f'       💵Цена на момент создания идеи: {idea["PRICE_RELEASE"]};\n'
            message += f'       📅Дата создания идеи: {idea["DATE_CREATE"]};\n\n'

        return message

    @staticmethod
    def getInfoMessageQuotation(quotation = None):
        """
        Getting information about quote for Telegram bot
        :param quotation: Quote Information
        :return: Message string
        """

        typeStatusText = 'снижается' if quotation['ChangeDayPercent'] < 0 else 'растёт'

        messageTextInfo = 'По моим данным ' + quotation['Name'] + ' сейчас котируется на уровне ' + \
                          str(quotation[
                                  'Value']) + f' {method.getTextByCount(int(quotation["Value"]), ["пункт", "пункта", "пунктов"])}' + \
                          ', и на текущий момент ' + typeStatusText + ' на ' + str(quotation['ChangeDayValue']) + \
                          ' пункта (' + str(quotation["ChangeDayPercent"]) + '%)'

        return messageTextInfo

    @staticmethod
    def getFullMessageSituation(typeMarket = None, marketObject = None):
        """
        Getting information about the quotes of a certain market for the telegram bot
        :param typeMarket: Market type, RUSSIA or USA
        :param marketObject: Market object
        :return: Message string
        """

        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M')

        if typeMarket == 'RUSSIA':
            index = ParseQuotation.getQuotationByName('ММВБ')
            indexName = 'индекс Мосбиржи'
            quotations = ParseQuotation.getQuotationsMOEX()

        elif typeMarket == 'USA':
            index = ParseQuotation.getQuotationByName('S&P 500')
            indexName = 'индекс S&P 500'
            quotations = ParseQuotation.getQuotationSP500()
        market = marketObject

        typeStatusText = 'снижается' if index['ChangeDayValue'] < 0 else 'растёт'

        messageMoexSituation = "По состоянию на " + nowTime + f", {indexName} {typeStatusText} на " + str(index['ChangeDayValue']) + \
                               f" пунктов ({str(index['ChangeDayPercent'])}%) и текущее его состояние {str(index['Value'])} пунктов.\n"

        messageTextLeaderFall = "\nЛидеры падения: \n"
        for i in range(0, 5):
            stocks = sorted(quotations, key=lambda item: item['ChangeDayPercent'])[i]
            messageTextLeaderFall += stocks[
                                         'StockName'] + f" - цена {str(stocks['Value'])} руб. ({str(stocks['ChangeDayPercent'])}%).\n"

        messageTextLeaderGrowth = "\nЛидеры роста: \n"
        for i in range(0, 5):
            stocks = sorted(quotations, reverse=True, key=lambda item: item['ChangeDayPercent'])[i]
            messageTextLeaderGrowth += stocks[
                                           'StockName'] + f" - цена {str(stocks['Value'])} руб. ({str(stocks['ChangeDayPercent'])}%).\n"

        messageTextActualCurrent = "\nЦена актуально торгуемых акций: \n"
        for i in range(len(quotations)):
            stocks = quotations[i]
            if method.in_array(stocks['StockName'], market.currentStock):
                messageTextActualCurrent += stocks[
                                                'StockName'] + f" - цена {str(stocks['Value'])} руб. ({str(stocks['ChangeDayPercent'])}%).\n"

        resultStr = messageMoexSituation + messageTextLeaderFall + messageTextLeaderGrowth + messageTextActualCurrent

        return resultStr

