"""
Group: Keyboard Liberators
This code provides a simpler way to send gamepad controls to the virtual controller.
"""

import vgamepad as vg
from vgamepad import XUSB_BUTTON


class VGamepad:
    """
    Virtual controller
    """

    UP = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    DOWN = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    LEFT = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    RIGHT = XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    A = XUSB_BUTTON.XUSB_GAMEPAD_A
    B = XUSB_BUTTON.XUSB_GAMEPAD_B
    X = XUSB_BUTTON.XUSB_GAMEPAD_X
    Y = XUSB_BUTTON.XUSB_GAMEPAD_Y
    START = XUSB_BUTTON.XUSB_GAMEPAD_START
    BACK = XUSB_BUTTON.XUSB_GAMEPAD_BACK
    GUIDE = XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

    def __init__(self):
        self._gamepad = vg.VX360Gamepad()

    def left_trigger(self, value):
        self._gamepad.left_trigger_float(value)  # [0.0, 1.0]
        self._gamepad.update()

    def right_trigger(self, value):
        self._gamepad.right_trigger_float(value)  # [0.0, 1.0]
        self._gamepad.update()

    def left_joystick(self, x_value, y_value):
        self._gamepad.left_joystick_float(x_value, y_value)  # [-1.0, 1.0]
        self._gamepad.update()

    def right_joystick(self, x_value, y_value):
        self._gamepad.right_joystick_float(x_value, y_value)  # [-1.0, 1.0]
        self._gamepad.update()

    def press_button(self, button: XUSB_BUTTON):
        self._gamepad.press_button(button)
        self._gamepad.update()

    def release_button(self, button: XUSB_BUTTON):
        self._gamepad.release_button(button)
        self._gamepad.update()

    def release(self):
        del self._gamepad
