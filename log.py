import cv2
import json
import datetime
import logging
import numpy as np

from emotion_recognition import EmotionRecognition


LOGFILE = 'logs/emotions.log'
#TODO handle in some config file

def replace_float32(obj):
    """Utility function to recursively convert float32 entries to float,
    so the object can be converted to JSON."""
    if type(obj) is dict:
        r = {}
        for key,value in obj.items():
            if type(value) is np.float32:
                r[key] = float(value)
            elif type(value) in [dict, list, tuple]:
                r[key] = replace_float32(value)
            else:
                r[key] = value
        return r
    elif type(obj) is list or type(obj) is tuple:
        r = []
        for value in obj:
            if type(value) is np.float32:
                r.append(float(value))
            elif type(value) in [dict, list, tuple]:
                r.append(replace_float32(value))
            else:
                r.append(value)
        return r
    else:
        raise Exception("Not implemented!")

def make_logline(results):
    now = datetime.datetime.now().isoformat()
    return now+','+json.dumps(replace_float32(results))+'\n'


if __name__=='__main__':
    er = EmotionRecognition(device='cpu')

    cap = cv2.VideoCapture(0)

    logging.info("Starting to log ...")
    try:
        while(True):
            # Capture video frame-by-frame
            ret, frame = cap.read()
            # frame is now a numpy array with the current frame captured by the webcam

            results = er.recognize(frame)

            if len(results):
                with open(LOGFILE, 'a') as f:
                    f.write(make_logline(results))

    finally:
        logging.info("Stopping log.")

        # When everything is done, release the capture
        cap.release()
