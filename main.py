import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
from datetime import datetime
import psycopg2

session = requests.Session()

conn = psycopg2.connect(
    dbname='telegramBot_vkr',
    user='ericozavr2002',
    password='postgres',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

cur.execute("SELECT * FROM students")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()

def authorization():
    with open('user_info.json', 'r') as file:
        info = json.load(file)

    login_url = 'https://lk.mirea.ru/auth.php'

    login_data = {
        'AUTH_FORM' : 'Y',
        'TYPE' : 'AUTH',
        'USER_LOGIN' : info['login'],
        'USER_PASSWORD' : info['password'],
        'USER_REMEMBER' : 'Y'
    }
    login_responce = session.post(login_url, data=login_data)
    
    return login_responce
    

user_data = {} 

#Ищет группу студента и запоминает его в словаь
def find_student_group():
    try:
        login_responce = authorization()
        soup =  BeautifulSoup(login_responce.text, 'html.parser')
        group_table = soup.find_all('table')[0]

        elements_in_gourp_table = group_table.find_all('td')
        
        student_gourp = elements_in_gourp_table[4]
        user_data['group'] = student_gourp.text
        return user_data
    except IndexError:
        return 

#Создает специальную ссылку для студента
def get_personal_url(url):
    with open('user_info.json', 'r') as file:
        student_group = json.load(file)
    personal_url = url + quote(student_group['group'], encoding='utf-8')
    return personal_url



def detect_weekday(n): 
    if n == 1: 
        return 'Monday'
    if n == 2: 
        return 'Tuesday'
    if n == 3: 
        return 'Wednesday'
    if n == 4: 
        return 'Thursday'
    if n == 5: 
        return 'Friday'
    if n == 6:
        return 'Saturday'
    return 'Unknown'

def detect_subject_number(n):
    if n == "09:00:00":
        return 1
    elif n == "10:40:00":
        return 2
    elif n == "12:40:00":
        return 3
    elif n == "14:20:00":
        return 4
    elif n == "16:20:00":
        return 5
    elif n == "18:10:00":
        return 6
    return 'Unknown'
            
#Определяет четность текущей недели(нужно ввести первый день твоего)
#def detect_week_type(month, day):
    september_1st = datetime(datetime.now().year, month, day)
    current_date = datetime.now()
    days_difference = (current_date - september_1st).days
    week_number = days_difference // 7
    print(days_difference)
    print(current_date)
    if week_number % 2 == 0:
        print("Четная неделя")
    else:
        print("Нечетная неделя")



#https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20
#https://timetable.mirea.ru/api/groups/name/%D0%91%D0%A1%D0%91%D0%9E-17-20
#parse_schedule("https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20")



    

#sergeeva.u.m@edu.mirea.ru
#SergeevaMike@19


