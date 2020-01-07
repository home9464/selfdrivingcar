import sys
import random
import functools
import asyncio

from wheel import Wheel
from camera import Camera
from servo import Servo
from gamepad import XboxController

driver = Wheel()
cam = Camera()
serv = Servo()
controller = XboxController()
controller.register('drive', driver.drive)
controller.register('servo0', functools.partial(serv.angle, 0))
controller.register('servo1', functools.partial(serv.angle, 1))
controller.register('camera_onoff', cam.onoff)


async def start_controller():
    await controller.start()

async def start_camera():
    await cam.start()

async def main():
    print("press Ctl-C to exit")
    print("camera initialization")
    try:
        #await asyncio.gather(start_camera(),start_controller())
        await asyncio.gather(start_controller())
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        #cam.close()

if __name__ == '__main__':
    asyncio.run(main())
