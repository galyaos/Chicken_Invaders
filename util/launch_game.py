import subprocess
import time

# Launches the game using the provided path
def launch_game(game_path):
    print(f"Launching game: {game_path}")
    subprocess.Popen(game_path, shell=True)
    time.sleep(3)