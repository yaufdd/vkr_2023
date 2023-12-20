import telebot
import main
import connectdb
from datetime import datetime

token = '6728104105:AAGaffrRqVxbOKCT6wetjQDpZWFXmjGtA0s'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["auth"])
def auth(message): 
    bot.send_message(message.chat.id, "Введите логин")
    bot.register_next_step_handler(message, save_login)


def save_login(message):
    main.user_data['login'] = message.text
    bot.send_message(message.chat.id, "Введите пароль") 
    bot.register_next_step_handler(message, save_password)

#Запоминает пароль, входит в систему, парсит группу студента и запоминает
#Так же сразу же сохраняет расписние в базу
def save_password(message):
    main.user_data['password'] = message.text
    student_name = main.find_student_name()['name']
    group = main.find_student_group()['group']
    login = main.user_data['login']
    password = main.user_data['password']
    main.user_data['tg_id'] = message.from_user.id
    if group != None:
        bot.send_message(message.chat.id, f"Ваша информация сохранена. \nВы {student_name} из группы {group}")
    else:
        bot.send_message(message.chat.id, "Данные введены неправильно. Запустите команду еще раз")
    connectdb.save_student_todb(student_name, group, login, password, message.from_user.id)
    main.save_schedule("https://timetable.mirea.ru/api/groups/name/")
    

#Показывает информацию группы
@bot.message_handler(commands=["info"])
def show_info(message):
    bot.send_message(message.chat.id, main.user_data['group'])


def send_formatted_schedule(schedule):
    message = "<b>Расписание на сегодня:</b>\n"
    for item in schedule:
        message += (
            f"📚 <i>{item[0]}</i> ({item[1]})\n"
            f"👤 Преподаватель: {item[2]}\n"
            f"📍 Аудитория: {item[3]}, {item[4]}\n\n"
            "────────────────────\n" 
        )
    return message

@bot.message_handler(commands=['today_schedule'])
def show_todaySchedule(message):
    isEven, td_weekday = main.week_evenOrNot(datetime.today())
    today_sche = connectdb.get_todaySchedule(isEven, td_weekday + 4, message.from_user.id)
    
    if today_sche:
        formatted_message = send_formatted_schedule(today_sche)
        bot.send_message(message.chat.id, formatted_message, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "На сегодня расписания нет.", parse_mode='HTML')
    print(today_sche)


bot.polling(none_stop=True)

#bamba.e@edu.mirea.ru
#a8JkFUmW

#sergeeva.u.m@edu.mirea.ru
#SergeevaMike@19