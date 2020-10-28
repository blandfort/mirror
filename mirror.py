import logging
import cv2 as cv
import time

from abc import ABC, abstractmethod


class Shard(ABC):
    """Shards are components of a Mirror.

    Initialize one to catch and reflect particular Rays of Behavior."""

    def __init__(self):
        pass

    @abstractmethod
    def reflect(self, rays: dict):
        """Update and return the current state."""
        pass


class CamShard(Shard):

    name = "webcam"

    def __init__(self, cam_id=0):
        self.capture = cv.VideoCapture(cam_id)

    def reflect(self, rays: dict):
        ret, frame = self.capture.read()
        return frame

    def __del__(self):
        # Release the camera
        self.capture.release()


class Lens(ABC):

    @abstractmethod
    def show(self, rays):
        pass


class CamLens(Lens):
    """Simple Lens to display the webcam on the screen."""

    def __init__(self, frame_name='webcam'):
        self.frame = frame_name

    def show(self, rays):
        cv.imshow(str(self.__class__), rays[self.frame])

        if cv.waitKey(1) & 0xFF == ord('q'):
            raise Exception("Interrupted.")  #TODO handle this differently

    def __del__(self):
        # When everything is done, release the capture
        cv.destroyAllWindows()


class EmotionLens(CamLens):

    def __init__(self, frame_name='webcam', emotion_name='emotions'):
        self.frame = frame_name
        self.emotions = emotion_name

    def show(self, rays):
        frame = rays[self.frame]
        f_h, f_w, c = frame.shape

        detection = rays[self.emotions]

        for result in detection:
            x1, y1, x2, y2 = result['position']
            emotion = result['emotion']
            score = result['score']

            frame = cv.rectangle(frame, (x1, y1), (x2, y2), color=[0, 255, 0], thickness=1)
            frame = cv.rectangle(frame, (x1, y1 - int(f_h*0.03125)), (x1 + int(f_w*0.21), y1), color=[0, 255, 0], thickness=-1)
            frame = cv.putText(frame, text=emotion+' (%0.2f)'%score, org=(x1 + 5, y1 - 3), fontFace=cv.FONT_HERSHEY_PLAIN,
                               color=[0, 0, 0], fontScale=1, thickness=1)

        #if return_type == 'RGB':
        #    return cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        rays[self.frame] = frame
        super().show(rays)


class Mirror:
    """Instantiate a Mirror.

    Mirrors can be used to reflect your behavior back at you.

    They can be seen as containers for Shards followed by a Lens,
    where each Shard in a Mirror can catch and reflect particular Rays of behavior
    and the Lens is used to make certain parts observable."""

    def __init__(self, shards: list, lens: Lens, timestep=1.):
        self.shards = shards
        self.lens = lens
        self.timestep = timestep

    def reflect(self, rays={}):
        """Reflect the current state of affairs."""
        for shard in self.shards:
            rays[shard.name] = shard.reflect(rays)
        return rays

    def memorize(self):
        """Memorize the current state."""
        for shard in self.shards.values():
            shard.memorize()

    def remember(self, **kwargs):
        """Retrieve particular states from memory."""
        memory = {name: shard.remember(**kwargs) for name,shard in self.shards.items()}
        #TODO might want to organize this differently (like by datetime) to make things more convenient
        return memory

    def run(self):
        logging.info("Activating the Mirror.")

        try:
            while(True):
                t1 = time.time()

                rays = self.reflect()

                self.lens.show(rays)

                # Wait a bit if we are too fast
                t2 = time.time()
                if t2-t1 < self.timestep:
                    time.sleep(self.timestep - (t2-t1))
        finally:
            logging.info("Deactivating the Mirror.")


if __name__=='__main__':
    import logger
    from emotion_shard import EmotionShard

    mirror = Mirror(shards=[CamShard(), EmotionShard()], lens=EmotionLens(), timestep=.0)
    mirror.run()
