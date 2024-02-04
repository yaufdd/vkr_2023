import telebot
from telebot import types

token = '6728104105:AAGaffrRqVxbOKCT6wetjQDpZWFXmjGtA0s'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    #Аавторизация (спросить студент или препод | Сделать авторизацию в мини ап)
    #Сделать авторизацию в мини ап
    #Cпросить студент или препод
    #При авторизации сохраняется информация о расписании в бд
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Авторизация")
    button2 = types.InlineKeyboardButton("Перейти на lk.mirea.ru", url='https://lk.mirea.ru/')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Это Univerbro 👋\n\nАвторизуйся если первый раз\n\nНу или можешь зайти на сайт если нужно", reply_markup=markup)
    


@bot.message_handler(commands=['today'])
def today_schedule(message):
    #Будет показываться расписание на сегодня
    bot.send_message(message.chat.id, 'Today Schedule')


@bot.message_handler(commands=['homework'])
def remember_hw(message):
    #Запоминает какой дз задали по какому предмету
    bot.send_message(message.chat.id, 'Remains homework')


@bot.message_handler(commands=['submit_hw'])
def submit_hw(message):
    #Выгружает в сдо дз на проверку
    bot.send_message(message.chat.id, 'Home was loaded to site')

@bot.message_handler(commands=['gpt'])
def summon_chatgpt(message):
    #Призывает чат гпт 
    bot.send_message(message.chat.id, 'Chat GPT was summoned')


bot.polling(none_stop=True)
