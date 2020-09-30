import telebot

from currency_exchange.logics import Currency

bot = telebot.TeleBot('1239503641:AAGMPTQq1R1vW5bQZCi7ERzxHu5nJn3sMF4')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(commands=['rates'])
def show_all_rates():
    bot.send_message(Currency.get_all_rates())

bot.polling()
