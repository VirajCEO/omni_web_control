import cv2
import threading
import numpy as np

class Camera(object):
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()

        self.video_capture = cv2.VideoCapture(0)  # Use the appropriate camera index (0 or 1) if you have multiple cameras
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        thread = threading.Thread(target=self._update, args=())
        thread.daemon = True
        thread.start()

    def _update(self):
        while True:
            with self.lock:
                _, frame = self.video_capture.read()
                if _:
                    self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame
