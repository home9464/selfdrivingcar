"""The Xbox controller
"""

from evdev import  InputDevice



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


class XboxController:
    def __init__(self):
        self.controller = InputDevice('/dev/input/event0')

    def register(self, event, callback):
        """
        run callback() when event happens
        """
        pass
