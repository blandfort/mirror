import os
import logging
import cv2 as cv

from emotion_recognition import EmotionRecognition
from shards import Shard
from lenses import CamLens
from memory import CSVMemory


class EmotionShard(Shard):

    name = 'emotions'

    def __init__(self, device='cpu', logfile=None):
        self.recognition = EmotionRecognition(device=device)
        self.classes = self.recognition.emotions

        if logfile is not None:
            self.memory = CSVMemory(logfile=logfile)
        else:
            logging.warning("Memory not activated for Shard '%s'."%self.name)
            self.memory = None

        self.state = None

    def reflect(self, rays):
        if 'faces' in rays:
            results = []
            for face in rays['faces']:
                result = self.recognition.run_on_face(face['image'])
                result['position'] = face['bounding_box']
                results.append(result)
            self.state = results
            return self.state
        if 'webcam' in rays:
            results = self.recognition.run(rays['webcam'])
            self.state = results
            return self.state
        else:
            raise Exception("Need webcam capture to detect emotions!")


class EmotionLens(CamLens):

    def __init__(self, frame_name='webcam', emotion_name='emotions'):
        self.frame = frame_name
        self.emotions = emotion_name

    def show(self, rays):
        frame = rays[self.frame]

        if frame is not None:
            f_h, f_w, c = frame.shape

            detection = rays[self.emotions]

            for result in detection:
                x1, y1, x2, y2 = result['position']
                emotion = result['emotion']
                score = result['score']

                frame = cv.rectangle(frame, (x1, y1), (x2, y2), color=[0, 255, 0], thickness=1)
                frame = cv.rectangle(frame, (x1, y1 - int(f_h*0.03125)), (x1 + int(f_w*0.21), y1), color=[0, 255, 0], thickness=-1)
                frame = cv.putText(frame, text=emotion+' (%0.2f)'%score, org=(x1 + 5, y1 - 3), fontFace=cv.FONT_HERSHEY_PLAIN,
                                   color=[0, 0, 0], fontScale=1, thickness=1)

            rays[self.frame] = frame
        super().show(rays)


