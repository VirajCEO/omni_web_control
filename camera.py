import io
import picamera
import threading

class Camera(object):
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()

        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)

        thread = threading.Thread(target=self._update, args=())
        thread.daemon = True
        thread.start()

    def _update(self):
        while True:
            with self.lock:
                stream = io.BytesIO()
                self.camera.capture(stream, format='jpeg')
                self.frame = stream.getvalue()

    def get_frame(self):
        with self.lock:
            return self.frame
