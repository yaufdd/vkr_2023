import requests


session = requests.Session()

user_info = {}
def login(login, password):
    try:
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
    except Exception as e:
        return
    

