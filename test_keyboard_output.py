"""
Tests keyboard output.
"""
import pytest
from keyboard_output import *

# Mock the keyboard.press function to capture the pressed key
pressed_key = None
def virtual_press(key):
    global pressed_key
    pressed_key = key

@pytest.mark.timeout(10)
def test_forward(monkeypatch):
    monkeypatch.setattr('keyboard.press', virtual_press)
    movement_press(0)
    assert pressed_key == "w"
