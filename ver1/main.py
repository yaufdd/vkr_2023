import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
from datetime import datetime
from connectdb import save_schedule_todb

session = requests.Session()

user_data = {}

def login():

    login_url = 'https://lk.mirea.ru/auth.php'

    login_data = {
        'AUTH_FORM' : 'Y',
        'TYPE' : 'AUTH',
        'USER_LOGIN' : user_data['login'],
        'USER_PASSWORD' : user_data['password'],
        'USER_REMEMBER' : 'Y'
    }
    login_responce = session.post(login_url, data=login_data)
    
    return login_responce


    

def authorization():
    
    login_url = 'https://lk.mirea.ru/auth.php'

    login_data = {
        'AUTH_FORM' : 'Y',
        'TYPE' : 'AUTH',
        'USER_LOGIN' : 'bamba.e@edu.mirea.ru',
        'USER_PASSWORD' : 'a8JkFUmW',
        'USER_REMEMBER' : 'Y'
    }
    login_responce = session.post(login_url, data=login_data)
    
    return login_responce

#Ищет группу студента и запоминает его в словаь
def find_student_group():
    try:
        login_responce = login()
        soup =  BeautifulSoup(login_responce.text, 'html.parser')
        group_table = soup.find_all('table')[0]

        elements_in_gourp_table = group_table.find_all('td')
        
        student_gourp = elements_in_gourp_table[4]
        user_data['group'] = student_gourp.text
        return user_data
    except IndexError:
        return 
    
def find_student_name():
    login_responce = login()
    soup =  BeautifulSoup(login_responce.text, 'html.parser')
    student_find_divs = soup.find_all(class_='student-personal-info')
    for div in student_find_divs:
        second_div = div.find_all('div')[0]

        span = second_div.find('span')
        if span :
            full_name = span.text.strip()
            user_data['name'] = full_name
            return user_data

#Создает специальную ссылку для студента
def get_personal_url(url):
    personal_url = url + quote(user_data['group'], encoding='utf-8')
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


def save_schedule(url):
    personal_url = url + quote(user_data['group'], encoding='utf-8')
    responce = session.get(personal_url)
    json_scheduleData = json.loads(responce.text)
    save_schedule_todb(user_data['tg_id'], json_scheduleData)


def week_evenOrNot(target_date):
    year = target_date.year
    september_1 = datetime(year, 9, 1)
    weekday = september_1.weekday()
    count = (target_date - september_1).days
    number = (count + weekday) // 7 + 1

    even = True
    if number % 2 != 0:
        even = False

    return even, target_date.weekday()
    


#print(save_schedule("https://timetable.mirea.ru/api/groups/name/"))









#https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20
#https://timetable.mirea.ru/api/groups/name/%D0%91%D0%A1%D0%91%D0%9E-17-20
#parse_schedule("https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20")


#sergeeva.u.m@edu.mirea.ru
#SergeevaMike@19
