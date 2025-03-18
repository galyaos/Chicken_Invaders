import numpy as np
import cv2


class ForegroundSegmenter:
    def __init__(self):
        self.bboxes = []
        self.last_bboxes = []

    def run_kmeans(self, image, scale=0.15):
        if image is None:
            raise ValueError("Error: image is None. Check the video source.")
        if not isinstance(image, np.ndarray):
            raise TypeError(f"Error: Expected numpy array but got {type(image)}")
        small_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        lab = cv2.cvtColor(small_image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        reshaped = small_image.reshape((-1, 3)).astype(np.float32)
        k = 2
        _, labels, _ = cv2.kmeans(reshaped, k, None,
                                  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
                                  10, cv2.KMEANS_RANDOM_CENTERS)
        labels = labels.reshape(small_image.shape[:2])
        if np.mean(l[labels == 0]) > np.mean(l[labels == 1]):
            mask = np.uint8(labels == 1) * 255
        else:
            mask = np.uint8(labels == 0) * 255
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        return mask

    def segment_foreground(self, image, num_bodies=2):
        mask = self.run_kmeans(image)
        new_bboxes = self.find_bodies(mask, num_bodies)
        if new_bboxes:
            self.bboxes = new_bboxes
            self.last_bboxes = self.bboxes
        return self.last_bboxes

    def find_bodies(self, mask, num_bodies=2):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return []
        largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:num_bodies]
        return [cv2.boundingRect(contour) for contour in largest_contours]