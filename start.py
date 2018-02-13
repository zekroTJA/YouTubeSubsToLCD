from time import *
import requests
import json
import sys

subs = ''
views = ''
time = 0
s_delta = 0
s_subs = 0
v_delta = 0
v_views = 0
arg_user = None
arg_interval = None
debug = False
display = True
lcd = None
logging = None
displaywidth = 16

status = 'subs'

argv = sys.argv[1:]

if len(argv) > 0:
    if '-u' in argv:
        arg_user = argv[argv.index('-u') + 1]
    if '-i' in argv:
        arg_interval = argv[argv.index('-i') + 1]
    if '-d' in argv:
        debug = True
    if '--nodisplay' in argv:
        display = False
    if '-l' in argv:
        logging = True


if display:
    from lib import lcddriver
    lcd = lcddriver.lcd()
    lcd.lcd_clear()


with open('settings.json') as f:
    config = json.loads(f.read())
    if config['logging'] and logging == None:
        logging = config['logging']
    if config['display-width']:
        displaywidth = config['display-width']    

def get_data():
    global subs, views, s_subs, time, s_delta, v_views, v_delta
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername={}&key={}'.format(
        arg_user if arg_user != None else config['channel'], config['key']
    )

    ytdata = json.loads(requests.get(url, headers=headers).text)['items'][0]['statistics']
    
    subs = ytdata['subscriberCount']
    views = ytdata['viewCount']

    if (s_subs == 0):
        s_subs = subs
        v_views = views
    s_delta = int(subs) - int(s_subs)
    v_delta = int(views) - int(v_views)
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
    

print("INITIALIZED WITH CHANNEL: " + (arg_user if arg_user != None else config['channel']))
if debug:
    print("DEBUG MODE ENABLED")
if logging:
    print("LOGGING ENABLED")
print('\n')

while (True):
    def _delta(delta):
        return '+' + str(delta) if delta >= 0 else '-' + str(delta)

    def _subs(mode):
        out = pointalize(subs if mode == 'subs' else views) + ' ' + mode[:1]
        for i in range(0, displaywidth - len(out) - len(str(s_delta if mode == 'subs' else v_delta)) - 1):
            out += ' '
        out += _delta(s_delta if mode == 'subs' else v_delta)
        return out

    get_data()
    # lcd.lcd_clear()
    if display:
        lcd.lcd_display_string(_subs(status), 1)
        lcd.lcd_display_string(strftime("%H:%M:%S", localtime()), 2)
    if debug:
        print(
            _subs(status) + '\n' +
            strftime("%H:%M:%S", localtime())
        )
    if (logging):
        with open('log.csv', 'a') as file:
            file.write(
                "%s,%s,%s\n" % (strftime("%Y/%m/%d - %H:%M:%S", localtime()), subs, views)
            )

    if status == 'subs':
        status = 'views'
    else:
        status = 'subs'

    sleep(int(arg_interval) if arg_interval != None else config['interval'])