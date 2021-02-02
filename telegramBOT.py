import telebot
import datetime
import parseInvesting
import custom
from telebot import types

config = '1666624885:AAFa62GqMHuWMUbpJALC2gKrbTG6lzmCRMU'

bot = telebot.TeleBot(config)
method = custom.method()
@bot.message_handler(commands=['start'])
def welcome(message):
    now = datetime.datetime.now()
    if now.hour >= 10 and now.hour < 17:
        welcomeMessage = 'Доброго дня, '
    elif now.hour >= 17 and now.hour < 23:
        welcomeMessage = 'Доброго вечера, '
    elif now.hour >= 23 or now.hour < 5:
        welcomeMessage = 'Доброй ночи, '
    else:
        welcomeMessage = 'Доброго утра, '

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnUSASituate = types.KeyboardButton('🇱🇷 Американский рынок - сейчас')
    btnRussiaSituate = types.KeyboardButton('🇷🇺 Российский рынок - сейчас')

    markup.add(btnUSASituate, btnRussiaSituate)

    bot.send_message(message.chat.id,
                     welcomeMessage + "{0.first_name} {0.last_name}.\nЯ - бот, который подскажет тебе всю информацию на "
                                      "фондовом рынке на сегодняшний день".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message(message):
    investing = parseInvesting.ParseInvesting()
    nowTime = datetime.datetime.now()
    print([nowTime, nowTime])
    messageList = {
        'close': '🔓 Пока что у меня нет информации, так-как биржа закрыта, подожди немного.. 🔓',
        'weekend': '🔓 Сегодня выходной день, биржа не работает, подожди немного.. 🔓'
    }

    if message.text == '🇷🇺 Российский рынок - сейчас':
        today = datetime.datetime.today()

        if method.in_array(today.weekday(), [5, 6]):
            messageInfo = messageList['close']
        elif nowTime > datetime.datetime(nowTime.year, nowTime.month, nowTime.day, 19, 15) or \
                nowTime < datetime.datetime(nowTime.year, nowTime.month, nowTime.day, 10, 1):

            messageInfo = messageList['close']
        else:

            investing = parseInvesting.ParseInvesting()
            messageInfo = investing.getFullMessageSituation()

    elif message.text == '🇱🇷 Американский рынок - сейчас':
        if method.in_array(datetime.datetime.today().weekday(), [5,6]):
            messageInfo = messageList['weekend']

        elif nowTime > datetime.datetime(nowTime.year, nowTime.month, nowTime.day, 23, 45) or \
                nowTime < datetime.datetime(nowTime.year, nowTime.month, nowTime.day, 17, 30):

            messageInfo = messageList['close']
        else:
            messageInfo = investing.getFullMessageSituation({'type': 'USA'})

    bot.send_message(message.chat.id, messageInfo)

bot.polling(none_stop=True)
