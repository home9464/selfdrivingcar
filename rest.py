import asyncio
import random
import time
import threading

from quart import Quart, request, jsonify
from servo import Servo
from camsrv import broadcast
from wheel_pi3 import Wheel

start_video = False

###################################################
# start a thread to broadcast video only
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

@app.route('/', methods=['GET'])
async def index():
    svo.angle(0, random.randint(0, 100))
    drv.drive(1)
    time.sleep(0.1)
    drv.drive(0)
    await asyncio.sleep(0)
    return ('', 200)


@app.route('/direction', methods=['POST'])
async def direction():
    content = await request.get_json()
    if content is not None:
        seconds = float(content['duration'])
        direction = int(content['direction'])
        drv.drive(direction)
        await asyncio.sleep(seconds)
        drv.drive(0)
    await asyncio.sleep(0)
    return ('', 200)

@app.route('/camera', methods=['POST'])
async def camera():
    content = await request.get_json()
    if content is not None:
        angle = int(content['angle'])
        svo.angle(0, angle)
    await asyncio.sleep(0)
    return ('', 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




