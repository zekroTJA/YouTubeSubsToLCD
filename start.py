from lib import lcddriver
from time import *
import requests
import json
import sys

lcd = lcddriver.lcd()
lcd.lcd_clear()

subs = ''
views = ''
delta = 0
time = 0
s_subs = 0
arg_user = None
arg_interval = None
debug = False

argv = sys.argv[1:]

with open('settings.json') as f:
        config = json.loads(f.read())

def get_data():
    global subs, views, s_subs, time, delta
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={}&key={}'.format(
        arg_user if arg_user != None else config['channel'], config['key']
    )

    ytdata = json.loads(requests.get(url, headers=headers).text)['items'][0]['statistics']
    
    subs = ytdata['subscriberCount']
    views = ytdata['viewCount']

    if (s_subs == 0):
        s_subs = subs
    delta = int(subs) - int(s_subs)
    if (time > 86400 / config['interval']):
        time = 0
        s_subs = 0
    else:
        time += 1


def pointalize(string):
    out = ''
    c_len = len(string)
    def _notneg(numb):
        return 0 if numb < 0 else numb
    while c_len > 0:
        out = string[_notneg(c_len - 3):c_len] + '.' + out
        c_len -= 3
    return out[:-1]


if len(argv) > 0:
    global arg_user, arg_interval, debug
    if '-u' in argv:
        arg_user = argv[argv.index('-u') + 1]
    if '-i' in argv:
        arg_interval = argv[argv.index('-i') + 1]
    if '-d' in argv:
        debug = True



print("INITIALIZED WITH CHANNEL: " + (arg_user if arg_user != None else config['channel']) + "\n")

while (True):
    def _delta():
        return '+' + str(delta) if delta >= 0 else '-' + str(delta)

    def _subs():
        out = pointalize(subs) + ' subs'
        for i in range(0, 16 - len(out) - len(str(delta)) - 1):
            out += ' '
        out += _delta()
        return out

    get_data()
    lcd.lcd_clear()
    lcd.lcd_display_string(_subs(), 1)
    lcd.lcd_display_string(strftime("%H:%M:%S", localtime()), 2)
    if debug:
        print(
            _subs() + '\n' +
            strftime("%H:%M:%S", localtime())
        )
    sleep(arg_interval if arg_interval != None else config['interval'])