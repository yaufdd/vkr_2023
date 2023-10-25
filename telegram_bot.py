import telebot
import main

token = '6728104105:AAGaffrRqVxbOKCT6wetjQDpZWFXmjGtA0s'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['my_info'])  
def get_stundent_login(message):
    bot.send_message(message.chat.id, "Введите ваш логин: ")
    login = message.text


bot.polling(non_stop=True)

