import time
import pyautogui

pyautogui.FAILSAFE = False


class Clicker:
    def __init__(self, cooldown_seconds: float):
        self.cooldown_seconds = cooldown_seconds
        self._last_click_time = 0.0

    def is_cooling_down(self) -> bool:
        return time.time() - self._last_click_time < self.cooldown_seconds

    def click(self, x: int, y: int) -> bool:
        if self.is_cooling_down():
            return False
        pyautogui.moveTo(x, y)
        pyautogui.click()
        self._last_click_time = time.time()
        return True
