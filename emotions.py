import os
import cv2 as cv

from emotion_recognition import EmotionRecognition
from mirror import Shard, CamLens
from memory import CSVMemory

from config import DEVICE, EMOTIONLOG


class EmotionShard(Shard):

    name = 'emotions'

    def __init__(self, device=DEVICE, logfile=EMOTIONLOG):
        self.recognition = EmotionRecognition(device=device)
        self.classes = self.recognition.emotions
        self.memory = CSVMemory(logfile=logfile)

        self.state = None

    def reflect(self, rays):
        if 'webcam' in rays:
            results = self.recognition.recognize(rays['webcam'])
            #results = self.recognition.show_emotions(rays['webcam'], return_type='BGR')
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

            #if return_type == 'RGB':
            #    return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            rays[self.frame] = frame
        super().show(rays)


