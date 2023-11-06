import telebot
import main

token = '6728104105:AAGaffrRqVxbOKCT6wetjQDpZWFXmjGtA0s'

bot = telebot.TeleBot(token)



@bot.message_handler(commands=["auth"])
def auth(message): 
    bot.send_message(message.chat.id, "Введите логин")
    bot.register_next_step_handler(message, save_login)


def save_login(message):
    main.user_data['login'] = message.text
    bot.send_message(message.chat.id, "Введите пароль") 
    with open('user_info.json', 'w') as file:
        main.json.dump(main.user_data, file)
    bot.register_next_step_handler(message, save_password)

#Запоминает пароль, входит в систему, парсит группу студента и запоминает
def save_password(message):
    main.user_data['password'] = message.text
    with open('user_info.json', 'w') as file:
        main.json.dump(main.user_data, file)
    student_group = main.find_student_group()
    if student_group != None:
        with open('user_info.json', 'w') as file:
            main.json.dump(student_group, file)
        bot.send_message(message.chat.id, f"Ваша информация сохранена. Вы студент группы {student_group['group']}")
    else:
        bot.send_message(message.chat.id, "Данные введены неправильно. Запустите команду еще раз")

#Показывает информацию группы
@bot.message_handler(commands=["info"])
def show_info(message):
    with open ('user_info.json', 'r') as file:
        info = main.json.load(file)
    bot.send_message(message.chat.id, info['group'])



@bot.message_handler(commands=['schedule'])
def show_schedule(message):
    currenct_url = main.get_personal_url('https://timetable.mirea.ru/api/groups/name/')
    student_schedule = main.parse_schedule_api()
    



bot.polling(none_stop=True)

#bamba.e@edu.mirea.ru
#a8JkFUmW

#sergeeva.u.m@edu.mirea.ru
#SergeevaMike@19