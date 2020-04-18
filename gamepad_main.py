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
#controller.register('servo1', functools.partial(serv.angle, 1))
#controller.register('camera_onoff', cam.onoff)

async def main():
    print("press Ctl-C to exit")
    #print("camera initialization")
    try:
        task1 = asyncio.create_task(controller.start())
        task2 = asyncio.create_task(cam.start())
        await task1
        await task2
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        cam.close()

if __name__ == '__main__':
    asyncio.run(main())
