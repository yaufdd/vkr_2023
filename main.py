import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
from datetime import datetime


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

class Subject:
    def __init__(self, name, campus, time_start, time_end, weekday, lesson_type):
        self.name = name
        self.campus = campus
        self.time_start = time_start
        self.time_end = time_end
        self.weekday = weekday
        self.lesson_type = lesson_type

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


#Парсит API расписания, запоминает в четный и нечетные недели листа объкеты дисциплины
def parse_schedule_api():
    schedule_responce = session.get(get_personal_url('https://timetable.mirea.ru/api/groups/name/'))
    schedule_api_data = json.loads(schedule_responce.text)
    lessons = schedule_api_data['lessons']
    even_week_subjects = []
    odd_week_subjects = []
    
    for i in range(len(lessons)):
        dict = {}
        dict = lessons[i]
        if dict['weeks'][0] % 2 == 0:
            evenweek = Subject(dict['discipline']['name'], 
                                      dict['room']['campus']['name'], 
                                      dict['calls']['time_start'], 
                                      dict['calls']['time_end'], 
                                      dict['weekday'], 
                                      dict['lesson_type']['name'])
            even_week_subjects.append(evenweek)
        if dict['weeks'][0] % 2 != 0:
            oddweek = Subject(dict['discipline']['name'], 
                                      dict['room']['campus']['name'], 
                                      dict['calls']['time_start'], 
                                      dict['calls']['time_end'], 
                                      dict['weekday'], 
                                      dict['lesson_type']['name'])
            odd_week_subjects.append(oddweek)

    easy_schedule_api = {
        "even" : sort_in_order_global(even_week_subjects),
        "odd" : sort_in_order_global(odd_week_subjects)
    }

    with open ('easy_schedule.json', 'w') as file:
        json.dump(easy_schedule_api, file)
    

def convertAllToJSON(input_list: list):
    res = [0] * len(input_list)
    for i, subject in enumerate(input_list):
        print(i, subject)
        res[i] = subject.toJSON()
    return res


def sort_in_order_global(input_list : list):
    Monday_subjects = []
    Tuesday_subjects = []
    Wednesday_subjects = []
    Thursday_subjects = []
    Friday_subjects = []
    Saturday_subjects = []
    for subject in input_list :
        if detect_weekday(subject.weekday) == 'Monday':
            Monday_subjects.append(subject)
        elif detect_weekday(subject.weekday) == "Tuesday":
            Tuesday_subjects.append(subject)
        elif detect_weekday(subject.weekday) == "Wednesday":
            Wednesday_subjects.append(subject)
        elif detect_weekday(subject.weekday) == "Thursday":
            Thursday_subjects.append(subject)
        elif detect_weekday(subject.weekday) == "Friday":
            Friday_subjects.append(subject)
        elif detect_weekday(subject.weekday) == "Saturday":
            Saturday_subjects.append(subject)
    Monday_subjects.sort(key=lambda a: a.time_start)
    Tuesday_subjects.sort(key=lambda a: a.time_start)
    Wednesday_subjects.sort(key=lambda a: a.time_start)
    Thursday_subjects.sort(key=lambda a: a.time_start)
    Friday_subjects.sort(key=lambda a: a.time_start)
    Saturday_subjects.sort(key=lambda a: a.time_start)

    Monday_subjects = convertAllToJSON(Monday_subjects)
    Tuesday_subjects = convertAllToJSON(Tuesday_subjects)
    Wednesday_subjects = convertAllToJSON(Wednesday_subjects)
    Thursday_subjects = convertAllToJSON(Thursday_subjects)
    Friday_subjects = convertAllToJSON(Friday_subjects)
    Saturday_subjects = convertAllToJSON(Saturday_subjects)
    return Monday_subjects, Tuesday_subjects, Wednesday_subjects, Thursday_subjects, Friday_subjects, Saturday_subjects
    
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


def detect_week_type():
    try :
        
        schedule_page = authorization()
        soup =  BeautifulSoup(schedule_page.text, 'html.parser')
        week_type = soup.find('p', class_='mt-0 text-sm text-gray-500 sm:mt-1')

        return schedule_page.text
    except:
        return

def 



#print(parse_schedule_api())

#https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20
#https://timetable.mirea.ru/api/groups/name/%D0%91%D0%A1%D0%91%D0%9E-17-20
#parse_schedule("https://timetable.mirea.ru/ui/schedule?group=%D0%91%D0%A1%D0%91%D0%9E-17-20")



    




