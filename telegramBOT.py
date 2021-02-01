import telebot
import datetime
import parseInvesting
import custom
from telebot import types

config = '1666624885:AAFa62GqMHuWMUbpJALC2gKrbTG6lzmCRMU'

bot = telebot.TeleBot(config)
now = datetime.datetime.now()
method = custom.method()
@bot.message_handler(commands=['start'])
def welcome(message):

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
    nowDate = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    messageList = {
        'close': '🔓 Пока что у меня нет информации, так-как биржа закрыта, подожди немного.. 🔓',
        'weekend': '🔓 Сегодня выходной день, биржа не работает, подожди немного.. 🔓'
    }

    if message.text == '🇷🇺 Российский рынок - сейчас':
        today = datetime.datetime.today()

        if method.in_array(today.weekday(), [5, 6]):
            messageInfo = messageList['close']
        elif nowDate > datetime.datetime(now.year, now.month, now.day, 18, 45) or \
                nowDate < datetime.datetime(now.year, now.month, now.day, 10, 1):

            messageInfo = messageList['close']
        else:

            investing = parseInvesting.ParseInvesting()
            messageInfo = investing.getFullMessageSituation()

    elif message.text == '🇱🇷 Американский рынок - сейчас':
        if method.in_array(datetime.datetime.today().weekday(), [5,6]):
            messageInfo = messageList['weekend']

        elif nowDate > datetime.datetime(now.year, now.month, now.day, 23, 45) or \
                nowDate < datetime.datetime(now.year, now.month, now.day, 17, 30):

            messageInfo = messageList['close']
        # messageInfo = investing.getFullMessageSituation({'type': 'USA'})

    bot.send_message(message.chat.id, messageInfo)

bot.polling(none_stop=True)
