import requests
import datetime
from bs4 import BeautifulSoup

session = requests.Session()




    

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
    soup =  BeautifulSoup(login_responce.text, 'html.parser')
    group_lable = soup.find_all('tr')
    
    print(group_lable)


import time

def parse_schedule(url):
    authorization()

    headers = {
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    schedule_responce = session.get(url)

    file_path = "example.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(schedule_responce.text)
    if "Облачные технологии" in schedule_responce:
        print("ok")
    print(schedule_responce.headers)

authorization()






#https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20
#https://timetable.mirea.ru/api/groups/name/%D0%91%D0%A1%D0%91%D0%9E-17-20
#parse_schedule("https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20")



    




