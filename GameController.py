import cv2
import threading
import time
from ForegroundSegmenter import ForegroundSegmenter
from util.KeyController import KeyController
from PlayerDetection import detect_players


class GameController:
    def __init__(self, mode1="double", downsample_factor=2, frame_skip=10):
        self.cap = cv2.VideoCapture(0)
        self.mode = mode1
        self.downsample_factor = downsample_factor
        self.frame_skip = frame_skip
        self.frame_count = 0
        self.key_controller = KeyController()
        self.video_mode = False
        self.frame = None  # Store the latest frame
        self.player_centers = {}  # Store initial centers for players
        self.keys_pressed = {}  # Track pressed keys
        self.segmenter = ForegroundSegmenter()

        # Start a separate thread for reading frames
        self.running = True
        self.video_thread = threading.Thread(target=self.read_frames, daemon=True)
        self.video_thread.start()

    def read_frames(self):
        """Continuously reads frames in a separate thread for real-time performance."""
        while self.cap.isOpened() and self.running:
            time.sleep(0.1)  # Skip frames for performance and flashing lights
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def process_frame(self):
        frame = self.frame
        if frame is None:
            return None  # Skip processing if there's no frame

        frame = frame[150:-20, :]  # Crop top 50 pixels and bottom 50 pixels
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        players = detect_players(frame, self.segmenter, mode=self.mode)

        for i, player in enumerate(players):
            bx, by, bw, bh = player['body']
            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 0, 0), 2)
            body_center_x = bx + bw // 2
            body_center_y = by + bh // 2

            if i not in self.player_centers:
                self.player_centers[i] = (body_center_x, body_center_y)

            self.handle_player(body_center_x, body_center_y, i)

        return frame

    def handle_player(self, body_center_x, body_center_y, player, movement_threshold=5):
        """Handles player movement by checking deviation from the initial center."""
        print(player)
        center_x, center_y = self.player_centers[player]

        # Ensure player has a set to store pressed keys
        if player not in self.keys_pressed:
            self.keys_pressed[player] = set()

        keys_to_press = set()  # Keys that need to be pressed
        keys_to_release = set(self.keys_pressed[player])  # Keys that should be released

        # Handle left and right movement
        if body_center_x > center_x + (movement_threshold+4):
            keys_to_press.add(self.key_controller.press_left(player))
            print(f"Player {player}: Move Left")
        elif body_center_x < center_x - (movement_threshold+4):
            keys_to_press.add(self.key_controller.press_right(player))
            print(f"Player {player}: Move Right")

        # Handle up (shoot)
        if body_center_y < center_y - movement_threshold:  # Move up
            keys_to_press.add(self.key_controller.press_space(player))
            print(f"Player {player}: Move Up (Shoot)")

        # Determine which keys should be released
        keys_to_release -= keys_to_press  # Keep only keys that were previously pressed but are not in the new keys_to_press set

        # Apply key presses
        for key in keys_to_press:
            if key not in self.keys_pressed[player]:  # Prevent re-pressing
                self.keys_pressed[player].add(key)

        # Release keys that are no longer needed
        for key in keys_to_release:
            self.key_controller.release_key(key)
            self.keys_pressed[player].remove(key)

    def run(self):
        while self.running:
            if self.frame is None:
                continue
            processed = self.process_frame()
            if processed is None:
                continue

            cv2.imshow('Game Control', processed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()