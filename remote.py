import requests
import random
import time

import asyncio
from pynput import keyboard

from test_cam import read_video_stream

base_url = 'http://1genomics.com:5000/'
direction_url = base_url + 'direction'
camera_url = base_url + 'camera'
broadcast_url = base_url + 'broadcast'

data = {'action': 'start'}
requests.post(broadcast_url, json = data)

"""

for i in range(10):
    data = {'angle': str(random.randint(0, 180))}
    time.sleep(1)
    x = requests.post(url, json = data)

data = {'angle': '180'}
time.sleep(1)
x = requests.post(camera_url, json = data)
"""

ANGLE = 180
THROTTLE = 0  # ([1, 100] -> forward, [-100, -1] -> backward, 0 -> stop)
def on_press(key):
    global ANGLE, THROTTLE
    try:
        #print('alphanumeric key {0} pressed'.format(key))
        drinving_pulse_time = 0.015

        # forward or backward, depends on throttle
        if key == keyboard.Key.up or key == keyboard.Key.down:
            THROTTLE = THROTTLE + 5 if key == keyboard.Key.up else THROTTLE - 5
            THROTTLE = 100 if THROTTLE > 100 else THROTTLE
            THROTTLE = -100 if THROTTLE < -100 else THROTTLE
            direction = 0
            if THROTTLE >= 1:
                direction = 1
            elif THROTTLE <= -1:
                direction = 2
            print(THROTTLE)
            data = {'duration': drinving_pulse_time, 'direction': direction, 'throttle':abs(THROTTLE)}
            requests.post(direction_url, json = data)

        # turn left
        elif key == keyboard.Key.left:
            data = {'duration': drinving_pulse_time, 'direction': 3, 'throttle': max(abs(THROTTLE), 70)}
            requests.post(direction_url, json = data)
        
        # turn right
        elif key == keyboard.Key.right:
            data = {'duration': drinving_pulse_time, 'direction': 4, 'throttle': max(abs(THROTTLE), 50)}
            requests.post(direction_url, json = data)

        # brake
        elif key == keyboard.Key.space:
            THROTTLE = 0
            data = {'duration': drinving_pulse_time, 'direction': 2, 'throttle': abs(THROTTLE)}
            requests.post(direction_url, json = data)

        elif key == keyboard.Key.page_up:
            ANGLE = max(0, ANGLE - 1)
            data =  {'angle': ANGLE}
            requests.post(camera_url, json = data)
        elif key == keyboard.Key.page_down:
            ANGLE = min(180, ANGLE + 1)
            data =  {'angle': ANGLE}
            requests.post(camera_url, json = data)
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    elif key == keyboard.Key.up:
        data = {'duration': '0.1', 'direction': '0'}
        requests.post(direction_url, json = data)
    elif key == keyboard.Key.down:
        data = {'duration': '0.1', 'direction': '0'}
        requests.post(direction_url, json = data)
    elif key == keyboard.Key.left:
        data = {'duration': '0.1', 'direction': '0'}
        requests.post(direction_url, json = data)
    elif key == keyboard.Key.right:
        data = {'duration': '0.1', 'direction': '0'}
        requests.post(direction_url, json = data)


# Collect events until released
#with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
#    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press,on_release=on_release)
listener.start()
asyncio.run(read_video_stream('192.168.1.3', 8888))
