import cv2 as cv

from .base import Lens


class CamLens(Lens):
    """Simple Lens to display the webcam on the screen."""

    def __init__(self, frame_name='webcam'):
        self.frame = frame_name

    def show(self, rays):
        frame = rays[self.frame]

        if frame is not None:
            cv.imshow(str(self.__class__), frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                raise Exception("Interrupted.")  #TODO handle this differently

    def __del__(self):
        # When everything is done, release the capture
        cv.destroyAllWindows()

