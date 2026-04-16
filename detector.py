import sys
import numpy as np
import cv2

try:
    import win32gui
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False

DOTA_WINDOW_TITLE = "Dota 2"
CAPTURE_WIDTH = 400
CAPTURE_HEIGHT = 300


def find_dota_window():
    if not HAS_WIN32:
        return None
    hwnd = win32gui.FindWindow(None, DOTA_WINDOW_TITLE)
    if not hwnd:
        return None
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return {
        "left": left,
        "top": top,
        "width": right - left,
        "height": bottom - top,
    }


def capture_center_region(window: dict) -> np.ndarray:
    cx = window["left"] + window["width"] // 2
    cy = window["top"] + window["height"] // 2
    monitor = {
        "left": cx - CAPTURE_WIDTH // 2,
        "top": cy - CAPTURE_HEIGHT // 2,
        "width": CAPTURE_WIDTH,
        "height": CAPTURE_HEIGHT,
    }
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


class Detector:
    def __init__(self, template_path: str, threshold: float):
        self.template = cv2.imread(template_path)
        if self.template is None:
            print(f"Error: Template image not found: {template_path}")
            sys.exit(1)
        self.threshold = threshold
        self.template_h, self.template_w = self.template.shape[:2]

    def detect(self) -> tuple[bool, int, int]:
        window = find_dota_window()
        if window is None:
            return (False, 0, 0)

        screenshot = capture_center_region(window)

        result = cv2.matchTemplate(screenshot, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= self.threshold:
            # Calculate screen-absolute coordinates of button center
            cx = window["left"] + window["width"] // 2
            cy = window["top"] + window["height"] // 2
            region_left = cx - CAPTURE_WIDTH // 2
            region_top = cy - CAPTURE_HEIGHT // 2

            button_x = region_left + max_loc[0] + self.template_w // 2
            button_y = region_top + max_loc[1] + self.template_h // 2
            return (True, button_x, button_y)

        return (False, 0, 0)
