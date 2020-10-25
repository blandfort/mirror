# Based on https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
# and https://pypi.org/project/facial-emotion-recognition/
import numpy as np
import cv2

from emotion_recognition import EmotionRecognition


# NOTE: In that package, had to change the line
# "model_dict = torch.load(os.path.join(os.path.dirname(__file__), 'model', 'model.pkl'))"
# to "model_dict = torch.load(os.path.join(os.path.dirname(__file__), 'model', 'model.pkl'), map_location=self.device)".
# Otherwise, loading the model without having a GPU fails.
# (Unfortunately couldn't find a way to contact the author.)
er = EmotionRecognition(device='cpu')

cap = cv2.VideoCapture(0)


while(True):
    # Capture video frame-by-frame
    ret, frame = cap.read()
    # frame is now a numpy array with the current frame captured by the webcam

    # Process stuff here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame = er.recognize_emotion(frame, return_type='BGR')

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
