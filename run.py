# Based on https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
# and https://pypi.org/project/facial-emotion-recognition/
import cv2

from emotion_recognition import EmotionRecognition


er = EmotionRecognition(device='cpu')

cap = cv2.VideoCapture(0)


while(True):
    # Capture video frame-by-frame
    ret, frame = cap.read()
    # frame is now a numpy array with the current frame captured by the webcam

    # Process stuff here
    frame = er.show_emotions(frame, return_type='BGR')

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
