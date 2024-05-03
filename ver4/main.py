import telebot
from telebot import types
from access_lks import user_info, login
from schedule_api import *
from bs4 import BeautifulSoup
import datetime
from postgres_operation import *

token = '6728104105:AAGaffrRqVxbOKCT6wetjQDpZWFXmjGtA0s'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    global tg_id
    tg_id = message.from_user.id
    if not is_user_exists_by_id(tg_id):
        msg = bot.send_message(message.chat.id, "Введите логин")
        bot.register_next_step_handler(msg, process_login_step)
    else:
        bot.send_message(message.chat.id, "Ты здесь не первый раз. Используй команды 😁")
    

def process_login_step(message):
    user_info[tg_id] = {'login' : message.text}
    msg = bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(msg, process_password_step)


def process_password_step(message):
    user_info[tg_id]['password'] = message.text
    bot.send_message(message.chat.id, '😊')
    process_group_step(message)


def process_group_step(message):
    get_group_and_name(message) #saving in dict students name and group
    try:
        user_info[tg_id]['group_uid'] = get_group_uid(user_info[tg_id]['group_name'])
        bot.send_message(message.chat.id, f"Вы {user_info[tg_id]['full_name']} из группы {user_info[tg_id]['group_name']}")
        save_student_in_db(tg_id, 
                        user_info[tg_id]['full_name'], 
                        user_info[tg_id]['group_name'], 
                        user_info[tg_id]['group_uid'], 
                        user_info[tg_id]['login'], 
                        user_info[tg_id]['password'])  #saving all got info in db
        process_subjects_step()
    except KeyError:
        return


def process_subjects_step():
    data = get_group_schedule(user_info[tg_id]['group_uid'])
    subjects = set()
    holidays = set()
    for item in data['data']:
        try:
            current_subject = item['subject']
            current_teacher = item['teachers'][0]['name']
        except IndexError:
            current_teacher = None
        except KeyError:
            holidays.add(item['title'])
        subjects.add((current_subject, current_teacher))
    for item in subjects:
        save_subject_of_student_in_db(item[0], item[1], tg_id)


@bot.message_handler(commands=['today'])
def show_today_schedule(message):
    tg_id = message.from_user.id
    if is_user_exists_by_id(tg_id):
        try:
            current_uid = get_group_uid_by_tg_id(tg_id)
            data = get_group_schedule(current_uid)
            today_date = datetime.datetime.now().strftime('%d-%m-%Y')
            #today_date = '22-03-2024'
            matching_items = []
            for item in data['data']:
                if today_date in item['dates']:
                    matching_items.append(item)
            if len(matching_items) != 0:
                bot.send_message(message.chat.id, "И так сегодня у нас")
                for item in matching_items:
                    subject = item['subject']
                    lesson_type = item['lesson_type']
                    if lesson_type == "practice":
                        lesson_type = "пр"
                    elif lesson_type == "lecture":
                        lesson_type = "лек"
                    teacher = item['teachers'][0]['name']
                    classroom = item['classrooms'][0]['name']
                    campus = item['classrooms'][0]['campus']['name']
                    start_time = item['lesson_bells']['start_time']
                    end_time = item['lesson_bells']['end_time']
                    bot.send_message(message.chat.id, f"{subject} ({lesson_type})\n{start_time}~{end_time}\nКабинет {classroom} ({campus})\nПреподаватель: {teacher}")
            else:
                bot.send_message(message.chat.id, "Сегодня нет пар")
        except Exception as e:
            print(e)
    else:
        bot.send_message(message.chat.id, "Пока не знаю кто ты нажима сначала /start")


