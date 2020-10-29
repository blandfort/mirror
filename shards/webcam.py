import logging
import cv2 as cv

from memory import ImageMemory
from .base import Shard

class CamShard(Shard):

    name = "webcam"

    def __init__(self, cam_id=0, **memory_kwargs):
        self.capture = cv.VideoCapture(cam_id)

        if 'logdir' in memory_kwargs:
            self.memory = ImageMemory(**memory_kwargs)
        else:
            logging.warning("Memory not activated for Shard '%s'."%self.name)
            self.memory = None
        self.state = None

    def reflect(self, rays: dict):
        ret, frame = self.capture.read()
        self.state = frame
        return self.state

    def __del__(self):
        # Release the camera
        self.capture.release()


