import os
import logging

from emotion_recognition import EmotionRecognition

from shards import Shard
from memory import CSVMemory


class EmotionShard(Shard):

    name = 'emotions'

    def __init__(self, model_path, logfile=None, **kwargs):
        """Initialize a Shard to analyze emotions from the webcam stream.

        kwargs are passed to emotion_recognition.EmotionRecognition."""
        self.recognition = EmotionRecognition(model_path=model_path, **kwargs)
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

