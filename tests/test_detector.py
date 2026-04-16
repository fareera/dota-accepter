import numpy as np
from unittest.mock import patch, MagicMock
from detector import Detector


@patch("detector.cv2.imread")
def test_init_loads_template(mock_imread):
    mock_imread.return_value = np.zeros((50, 120, 3), dtype=np.uint8)
    d = Detector(template_path="templates/accept_button.png", threshold=0.8)
    assert d.template is not None
    assert d.threshold == 0.8


@patch("detector.cv2.imread")
def test_init_missing_template_exits(mock_imread):
    mock_imread.return_value = None
    import pytest
    with pytest.raises(SystemExit):
        Detector(template_path="templates/missing.png", threshold=0.8)


@patch("detector.cv2.imread")
def test_find_dota_window_not_found(mock_imread):
    mock_imread.return_value = np.zeros((50, 120, 3), dtype=np.uint8)
    d = Detector(template_path="t.png", threshold=0.8)

    with patch("detector.find_dota_window", return_value=None):
        result = d.detect()
    assert result == (False, 0, 0)


@patch("detector.cv2.imread")
def test_detect_match_found(mock_imread):
    template = np.zeros((50, 120, 3), dtype=np.uint8)
    mock_imread.return_value = template

    d = Detector(template_path="t.png", threshold=0.8)

    fake_window = {"left": 100, "top": 100, "width": 1920, "height": 1080}
    fake_screenshot = np.zeros((300, 400, 3), dtype=np.uint8)

    with patch("detector.find_dota_window", return_value=fake_window), \
         patch("detector.capture_center_region", return_value=fake_screenshot), \
         patch("detector.cv2.matchTemplate") as mock_match, \
         patch("detector.cv2.minMaxLoc") as mock_minmax:

        mock_match.return_value = np.array([[0.95]])
        # max_val=0.95, max_loc=(50, 30) — top-left corner of match
        mock_minmax.return_value = (0, 0.95, (0, 0), (50, 30))

        detected, x, y = d.detect()

    assert detected is True
    # x = window_center_x_start + match_x + template_w/2
    # y = window_center_y_start + match_y + template_h/2
    assert x > 0
    assert y > 0


@patch("detector.cv2.imread")
def test_detect_no_match(mock_imread):
    template = np.zeros((50, 120, 3), dtype=np.uint8)
    mock_imread.return_value = template

    d = Detector(template_path="t.png", threshold=0.8)

    fake_window = {"left": 0, "top": 0, "width": 1920, "height": 1080}
    fake_screenshot = np.zeros((300, 400, 3), dtype=np.uint8)

    with patch("detector.find_dota_window", return_value=fake_window), \
         patch("detector.capture_center_region", return_value=fake_screenshot), \
         patch("detector.cv2.matchTemplate") as mock_match, \
         patch("detector.cv2.minMaxLoc") as mock_minmax:

        mock_match.return_value = np.array([[0.3]])
        mock_minmax.return_value = (0, 0.3, (0, 0), (50, 30))

        detected, x, y = d.detect()

    assert detected is False
    assert x == 0
    assert y == 0
