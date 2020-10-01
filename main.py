import telebot
from telebot import types

from currency_exchange.logics import Currency

bot = telebot.TeleBot('1239503641:AAGMPTQq1R1vW5bQZCi7ERzxHu5nJn3sMF4')

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Переглянути всі курси(відносно грн)', 'Продати валюту', 'Купити валюту')
cur = Currency()
to_sell = ""
to_buy = ""


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт, знизу обери бажану дію', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'переглянути всі курси(відносно грн)':
        Rates = cur.get_all_rates()
        msg = ""
        for x in Rates:
            c = str(cur.get_currency_rate(x, "uah"))
            if (len(msg) >= 4000):
                bot.send_message(message.chat.id, msg)
                msg = ""
            msg += "1 " + x + " = " + c + " UAH" + '\n'
        bot.send_message(message.chat.id, msg)
    elif message.text.lower() == 'продати валюту':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'купити валюту':
        send = bot.send_message(message.chat.id, 'Введіть абревіатуру валюти продажу')
        bot.register_next_step_handler(send, buy_bot)
    else:
        bot.send_message(message.chat.id, 'я тебе не розумію, обери дію, перелік нижче', reply_markup=keyboard1)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBZahfdG4OH1sG5g5ESnK8mjN0tsu0MgACEwADwDZPE6qzh_d_OMqlGwQ')


def buy_bot(message):
    global to_sell
    to_sell = message.text.upper()
    send = bot.send_message(message.chat.id, 'Введіть абревіатуру валюти купівлі')
    bot.register_next_step_handler(send, get_sell_)


def get_sell_(message):
    global to_buy
    to_buy = message.text.upper()
    send = bot.send_message(message.chat.id, 'Введіть суму')
    bot.register_next_step_handler(send, get_sum_by_selling)


def get_sum_by_selling(message):
    cost = float(int(message.text))
    print(to_sell)
    print(to_buy)
    print(cost)
    new_cost = cur.currency_cost_to_buy(to_sell, to_buy, cost)
    bot.send_message(message.chat.id, 'Сума купівлі - ' + new_cost + ' ' + to_buy.upper())


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


bot.polling()
