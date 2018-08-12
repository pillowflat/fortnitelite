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
interval = os.getenv('PING_INTERVAL_SEC')
PING_INTERVAL_SEC = int(interval) if interval.isnumeric() else 5

kills_count = 0

def switch_on():
    print('Switching on...')
    subprocess.run('wemo switch Outlet on'.split(' '))

def switch_off():
    print('Switching off...')    
    subprocess.run('wemo switch Outlet off'.split(' '))

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
    pp.pprint(status)
    if (status['kills'] != kills_count):
        kills_count = status['kills']
        switch_on()
    else:
        switch_off()

def start():
    threading.Timer(PING_INTERVAL_SEC, start).start()
    execute()

if __name__ == "__main__":
    print('PING_INTERVAL_SEC: {}'.format(PING_INTERVAL_SEC))    
    print('Testing switch on/off...')
    switch_on()
    switch_off()
    status = get_status()
    pp.pprint(status)
    kills_count = status['kills']
    start()

