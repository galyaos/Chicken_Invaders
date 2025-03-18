from GameController import GameController
from ui.calibration import show_calibration_screen
from util.launch_game import launch_game
from util.simulate_mouse_clicks import simulate_mouse_clicks
from before_main import process_hand

CLICK_X, CLICK_Y = 405, 800
IMAGE_PATH = r"C:\Users\ostr1\PycharmProjects\ai_course\image_processing_full\images\SlobChickenHead.png"
GAME_PATH = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Chicken Invaders 1\Chicken Invaders 1 (remastered).lnk"

if __name__ == "__main__":
    mode = process_hand()
    controller = GameController(mode1="double" if mode == 2 else "single")
    show_calibration_screen(IMAGE_PATH, controller)
    launch_game(GAME_PATH)
    simulate_mouse_clicks(CLICK_X, CLICK_Y, count=4, mode=mode)
    controller.run()
