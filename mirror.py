import logging
import cv2 as cv
import time
import datetime

from abc import ABC, abstractmethod

from memory import ImageMemory, CSVMemory


class Shard(ABC):
    """Shards are components of a Mirror.

    Initialize one to catch and reflect particular Rays of Behavior."""

    def __init__(self):
        pass

    @abstractmethod
    def reflect(self, rays: dict):
        """Update and return the current state."""
        pass

    @abstractmethod
    def memorize(self, id_):
        """Memorize the current state."""
        pass


class CamShard(Shard):

    name = "webcam"

    def __init__(self, cam_id=0, **memory_kwargs):
        self.capture = cv.VideoCapture(cam_id)

        if 'logdir' in memory_kwargs:
            self.memory = ImageMemory(**memory_kwargs)
        else:
            logging.warning("Memory not activated for Shard '%s'."%self.name)
            self.memory = None

    def reflect(self, rays: dict):
        ret, frame = self.capture.read()
        self.state = frame
        return self.state

    def memorize(self, id_):
        if self.memory is not None:
            self.memory.memorize(self.state, id_=id_)

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


class Mirror:
    """Instantiate a Mirror.

    Mirrors can be used to reflect your behavior back at you.

    They can be seen as containers for Shards followed by a Lens,
    where each Shard in a Mirror can catch and reflect particular Rays of behavior
    and the Lens is used to make certain parts observable."""

    def __init__(self, logfile, shards: list, lens: Lens, timestep=1.):
        self.shards = shards
        self.lens = lens
        self.timestep = timestep
        self.memory = CSVMemory(logfile)

        self.current_id = 0
        #TODO might want to start somewhere else; or make it based on datetime anyway

    def reflect(self, rays={}):
        """Reflect the current state of affairs."""
        for shard in self.shards:
            rays[shard.name] = shard.reflect(rays)
        return rays

    def memorize(self):
        """Memorize the current state."""
        info = {'timestamp': datetime.datetime.now().isoformat()}
        #TODO not sure we want to store all of this for each time step
        info['shards'] = [{'name': shard.name, 'class': str(shard.__class__)} for shard in self.shards]
        info['timestep'] = self.timestep
        self.memory.memorize(id_=self.current_id, content=info)

        for shard in self.shards:
            shard.memorize(id_=self.current_id)

        self.current_id += 1

    def remember(self, **kwargs):
        """Retrieve particular states from memory."""
        memory = {name: shard.remember(**kwargs) for name,shard in self.shards.items()}
        #TODO might want to organize this differently (like by datetime) to make things more convenient
        return memory

    def run(self, memorize=False):
        logging.info("Activating the Mirror.")

        try:
            while(True):
                t1 = time.time()

                rays = self.reflect()

                if memorize:
                    self.memorize()

                self.lens.show(rays)

                # Wait a bit if we are too fast
                t2 = time.time()
                if t2-t1 < self.timestep:
                    time.sleep(self.timestep - (t2-t1))
        finally:
            logging.info("Deactivating the Mirror.")


if __name__=='__main__':
    import logger
    from emotions import EmotionShard, EmotionLens
    from config import MIRRORLOG

    shards = [CamShard(logdir='logs/test/'), EmotionShard()]
    mirror = Mirror(shards=shards, lens=EmotionLens(), timestep=1., logfile=MIRRORLOG)
    mirror.run(memorize=True)
