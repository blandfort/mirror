import os
import cv2 as cv
from facenet_pytorch import MTCNN

from shards import Shard
from memory import ImageMemory


class FaceShard(Shard):
    """Shard to reflect faces captured by the webcam."""

    name = 'faces'

    def __init__(self, logdir=None, device='cpu', extension='png'):
        if logdir is not None:
            self.memory = ImageMemory(logdir=logdir, extension=extension)
        else:
            logging.warning("Memory not activated for Shard '%s'."%self.name)
            self.memory = None
        self.mtcnn = MTCNN(keep_all=True, device=device)

        self.state = None

    def reflect(self, rays):
        if 'webcam' in rays:
            frame = rays['webcam']

            f_h, f_w, c = frame.shape
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            boxes, probs = self.mtcnn.detect(frame)

            faces = []
            if boxes is not None:
                for bbox in boxes:
                    x1, y1, x2, y2 = int(round(bbox[0])), int(round(bbox[1])), int(round(bbox[2])), int(round(bbox[3]))
                    faces.append({'image': frame[y1:y2, x1:x2], 'bounding_box': (x1, y1, x2, y2)})

            self.state = faces
            return self.state
        else:
            raise Exception("Need webcam capture to detect faces!")

    def memorize(self, id_):
        """Memorize the current state."""
        if self.memory is not None and self.state is not None:
            for face in self.state:
                title = '_'.join(map(str, face['bounding_box']))
                self.memory.memorize(face['image'], id_=id_, title=title)

    def remember(self, ids):
        memories = {}
        for id_ in ids:
            memories[id_] = self._remember_id(id_)
        return memories

    def _remember_id(self, id_):
        if self.memory is not None:
            face_images = self.memory.search(startswith=str(id_))

            faces = []
            for face_image in face_images:
                face_id, face_title = os.path.splitext(face_image)[0].split('_', 1)

                face = {'image': self.memory._remember_id(id_=face_id, title=face_title)}
                face['bounding_box'] = list(map(int, face_title.split('_')))
                faces.append(face)
            return faces
        else:
            return None
