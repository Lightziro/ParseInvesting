import telebot
import datetime
from parseInvesting import ParseQuotation
from custom import method
import random
from telebot import types
import stockMarket
from User import User
import re

config = '1666624885:AAFa62GqMHuWMUbpJALC2gKrbTG6lzmCRMU'
bot = telebot.TeleBot(config)

user = None

@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Function greeting the user at start
    :param message: Message Data
    :return:
    """
    global user
    # Calculating time of day
    now = datetime.datetime.now()
    if now.hour >= 10 and now.hour < 17:
        welcomeMessage = 'Доброго дня, '
    elif now.hour >= 17 and now.hour < 23:
        welcomeMessage = 'Доброго вечера, '
    elif now.hour >= 23 or now.hour < 5:
        welcomeMessage = 'Доброй ночи, '
    else:
        welcomeMessage = 'Доброго утра, '

    # Creating buttons on keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnUSASituate = types.KeyboardButton('🇱🇷 Американский рынок - сейчас')
    btnActualIdea = types.KeyboardButton('🇱🇷 Актуальные идеи')
    btnRussiaSituate = types.KeyboardButton('🇷🇺 Российский рынок - сейчас')
    markup.add(btnUSASituate, btnRussiaSituate, btnActualIdea)

    welcomeMessage += "{0.first_name} {0.last_name}.\nЯ - бот, который подскажет тебе всю информацию на " \
                      "фондовом рынке на сегодняшний день".format(message.from_user, bot.get_me())

    bot.send_message(message.chat.id, welcomeMessage, parse_mode='html', reply_markup=markup)
    if User.checkUserDB(message.from_user.id) is False:
        User.registerUserDB(message.from_user)
        user = User(message.from_user.id)


@bot.message_handler(content_types=['text'])
def message(message):

    global user
    if user is None:
        user = User(message.from_user.id)
    user.updateDateLastMessage()

    nowTime = datetime.datetime.now()
    market = stockMarket.stockMarket()
    sendQuestion = bool(False)

    messageList = {
        'close': '🔓 Пока что у меня нет информации, так-как биржа закрыта, подожди немного.. 🔓',
        'weekend': '🔓 Сегодня выходной день, биржа не работает, подожди немного.. 🔓',
        'dontKnow': '📊К сожалению в моём списке пока нет информации про этот котирующий инструмент📊',
        'successDelete': '❌Инструмент торговли удален из вашего портфеля❌',
        'errorDelete': 'Невозможно удалить данный инструмент торговли, так-как его нет в вашем портфеле',
        'successAdd': '✅Инструмент торговли добавлен к вам в портфель, чтобы отследить его напишите "Мои"✅'
    }
    splitMessage = message.text.split()

    if method.in_array(message.text, [market.ruMarket['textButton'], market.usMarket['textButton']]):

        typeMarket = market.ruMarket if message.text == market.ruMarket['textButton'] else market.usMarket

        today = datetime.datetime.today()

        if method.in_array(today.weekday(), [5, 6]):
            # if today is a day off
            messageInfo = messageList['close']

        elif nowTime > typeMarket['workTime']['workUntil'] or nowTime < typeMarket['workTime']['workWith']:
            # if the exchange's working hours are over
            messageInfo = messageList['close']

        else:
            # output information from the exchange
            messageInfo = ParseQuotation.getFullMessageSituation({'type': typeMarket['typeName']})

            randQuestion = random.randint(0, 5)
            if randQuestion % 2 != 0:
                sendQuestion = True
                messageQuestion = 'Как Вам сегодняшняя ситуация на рынке?'
                markClient = types.InlineKeyboardMarkup(row_width=2)
                goodBtn = types.InlineKeyboardButton("👍", callback_data='good')
                sosoBtn = types.InlineKeyboardButton("✊", callback_data='so-so')
                badBtn = types.InlineKeyboardButton("👎", callback_data='bad')
                markClient.add(goodBtn, sosoBtn, badBtn)

        bot.send_message(message.chat.id, messageInfo)
        if sendQuestion and sendQuestion not in locals():
            bot.send_message(message.chat.id, messageQuestion, reply_markup=markClient)

    if message.text[0] == '!':
        quotationTextMessage = message.text.replace('!', '')
        if method.in_array(quotationTextMessage, ParseQuotation.listStocksName):

            quotationInfo = ParseQuotation.getQuotationByName(quotationTextMessage)
            quotationInfo.update({'Name': quotationTextMessage})

            resultMessage = ParseQuotation.getInfoMessageQuotation(quotationInfo)

        else:
            resultMessage = messageList['dontKnow']
        bot.send_message(message.chat.id, resultMessage)

    if method.in_array(message.text[0], ['+', '-']):

        quotationName = re.sub('[-]|[+]', '', message.text.replace('+', ''))
        if method.in_array(quotationName, ParseQuotation.listStocksName):
            codeQuotation = ParseQuotation.listStocksName[quotationName]['code']
            if message.text[0] == '+':
                resultAdd = user.addQuotation({'nameQuotation': quotationName, 'codeQuotation': codeQuotation})
                resultMessage = messageList['successAdd']
            elif message.text[0] == '-':
                resultDelete = user.removeQuotation({'nameQuotation': quotationName, 'codeQuotation': codeQuotation})

                if resultDelete is False:
                    resultMessage = messageList['errorDelete']
                else:
                    resultMessage = messageList['successDelete']

        else:
            resultMessage = messageList['dontKnow']

        bot.send_message(message.chat.id, resultMessage, parse_mode='html')


    if method.in_array(message.text, ['мои', 'Мои', 'МОИ']):

        arQuotationUser = user.getQuotation()
        resultMessage = ParseQuotation.getInfoMessageUserQuotation(arQuotationUser)
        bot.send_message(message.chat.id, resultMessage)




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if method.in_array(call.data, ['good', 'so-so', 'bad']):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="📕Спасибо за ваш отзыв!📕", reply_markup=None)

    except Exception as e:
        print(repr(e))



bot.polling(none_stop=True)
