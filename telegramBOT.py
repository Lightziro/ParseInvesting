import telebot
import datetime
from parseInvesting import ParseQuotation
from custom import method
import random
from telebot import types
import stockMarket
import constant
from User import User
import re
import actualIdea
from convertInMessage import ConvertInMessage

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
    btnActualIdea = types.KeyboardButton('🗓 Актуальные идеи')
    btnRussiaSituate = types.KeyboardButton('🇷🇺 Российский рынок - сейчас')
    markup.add(btnUSASituate, btnRussiaSituate, btnActualIdea)

    welcomeMessage += "{0.first_name}.\nЯ - бот, который подскажет тебе всю информацию на " \
                      "фондовом рынке на сегодняшний день".format(message.from_user, bot.get_me())

    bot.send_message(message.chat.id, welcomeMessage, parse_mode='html', reply_markup=markup)
    if User.checkUserDB(message.from_user.id) is False:
        User.registerUserDB(message.from_user)
        user = User(message.from_user.id)


@bot.message_handler(content_types=['text'])
def message(message):

    global user
    if user is None or (getattr(user, 'telegramId') != message.from_user.id):
        user = User(message.from_user.id)
        print(hasattr(user, 'telegramId'))
        if not hasattr(user, 'telegramId'):
            User.registerUserDB(message.from_user)
            user = User(message.from_user.id)
    user.updateDateLastMessage()

    nowTime = datetime.datetime.now()
    marketRussia = stockMarket.StockMarket(typeMarket='RUSSIA')
    marketUSA = stockMarket.StockMarket(typeMarket='USA')
    sendQuestion = bool(False)

    splitMessage = message.text.split()

    if method.in_array(message.text, [marketRussia.buttonText, marketUSA.buttonText]):

        if message.text in marketRussia.buttonText:
            typeMarket = marketRussia
        elif message.text in marketUSA.buttonText:
            typeMarket = marketUSA

        today = datetime.datetime.today()

        if method.in_array(today.weekday(), [5, 6]):
            # if today is a day off
            messageInfo = constant.CLOSE_MARKET

        elif nowTime > typeMarket.workTimeUntil or nowTime < typeMarket.workTimeWith:
            # if the exchange's working hours are over
            messageInfo = constant.CLOSE_MARKET

        else:
            # output information from the exchange
            messageInfo = ConvertInMessage.getFullMessageSituation(typeMarket=typeMarket.typeName, marketObject=typeMarket)

            randQuestion = random.randint(0, 5)
            if randQuestion % 2 != 0:
                # ask a question in 25% of cases about the market situation
                sendQuestion = True
                messageQuestion = 'Как Вам сегодняшняя ситуация на рынке?'
                markClient = types.InlineKeyboardMarkup(row_width=2)
                markClient.add(types.InlineKeyboardButton("👍", callback_data='good'))
                markClient.add(types.InlineKeyboardButton("✊", callback_data='so-so'))
                markClient.add(types.InlineKeyboardButton("👎", callback_data='bad'))

        bot.send_message(message.chat.id, messageInfo)
        if sendQuestion and sendQuestion not in locals():
            bot.send_message(message.chat.id, messageQuestion, reply_markup=markClient)

    if message.text[0] == '!':
        quotationTextMessage = message.text.replace('!', '')
        if method.in_array(quotationTextMessage, ParseQuotation.listStocksName):

            quotationInfo = ParseQuotation.getQuotationByName(quotationTextMessage)
            quotationInfo.update({'Name': quotationTextMessage})

            resultMessage = ConvertInMessage.getInfoMessageQuotation(quotation=quotationInfo)

        else:
            resultMessage = constant.DONT_KNOW_QUOTATION
        bot.send_message(message.chat.id, resultMessage)

    if method.in_array(message.text[0], ['+', '-']):

        quotationName = re.sub('[-]|[+]', '', message.text.replace('+', ''))
        if method.in_array(quotationName, ParseQuotation.listStocksName):
            codeQuotation = ParseQuotation.listStocksName[quotationName]['code']
            if message.text[0] == '+':
                resultAdd = user.addQuotation({'nameQuotation': quotationName, 'codeQuotation': codeQuotation})
                resultMessage = constant.SUCCESS_ADD_IN_CASE
            elif message.text[0] == '-':
                resultDelete = user.removeQuotation({'nameQuotation': quotationName, 'codeQuotation': codeQuotation})

                if resultDelete is False:
                    resultMessage = constant.NOT_QUOTATION_CASE
                else:
                    resultMessage = constant.SUCCESS_DELETE_QUOTATION_IN_CASE

        else:
            resultMessage = constant.DONT_KNOW_QUOTATION

        bot.send_message(message.chat.id, resultMessage, parse_mode='html')


    if message.text.upper() in 'МОИ':

        arQuotationUser = user.getQuotation()
        resultMessage = ConvertInMessage.getInfoMessageUserQuotation(arQuotationUser)
        bot.send_message(message.chat.id, resultMessage)

    if message.text in '🗓 Актуальные идеи':
        listIdea = actualIdea.Idea.GetList()
        messageReturn = ConvertInMessage.convertListIdea(listIdea)
        bot.send_message(message.chat.id, str(messageReturn))




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
