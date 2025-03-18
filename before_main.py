import cv2
import numpy as np
import joblib
import mediapipe as mp
import time
import threading
from collections import Counter


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=mode,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        return results

    def findPosition(self, img, results):
        hands_data = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lmList = [[lm.x, lm.y] for lm in handLms.landmark]
                hands_data.append(lmList)
        return hands_data


class VideoCaptureApp:
    def __init__(self, model1_path, model2_path):
        self.model1 = joblib.load(model1_path)
        self.model2 = joblib.load(model2_path)
        self.detector = HandDetector()
        self.final_prediction = None
        self.prediction_ready = threading.Event()

    def capture_and_predict(self, model, image_map, message_1, message_2=None):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video stream.")
            return None

        predictions = []
        print(f"Waiting 1 second before starting: {message_1}")
        time.sleep(1)

        for frame_idx in range(15):
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)

            cv2.putText(frame, message_1, (25, 25),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            if message_2 is not None:
                cv2.putText(frame, message_2, (25, 70),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            results = self.detector.findHands(frame)
            hands_data = self.detector.findPosition(frame, results)
            if hands_data:
                feature_vector = np.array([coord for point in hands_data[0] for coord in point]).reshape(1, -1)
                predicted_class = model.predict(feature_vector)[0]
                predictions.append(predicted_class)
                print(f"Frame {frame_idx + 1}: Predicted Class = {predicted_class}")
                if predicted_class in image_map:
                    prediction_img = cv2.imread(image_map[predicted_class])
                    if prediction_img is not None:
                        if message_2 is None:
                            prediction_img = cv2.resize(prediction_img, (150, 150))
                            frame[10:160, -160:-10] = prediction_img
                        else:
                            prediction_img = cv2.resize(prediction_img, (150, 150))
                            frame[80:230, -160:-10] = prediction_img
            cv2.imshow("Game Setup", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.25)
        cap.release()
        cv2.destroyAllWindows()
        last_n_prediction = predictions[-9:] if len(predictions) >= 9 else predictions
        majority_vote = Counter(last_n_prediction).most_common(1)[0][0] if last_n_prediction else None
        print(f"Majority Vote Prediction: {majority_vote}")
        return majority_vote

    def run_pipeline(self):
        image_map_1 = {1: r"images\pic1.jpg", 2: r"images\pic2.jpg"}
        image_map_2 = {1: r"images\pic3.jpg", 2: r"images\pic4.jpg"}

        while True:
            first_prediction = self.capture_and_predict(self.model1, image_map_1, "Choose number of players")
            if first_prediction is None:
                print("Retrying first prediction...")
                continue

            if first_prediction == 0:
                print("Zero players selected. Restarting the process...")
                continue

            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open video stream.")
                return

            while True:
                ret, frame = cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)
                second_prediction = self.capture_and_predict(self.model2, image_map_2, f"You chose {first_prediction}" f" player/s", "Fist to Confirm, Palm to Restart")
                if second_prediction is None:
                    continue
                if second_prediction == 1:
                    cv2.destroyAllWindows()
                    self.final_prediction = first_prediction
                    self.prediction_ready.set()
                    return
                else:
                    cv2.destroyAllWindows()
                    break

    def get_prediction(self):
        self.prediction_ready.wait()
        return self.final_prediction


def process_hand():
    model1_path = r"C:\Users\ostr1\PycharmProjects\ai_course\image_processing_full\svm_12_big_model.pkl"
    model2_path = r"C:\Users\ostr1\PycharmProjects\ai_course\image_processing_full\svm_pf_big_model.pkl"

    app = VideoCaptureApp(model1_path, model2_path)
    threading.Thread(target=app.run_pipeline, daemon=True).start()
    return app.get_prediction()


if __name__ == "__main__":
    final_result = process_hand()
    print("Final Prediction:", final_result)
