import time
from unittest.mock import patch
from clicker import Clicker


@patch("clicker.pyautogui.click")
@patch("clicker.pyautogui.moveTo")
def test_click_accept(mock_move, mock_click):
    c = Clicker(cooldown_seconds=5)
    result = c.click(100, 200)
    assert result is True
    mock_move.assert_called_once_with(100, 200)
    mock_click.assert_called_once()


@patch("clicker.pyautogui.click")
@patch("clicker.pyautogui.moveTo")
def test_click_during_cooldown(mock_move, mock_click):
    c = Clicker(cooldown_seconds=5)
    c.click(100, 200)
    result = c.click(100, 200)
    assert result is False
    assert mock_click.call_count == 1


@patch("clicker.pyautogui.click")
@patch("clicker.pyautogui.moveTo")
def test_click_after_cooldown(mock_move, mock_click):
    c = Clicker(cooldown_seconds=0)
    c.click(100, 200)
    result = c.click(100, 200)
    assert result is True
    assert mock_click.call_count == 2


def test_is_cooling_down():
    c = Clicker(cooldown_seconds=5)
    assert c.is_cooling_down() is False
