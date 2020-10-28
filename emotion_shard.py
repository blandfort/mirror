import os

from mirror import Shard
from emotion_recognition import EmotionRecognition
from config import DEVICE, EMOTIONLOG


def make_logline(results, id_):
    now = datetime.datetime.now().isoformat()
    return str(id_)+','+now+','+json.dumps(replace_float32(results))+'\n'


class EmotionShard(Shard):

    name = 'emotions'

    def __init__(self, device=DEVICE, logfile=EMOTIONLOG):
        self.recognition = EmotionRecognition(device=device)

        #TODO this logging with ID stuff doesn't seem clean, do this differently
        # Figure out the most recent ID so far
        self.current_id = 0
        if os.path.isfile(logfile):
            with open(logfile, 'r') as f:
                for line in f:
                    if len(line.strip())>0:
                        self.current_id = int(line.split(',')[0])+1

        self.state = None

    def reflect(self, rays):
        if 'webcam' in rays:
            results = self.recognition.recognize(rays['webcam'])
            #results = self.recognition.show_emotions(rays['webcam'], return_type='BGR')
            self.state = results
            return self.state
        else:
            raise Exception("Need webcam capture to detect emotions!")

    def memorize(self):
        line = make_logline(self.state, self.current_id)
        with open(self.logfile, 'a') as f:
            f.write(line)

        self.current_id += 1
