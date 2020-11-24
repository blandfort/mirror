import cv2 as cv
import numpy as np

from lenses import CamLens


class FaceswapLens(CamLens):

    def __init__(self, frame_name='webcam', face_name='faces'):
        self.frame = frame_name
        self.faces = face_name

    def show(self, rays):
        frame = rays[self.frame]

        if frame is not None:
            f_h, f_w, c = frame.shape

            faces = rays[self.faces]

            if len(faces)>1:
                # Bugfix: Changing the frame image changes the face images
                # as well unless we work with copies of the face images.
                faces[0]['image'] = np.copy(faces[0]['image'])
                faces[1]['image'] = np.copy(faces[1]['image'])

                # Put the second face where the first face was and vice versa
                self._swap_faces(frame, faces[0], faces[1])
                self._swap_faces(frame, faces[1], faces[0])

            rays[self.frame] = frame
        super().show(rays)

    def _swap_faces(self, frame, face1, face2):
        x1, y1, x2, y2 = face1['bounding_box']
        if min(face1['image'].shape)<1 or min(face2['image'].shape)<1:
            return frame
        frame[y1:y2, x1:x2] = cv.resize(face2['image'], (x2-x1, y2-y1), interpolation=cv.INTER_CUBIC)
        return frame
