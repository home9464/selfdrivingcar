import sys

import asyncio as AIO
import cv2
import random
from evdev import  InputDevice


from wheel import Wheel
from camera import Camera
from servo import Servo

try:
    gamepad = InputDevice('/dev/input/event0')
except OSError as e:
    print('Xbox controller is powered off')
    sys.exit(-1)


driver = Wheel()
cam = Camera()
serv = Servo()

async def read_gamepad():
    STICK_OR_PAD_TYPE = 3
    CODE_LEFT_STICK_VERTICAL = 0
    CODE_LEFT_STICK_HORIZONTAL = 1

    CODE_RIGHT_STICK_VERTICAL = 3
    CODE_RIGHT_STICK_HORIZONTAL = 4

    CODE_PAD_HORIZONTAL = 16
    CODE_PAD_VERTICAL = 17

    TYPE_BUTTON_A = 304
    TYPE_BUTTON_B = 305
    TYPE_BUTTON_X = 306
    TYPE_BUTTON_Y = 307
    TYPE_BUTTON_LEFT_BUMPER = 308
    TYPE_BUTTON_RIGHT_BUMPER = 309

    # non-blocking
    while True:
        async for event in gamepad.async_read_loop():
            if  event.code == CODE_PAD_HORIZONTAL or event.code == CODE_PAD_VERTICAL:
                # either x!=0 or y!=0 or both != 0
                x = event.value if event.code == CODE_PAD_HORIZONTAL else 0
                y = event.value if event.code == CODE_PAD_VERTICAL else 0
                direction = 0
                if x == 0:  # y != 0
                    if y == -1:
                        direction = 1  # 'up'
                    elif y == 1:
                        direction = 2  # 'down'
                    else:
                        pass
                elif y == 0:  # x != 0
                    if x == -1:
                        direction = 3  # 'left'
                    elif x == 1:
                        direction = 4  # 'right'
                    else:
                        pass
                else:  # x != 0 and y != 0
                    if x == -1 and y == -1:  # up-left
                        direction = 5  # 'up-left'
                    elif x == -1 and y == 1:  # up-right
                        direction = 6  # 'up-right'
                    elif x == 1 and y == -1:  # down-left
                        direction = 7  # 'down-left'
                    else:
                        direction = 8  # 'down-right'
                driver.drive(direction)

            if  event.code == CODE_RIGHT_STICK_VERTICAL or event.code == CODE_RIGHT_STICK_HORIZONTAL:
                serv.angle(0, random.randint(0, 120))
                serv.angle(1, random.randint(0, 120))

async def read_camera():
    await cam.start()

async def main():
    print("press Ctl-C to exit")
    print("camera initialization")
    try:
        await AIO.gather(read_camera(),read_gamepad())
    except KeyboardInterrupt:
        pass
    finally:
        driver.close()
        cam.close()

if __name__ == '__main__':
    AIO.run(main())

