"""The Xbox controller

1. it was not started
2. powered off after connection
"""
import asyncio
import random
from evdev import  InputDevice



STICK_OR_PAD_TYPE = 3
CODE_LEFT_STICK_VERTICAL = 0
CODE_LEFT_STICK_HORIZONTAL = 1

CODE_RIGHT_STICK_VERTICAL = 3
CODE_RIGHT_STICK_HORIZONTAL = 4

CODE_PAD_HORIZONTAL = 16
CODE_PAD_VERTICAL = 17

CODE_BUTTON_A = 304
CODE_BUTTON_B = 305
CODE_BUTTON_X = 306
CODE_BUTTON_Y = 307
CODE_BUTTON_LEFT_BUMPER = 308
CODE_BUTTON_RIGHT_BUMPER = 309
CODE_BUTTON_LEFT_BUMPER = 308
CODE_BUTTON_RIGHT_BUMPER = 309

CODE_BUTTON_VIEW = 310
CODE_BUTTON_MENU = 311


class XboxController:
    def __init__(self):
        self._wait_until_connected()
        self.events_callback = {'drive':[], 'servo0':[], 'servo1':[]}
        self.events_value = {'drive':None, 'servo0':None, 'servo1':None, 'camera_onoff': 0}

    def _wait_until_connected(self):
        self.controller = None
        while self.controller is None:
            try:
                self.controller = InputDevice('/dev/input/event0')
            except OSError as e:
                self.controller = None
        print('Controller connected')

    def register(self, event, callback):
        """
        run callback() when event happens
        """
        if event in self.events_callback and callback not in self.events_callback[event]:
            self.events_callback[event].append(callback)


    def unregister(self, event, callback):
        """
        remove callback()
        """
        if event in self.events_callback and callback in self.events_callback[event]:
            self.events_callback[event].remove(callback)

    async def start(self):
        # non-blocking
        while True:
            try:
                async for event in self.controller.async_read_loop():
                    #print(dir(event))
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
                        #driver.drive(direction)
                        self.events_value['drive'] = direction

                    if  event.code == CODE_RIGHT_STICK_VERTICAL:
                        print(event.value, event.sec, event.usec, event.timestamp, event.type)
                        'code', 'sec', 'timestamp', 'type', 'usec', 'value'

                        #self.events_value['servo0'] = random.randint(0, 180)
                        self.events_value['servo0'] = 180

                    if  event.code == CODE_RIGHT_STICK_HORIZONTAL:
                        self.events_value['servo0'] = 0
                        #pass
                        #print(dir(event))
                        #self.events_value['servo0'] = random.randint(0, 180)
                    #if  event.code == CODE_BUTTON_VIEW and event.value == 1:  # turn on / off camera
                    #    self.events_value['camera_onoff'] = 1 - self.events_value['camera_onoff']

                    for evt, callbacks in self.events_callback.items():
                        for cb in callbacks:
                            if self.events_value[evt] is not None:
                                cb(self.events_value[evt])
                                self.events_value[evt] = None
                await asyncio.sleep(0)
            except OSError as e:  # when controller was poweroff
                print('Controller not connected')
                self._wait_until_connected()
        def close(self):
            pass

if __name__ == '__main__':
    async def main():
        controller = XboxController()
        try:
            await asyncio.gather(await controller.start())
        except Exception as e:
            print(e)
        finally:
            pass
    asyncio.run(main())
