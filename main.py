import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json

session = requests.Session()

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


def parse_schedule_api():
    authorization()
    schedule_responce = session.get(get_personal_url('https://timetable.mirea.ru/api/groups/name/'))
    schedule_api_data = json.loads(schedule_responce.text)
    lessons = schedule_api_data["lessons"]
    return lessons


def make_schedule(data):
    subject = {}
    if data['weekday'] == 1:
        print("True")

print(parse_schedule_api())


#https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20
#https://timetable.mirea.ru/api/groups/name/%D0%91%D0%A1%D0%91%D0%9E-17-20
#parse_schedule("https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20")



    




