import pydirectinput
import time

class KeyController:
    def __init__(self, press_duration=0.004, space_duration=0.000000001):
        self.press_duration = press_duration
        self.space_duration = space_duration
        self.active_keys = set()  # Track currently pressed keys

    def press_key(self, key, duration=None):
        if duration is None:
            duration = self.press_duration
        if key not in self.active_keys:  # Prevent re-pressing the same key
            pydirectinput.keyDown(key)
            self.active_keys.add(key)
        time.sleep(duration)

    def release_key(self, key):
        if key in self.active_keys:
            pydirectinput.keyUp(key)
            self.active_keys.remove(key)

    def press_left(self, player):
        key = 'a' if player == 1 else 'left'
        self.press_key(key)
        return key

    def press_right(self, player):
        key = 'd' if player == 1 else 'right'
        self.press_key(key)
        return key

    def press_space(self, player):
        key = 'w' if player == 1 else 'space'
        self.press_key(key, self.space_duration)  # Quick tap
        self.release_key(key)
        return key