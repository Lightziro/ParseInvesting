from custom import method

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

