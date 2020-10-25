import json
import datetime
import logging
import numpy as np

from config import *


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

def make_logline(results, id_):
    now = datetime.datetime.now().isoformat()
    return str(id_)+','+now+','+json.dumps(replace_float32(results))+'\n'


if __name__=='__main__':
    import os
    import cv2
    import time
    from PIL import Image

    from emotion_recognition import EmotionRecognition
    from behavior import get_active_window_info, take_screenshot

    import logger

    er = EmotionRecognition(device='cpu')

    cap = cv2.VideoCapture(0)

    # Figure out the most recent ID so far
    id_ = 0
    if os.path.isfile(EMOTIONLOG):
        with open(EMOTIONLOG, 'r') as f:
            for line in f:
                if len(line.strip())>0:
                    id_ = int(line.split(',')[0])+1

    logging.info("Starting to log ...")
    try:
        while(True):
            t1 = time.time()

            # Capture video frame-by-frame
            ret, frame = cap.read()
            # frame is now a numpy array with the current frame captured by the webcam

            window_info = get_active_window_info()

            results = er.recognize(frame)

            if len(results):
                logging.info(str(results))
                line = make_logline(results, id_)
                with open(EMOTIONLOG, 'a') as f:
                    f.write(line)

                # Sometimes we even want a screenshot
                if True: #TODO replace by some criterion
                    take_screenshot(os.path.join(SCREENSHOT_DIR, '%d.jpg'%id_), resolution=SCREENSHOT_RESOLUTION)

                # Log behavior too (if info is available)
                if window_info is not None:
                    logging.info(str(window_info))
                    line = make_logline(window_info, id_)
                    with open(BEHAVIORLOG, 'a') as f:
                        f.write(line)

                # Store some of the cam captures as well
                if True: #TODO replace by some criterion
                    for ix,r in enumerate(results):
                        face = frame[r['position'][1]:r['position'][3], r['position'][0]:r['position'][2]]
                        cv2.imwrite(os.path.join(CAMSHOT_DIR, '%d_%d.png' % (id_, ix)), face) 

                id_ += 1

            # Wait a bit if we are too fast
            t2 = time.time()
            if t2-t1 < TIMESTEP:
                time.sleep(TIMESTEP-(t2-t1))

    finally:
        logging.info("Stopping log.")

        # When everything is done, release the capture
        cap.release()
