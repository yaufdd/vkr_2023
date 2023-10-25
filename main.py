import requests
import datetime
from bs4 import BeautifulSoup

session = requests.Session()


def authorization(login, password):

    login_url = 'https://lk.mirea.ru/auth.php'

    login_data = {
        'AUTH_FORM' : 'Y',
        'TYPE' : 'AUTH',
        'USER_LOGIN' : login,
        'USER_PASSWORD' : password,
        'USER_REMEMBER' : 'Y'
    }

    login_responce = session.post(login_url, data=login_data)

    return login_responce
    

def find_student_group(login, password):
    
    login_responce = authorization(login, password)
    soup =  BeautifulSoup(login_responce.text, 'html.parser')
    group_table = soup.find_all('table')[0]

    elements_in_gourp_table = group_table.find_all('td')
    
    student_gourp = elements_in_gourp_table[4]

    print(f"Your group is {student_gourp.text}")


def parse_schedule(url):
    authorization()

    schedule_responce = session.get(url)

    file_path = "example.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(schedule_responce.text)
    if "Облачные технологии" in schedule_responce:
        print("ok")
    print(schedule_responce.headers)







#https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20
#https://timetable.mirea.ru/api/groups/name/%D0%91%D0%A1%D0%91%D0%9E-17-20
#parse_schedule("https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20")



    




