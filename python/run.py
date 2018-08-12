import os
import threading
import subprocess
from dotenv import load_dotenv
import requests
import pprint as pp

load_dotenv()

API_KEY = os.getenv('API_KEY')
PLATFORM = os.getenv('PLATFORM')
NICKNAME = os.getenv('NICKNAME')
URL = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(PLATFORM, NICKNAME)

kills_count = 0

def switch_on():
    subprocess.run('wemo switch Outlet on'.split(' '))

def switch_off():
    subprocess.run('wemo switch Outlet on'.split(' '))

def get_value(key, items):
    for item in items:
        if item['key'] == key:
            return item['value']
    return None

def get_status():
    headers = { 'TRN-Api-Key': API_KEY }
    try:
        response = requests.get(URL, headers=headers)
        json = response.json()
        stats = json['lifeTimeStats']
        return { 
            'user': json['epicUserHandle'],
            'matches': get_value('Matches Played', stats),
            'kills': get_value('Kills', stats)
        }
    except Exception as err:
        print('Error: {}'.format(err))

def execute():
    global kills_count
    status = get_status()
    if (status['kills'] != kills_count):
        kills_count = status['kills']
        switch_on()
    else:
        switch_off()

def start():
    threading.Timer(5.0, start).start()
    execute()

if __name__ == "__main__":
    kills_count = get_status()['kills']
    start()