@bot.message_handler(commands=['see_homework'])
def see_homework(message):
    print(message.from_user.id)
    homework_list = get_homeworks_from_db(message.from_user.id)
    subject_dict = {}
    for content, deadline, subject in homework_list:
        if subject not in subject_dict:
            subject_dict[subject] = []
        subject_dict[subject].append((content, deadline))
    
    response_message = ""
    for subject, tasks in subject_dict.items():
        response_message += f"<b>{subject.upper()}</b>\n"
        for content, deadline in tasks:
            formatted_date = deadline.strftime("%d.%m.%Y")
            response_message += f"{content} до {formatted_date}\n"
        response_message += "\n"

    bot.send_message(message.chat.id, response_message, parse_mode='HTML')


import hashlib
user_state = {}
@bot.message_handler(commands=['homework'])
def save_homework(message):
    tg_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    semester_student_subjects = []
    semester_student_subjects = get_subjects_of_student_by_tg_id(tg_id)
    for subject_tuple in semester_student_subjects:
        subject = subject_tuple[0]
        subject_hash = hashlib.md5(subject.encode()).hexdigest()[:10]
        button = types.InlineKeyboardButton(f"{subject}", callback_data=subject_hash)
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)
    user_state[tg_id] = 'waiting_homework_content'

@bot.callback_query_handler(func=lambda call: user_state[call.from_user.id] == 'waiting_homework_content')
def callback_query(call):
    tg_id = call.from_user.id
    semester_student_subjects = []
    semester_student_subjects = get_subjects_of_student_by_tg_id(tg_id)
    global subject_hm
    for subjec_tuple in semester_student_subjects:
        subject_hm = subjec_tuple[0]
        subject_hash = hashlib.md5(subject_hm.encode()).hexdigest()[:10]
        if call.data == subject_hash:
            global selected_subject_hm
            selected_subject_hm = subject_hm
            bot.send_message(call.message.chat.id, f'Введите домашнее задание для:\n <b>"{subject_hm}"</b>', parse_mode='HTML')

@bot.message_handler(func=lambda message: user_state[message.chat.id] == 'waiting_homework_content')
def homework_saver(message):
    global homework_content
    homework_content = message.text
    user_state[message.from_user.id] = 'waiting_homework_deadline'
    bot.send_message(message.chat.id, f'Отправьте последний день сдачи\n(ГГГГ-ММ-ДД)')

@bot.message_handler(func=lambda message: user_state[message.chat.id] == 'waiting_homework_deadline')
def homework_deadline_saver(message):
    save_homework_in_db(homework_content, message.text, selected_subject_hm)








def get_group_and_name(message):
    login_responce = login(user_info[tg_id]['login'], user_info[tg_id]['password'])
    if login_responce:
        try:
            soup =  BeautifulSoup(login_responce.text, 'html.parser')
            student_find_divs = soup.find_all(class_='student-personal-info')
            for div in student_find_divs:
                second_div = div.find_all('div')[0]

                span = second_div.find('span')
                if span :
                    full_name = span.text.strip()
                    user_info[tg_id]['full_name'] = full_name 
            soup =  BeautifulSoup(login_responce.text, 'html.parser')
            group_table = soup.find_all('table')[0]

            elements_in_gourp_table = group_table.find_all('td')
            
            student_gourp = elements_in_gourp_table[4]
            user_info[tg_id]['group_name'] = student_gourp.text
            return user_info
        except:
            bot.send_message(message.chat.id, "Неправильно введен пароль\nЕсли уверены что правильно обратитесь в поддержку /help")
    else:
        bot.send_message("Ошибка в соединении, проверить подключение к интнернуте или выключите VPN")
        return




def make_subject_inline(cur_tg_id):
    markup = types.InlineKeyboardMarkup()
    semester_student_subjects = []
    semester_student_subjects = get_subjects_of_student_by_tg_id(cur_tg_id)
    for subject_tuple in semester_student_subjects:
        subject = subject_tuple[0]
        subject_hash = hashlib.md5(subject.encode()).hexdigest()[:10]
        button = types.InlineKeyboardButton(f"{subject}", callback_data=subject_hash)
        markup.add(button)
    return markup





bot.polling(non_stop=True)
#bamba.e@edu.mirea.ru
#a8JkFUmW