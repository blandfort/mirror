import os
import logging
import torch
import torchvision.transforms as transforms
import numpy as np
import cv2 as cv
from facenet_pytorch import MTCNN

from .dataset import FERPlus
from .networks import NetworkBasic


#TODO put the path into some configuration file or pass as argument to init
MODEL_PATH = 'models/own.pt'


class EmotionRecognition(object):
    def __init__(self, device, gpu_id=0):
        assert device == 'cpu' or device == 'gpu',"Need to specify device! ('cpu' or 'gpu')"

        # Set the device according to arguments and what is available
        if torch.cuda.is_available():
            if device == 'cpu':
                logging.warning('Your machine has a GPU. Performance would be better with EmotionRecognition(device=gpu)!')
                self.device = torch.device('cpu')
            if device == 'gpu':
                self.device = torch.device(f'cuda:{str(gpu_id)}')
        else:
            if device == 'gpu':
                logging.warning('No GPU is detected, so cpu is selected as device!')
                self.device = torch.device('cpu')
            if device == 'cpu':
                self.device = torch.device('cpu')

        self.emotions = FERPlus.classes #{0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

        # Model used for emotion recognition (from cropped face images)
        self.network = NetworkBasic(in_c=1, nl=32, out_f=len(self.emotions)).to(self.device)

        # Load the saved state
        model_dict = torch.load(MODEL_PATH, map_location=self.device)
        self.network.load_state_dict(model_dict)
        self.network.eval()

        # Normalization
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((48, 48)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5], std=[0.5])
        ])

        # Model used to detect faces in the video stream
        self.mtcnn = MTCNN(keep_all=True, device=self.device)

    def _predict(self, image):
        """Given an image of a face, return the primary emotion shown in the face."""
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        output = self.network(tensor)
        ps = torch.exp(output).tolist()
        index = np.argmax(ps)
        score = np.amax(output.detach().numpy())

        return self.emotions[index], score

    def run_on_face(self, face):
        gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
        emotion, score = self._predict(gray)

        return {'emotion': emotion, 'score': score}
        

    def run(self, frame):
        """Perform emotion recognition on a single frame and return the results.

        Different from show_emotions(), this method does not return a modified frame."""
        f_h, f_w, c = frame.shape
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        boxes, _ = self.mtcnn.detect(frame)

        results = []
        if boxes is not None:
            for i in range(len(boxes)):
                x1, y1, x2, y2 = int(round(boxes[i][0])), int(round(boxes[i][1])), int(round(boxes[i][2])), int(
                    round(boxes[i][3]))
                emotion, score = self._predict(gray[y1:y2, x1:x2])

                results.append( {'emotion': emotion, 'score': score, 'position': (x1, y1, x2, y2)} )
        return results

    def show(self, frame, return_type='BGR'):
        """Perform emotion recognition on a single frame and show the result
        by returning a modified frame.

        The returned frame has a bounding box around all detected faces
        plus the names of the detected emotions."""
        f_h, f_w, c = frame.shape
        detection = self.recognize(frame)

        for result in detection:
            x1, y1, x2, y2 = result['position']
            emotion = result['emotion']
            score = result['score']

            frame = cv.rectangle(frame, (x1, y1), (x2, y2), color=[0, 255, 0], thickness=1)
            frame = cv.rectangle(frame, (x1, y1 - int(f_h*0.03125)), (x1 + int(f_w*0.21), y1), color=[0, 255, 0], thickness=-1)
            frame = cv.putText(frame, text=emotion+' (%0.2f)'%score, org=(x1 + 5, y1 - 3), fontFace=cv.FONT_HERSHEY_PLAIN,
                               color=[0, 0, 0], fontScale=1, thickness=1)

        if return_type == 'BGR':
            return frame
        if return_type == 'RGB':
            return cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        else:
            raise Exception("Unknown return_type!")
