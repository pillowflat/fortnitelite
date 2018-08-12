import os
import threading
import subprocess
from dotenv import load_dotenv
import requests
import pprint as pp
from device import Device

load_dotenv()

API_KEY = os.getenv('API_KEY')
PLATFORM = os.getenv('PLATFORM')
NICKNAME = os.getenv('NICKNAME')
URL = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(PLATFORM, NICKNAME)
interval = os.getenv('POLL_INTERVAL_SEC')
POLL_INTERVAL_SEC = int(interval) if interval.isnumeric() else 5
DEVICE_NAME = os.getenv('DEVICE_NAME')

kills_count = 0

device = None
polls = 0

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

def poll():
    global kills_count
    global polls
    polls += 1
    status = get_status()
    new_kills = int(status['kills'])
    print('old kills: {}, new kills: {}'.format(kills_count, new_kills))
    
    # #debug
    # if (polls % 4 == 0):
    #     new_kills += 1

    if (new_kills != kills_count):
        kills_count = new_kills
        device.on()
    else:
        device.off()

def start_polling():
    threading.Timer(POLL_INTERVAL_SEC, start_polling).start()
    poll()

def init():
    print('POLL_INTERVAL_SEC: {}'.format(POLL_INTERVAL_SEC))    
    print('DEVICE_NAME: {}'.format(DEVICE_NAME))
    print('NICKNAME: {}'.format(NICKNAME))

    print('Testing switch on/off...')
    global device
    device = Device(DEVICE_NAME)
    device.on()
    device.off()

    print('Setting initial state...')
    status = get_status()
    pp.pprint(status)
    global kills_count
    kills_count = int(status['kills'])
    
    print('Starting polling...')
    start_polling()

if __name__ == "__main__":
    init()
