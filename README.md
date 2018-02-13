<div align="center">
    <h1>~ YouTubeSubsToLCD ~</h1>
    <strong>A python script displaying YouTube Statistics on an I²C LCD display.</strong><br><br>
</div>

---

# Introduction

<div style="display: flex;">
  <a target="_blank" href="https://zekro.de/files/IMG_20180212_230225.jpg"><img src="https://zekro.de/files/IMG_20180212_230225.jpg" width="293"/></a>
  <a target="_blank" href="https://zekro.de/files/IMG_20180212_230237.jpg"><img src="https://zekro.de/files/IMG_20180212_230237.jpg" width="293"/></a>
  <a target="_blank" href="https://zekro.de/files/IMG_20180212_230312.jpg"><img src="https://zekro.de/files/IMG_20180212_230312.jpg" width="293"/></a>
</div>

> *Click images for fullsize view ;)*

This script pulls YouTube statistics via the YouTube V3 API and displays view and subscriber count on a common I²2 LCD display (in this case 2x16).
Also, as you can see, it shows a delta for both values which resets after 24 hours. Also the tool is able to log all data into a CSV file to analyze and display data in a char or something like this.

---

# Setup

### What do I need?

- **Raspberry Pi** *(Zero W / 1B / 1B+ / 2B / 2B1.2 / 3B)*
    - Python 3 Installed [*[How-To](https://raspberrypi.stackexchange.com/questions/59381/how-do-i-update-my-rpi3-to-python-3-6#59391)*]
- **2x16 LCD Display** *(Other sizes are also possible, but then you need to change some things in the settings)*
- **I²C Module for LCD display**
- **I²C 3.3V - 5V Logic Level Comverter** *(optional, but recommended ^^)*
- **Breadboard**
- **Jumper Wires** *(Male-Female)*
- **Google Account**

### First things first

You need to create a YouTube API V3 on your account and generate an API key.

1. Go to **[console.developers.google.com](https://console.developers.google.com)**
2. Create a project in the top left corner and select it
3. Klick on `Enable APIs and services`
4. Search for `YouTube Data API v3` and enable it
5. Then navigate to `Credentials` in the left sidebar
6. Klick `Create credentials` → `API key`
7. Copy the API key

### Display Setup

On tutorials-raspberrypi.com, you can find a verry good tutorial how to set up the display with a Raspberry Pi with Amazon links to all stuff you need:
- **[US/UK](https://tutorials-raspberrypi.com/control-a-raspberry-pi-hd44780-lcd-display-via-i2c/)**
- **[GER](https://tutorials-raspberrypi.de/hd44780-lcd-display-per-i2c-mit-dem-raspberry-pi-ansteuern/)**

> **Little tipp:**  
> You don't need unconditionally an I²C LLC to convert from 3.3V to 5V. You can also just plug the display directly to the I²C pins `(SDA → 3, SCL → 5)` and the power input to one of the two 5v power pins.  
> **But this is not recommended and if you should not do this if you don't want to damage your stuff accidentally!**  
> Here you can find a very nice map of all GPIO pins and their functions: **[pinout.xyz](https://pinout.xyz/)**

### Software Setup

First of all, you should install Python v3.6 on your Raspberry Pi. Use the following commands to do so:
```bash
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar xzvf Python-3.6.4.tgz
cd Python-3.6.4/
./configure
make
sudo make install
```
> **Attention**  
> This downloads the python repository and compiles it locally on the Raspberry Pi, so this process can take abount 30 minutes!

Then, as described in the tutorial on tutorials-raspberrypi.com, you need to install the packages `python-smbus` and `i2c-tools`:
```
sudo apt-get install python-smbus i2c-tools
```

Also, you need to enable I²C in the Raspberry Pi Options:
```
sudo raspi-config
```
> On **Raspberry Pi 2**, you need to enable it under `Interfacing Options` → `I2C`  
> Using a **Raspberry Pi 3**, you fint this option under `Advanced Options` → `I2C`

Then, add `i2c-dev` and `i2c-bcm2708` to modules with 
```
sudo echo i2c-dev >> /etc/modules
sudo echo i2c-bcm2708 >> /etc/modules
```

After that, you need to reboot your Raspberry Pi:
```
sudo reboot
```

### Script Setup

Now, create a folder somewhere you want to install the script. Then, download this repository or clone it with git:
```bash
mkdir display && cd display

git clone https://github.com/zekroTJA/YouTubeSubsToLCD.git ./
# OR
wget https://github.com/zekroTJA/YouTubeSubsToLCD/archive/master.zip && unzip master.zip ./ && rm master.zip
```

Now, you should plug in your display connection and get the adress of the display with the command:
```
sudo i2cdetect -y 1
```

The ouput should look like following:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
So, the address of your display would be `0x27` in this example.

Now, rename the **`settings.json.example`** to **`settings.json`** and enter your preferences:
- `key`: your YouTube Data API key
- `channel`: the YouTube channel you want to watch
- `interval`: the interval in secons the display should update
- `logging`: enable or disable if the script should write a log file in te set interval
- `display`.`width`: the character width of your display
- `display`.`address`: the address of your display you got with the command *`sudo i2cdetect -y 1`*
```json
{
    "key": "your YouTube API V3 key here",
    "channel": "zekrommaster110",
    "interval": 10,
    "logging": true,
    "dispay": {
        "width": 16,
        "address": "0x27"
    } 
}
```

Now, use the **`start`** script to start the tool. For this, **screen** is required to be installed:
```
sudo apt-get install screen
```

Now, enter
```
bash start h
```
to get some information about the start script and arguments you can use.

Now, if you start the script with
```
bash start
```
it will run in a screen named `display` which can be resumed with
```
bash start r
```
and stopped with
```
bash start s
```

Optionally, you can run the sccript without the start script with
```
python3 start.py
```
but keep in mind, that the process will stop after quitting the current SSH sesshion. This will only work, if you start the script via VNC or locally on the Pi's terminal.

