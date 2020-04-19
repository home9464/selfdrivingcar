#!/usr/bin/python3
import asyncio
import random
import time
import threading

from quart import Quart, request, jsonify
from servo import Servo
from wheel import Wheel
from broadcast import VideoBroadcastThread


###################################################
# start a thread to broadcast video only
start_video = False
def broadcast_video():
    video_loop = asyncio.new_event_loop()
    video_loop.create_task(broadcast(video_loop))
    video_loop.run_forever()
if start_video:
    threading.Thread(target=broadcast_video).start()
###################################################


app = Quart(__name__)
svo = Servo()
drv = Wheel()

video_broadcast = None

@app.route('/', methods=['GET'])
async def index():
    svo.angle(0, random.randint(0, 180))
    await asyncio.sleep(0)
    return ('', 200)

@app.route('/direction', methods=['POST'])
async def direction():
    content = await request.get_json()
    if content is not None:
        seconds = float(content['duration'])
        direction = int(content['direction'])
        throttle = int(content['throttle'])
        drv.drive(direction, throttle)  # start driving
        if direction != 0:
            await asyncio.sleep(seconds)  # driving time
    return ('', 200)

@app.route('/camera', methods=['POST'])
async def camera():
    content = await request.get_json()
    if content is not None:
        angle = int(content['angle'])
        svo.angle(0, angle)
    return ('', 200)

@app.route('/broadcast', methods=['POST'])
async def broadcast():
    global video_broadcast
    content = await request.get_json()
    if content is not None:
        action = content['action']
        if action == 'start':
            if video_broadcast is None:
                video_broadcast = VideoBroadcastThread() 
                video_broadcast.start() 
        elif action == 'stop':
            print('stop video')
            if video_broadcast is not None:
                video_broadcast.stop() 
                print('exception')
                #video_broadcast.join()
                video_broadcast = None
    return ('', 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




