"""
Group: Keyboard Liberators
This code provides a simpler way to send gamepad controls to the virtual controller.
"""

# Guarded import for vgamepad (Windows/Linux only)
try:
    import vgamepad as vg
    from vgamepad import XUSB_BUTTON
    _HAS_VGAMEPAD = True
except Exception:
    vg = None
    XUSB_BUTTON = None
    _HAS_VGAMEPAD = False


class VGamepad:
    """
    Virtual controller (supports skip mode for macOS/testing)
    """

    # Button constants - only defined if vgamepad available
    if _HAS_VGAMEPAD:
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
    else:
        # Dummy constants for skip mode (macOS)
        UP = DOWN = LEFT = RIGHT = A = B = X = Y = START = BACK = GUIDE = None

    def __init__(self, skip=False):
        if not skip and _HAS_VGAMEPAD:
            self._gamepad = vg.VX360Gamepad()
        else:
            self._gamepad = None

    def left_trigger(self, value):
        if self._gamepad:
            self._gamepad.left_trigger_float(value)  # [0.0, 1.0]
            self._gamepad.update()

    def right_trigger(self, value):
        if self._gamepad:
            self._gamepad.right_trigger_float(value)  # [0.0, 1.0]
            self._gamepad.update()

    def left_joystick(self, x_value, y_value):
        if self._gamepad:
            self._gamepad.left_joystick_float(x_value, y_value)  # [-1.0, 1.0]
            self._gamepad.update()

    def right_joystick(self, x_value, y_value):
        if self._gamepad:
            self._gamepad.right_joystick_float(x_value, y_value)  # [-1.0, 1.0]
            self._gamepad.update()

    def press_button(self, button):
        if self._gamepad:
            self._gamepad.press_button(button)
            self._gamepad.update()

    def release_button(self, button):
        if self._gamepad:
            self._gamepad.release_button(button)
            self._gamepad.update()

    def release(self):
        if self._gamepad:
            self._gamepad.reset()
            self._gamepad.update()
