import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import quote
from access_lks import user_info

session = requests.Session()


def get_json(URL):
    json_responce = json.loads(session.get(URL).text)
    return json_responce

def get_group_uid(group_name):
    encoded_string = quote(group_name, encoding='utf-8')
    group_uid = get_json(f'https://app-api.mirea.ninja/api/v1/schedule/search/groups?query={encoded_string}')
    group_uid['results'][0]['uid']
    return group_uid['results'][0]['uid']

def get_group_schedule(uid):
    schedule_data = get_json(f'https://app-api.mirea.ninja/api/v1/schedule/group/{uid}')
    return schedule_data




    