import time
import pydirectinput

# Simulate mouse clicks at the specified position to start the game
def simulate_mouse_clicks(x, y, count=4, mode=1):
    pydirectinput.moveTo(x, y)  # Move cursor to the target position
    for _ in range(count):
        pydirectinput.click()
        time.sleep(0.3)  # Small delay between clicks
    # If two-player mode, press 'W' after the 4 clicks to generate second player
    if mode == 2:
        time.sleep(0.2)
        pydirectinput.press('w')