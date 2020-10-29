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
        self.memory = None
        self.state = None

    @abstractmethod
    def reflect(self, rays: dict):
        """Update and return the current state."""
        pass

    def memorize(self, id_):
        """Memorize the current state."""
        if self.memory is not None and self.state is not None:
            self.memory.memorize(self.state, id_=id_)

    def remember(self, id_):
        if self.memory is not None:
            return self.memory.remember(id_=id_)
        else:
            return None


class CamShard(Shard):

    name = "webcam"

    def __init__(self, cam_id=0, **memory_kwargs):
        self.capture = cv.VideoCapture(cam_id)

        if 'logdir' in memory_kwargs:
            self.memory = ImageMemory(**memory_kwargs)
        else:
            logging.warning("Memory not activated for Shard '%s'."%self.name)
            self.memory = None
        self.state = None

    def reflect(self, rays: dict):
        ret, frame = self.capture.read()
        self.state = frame
        return self.state

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
        frame = rays[self.frame]

        if frame is not None:
            cv.imshow(str(self.__class__), frame)

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

        # Figure out the next ID
        ids = [int(id_) for id_ in self.memory.remember().keys()]
        if len(ids)>0:
            self.current_id = max(ids)+1

    def reflect(self, rays={}):
        """Reflect the current state of affairs."""
        for shard in self.shards:
            rays[shard.name] = shard.reflect(rays)
        return rays

    def memorize(self, blocked_shards=[]):
        """Memorize the current state."""
        info = {'timestamp': datetime.datetime.now().isoformat()}
        info['shards'] = []
        info['timestep'] = self.timestep

        for shard in self.shards:
            if shard.name in blocked_shards:
                continue

            shard.memorize(id_=self.current_id)
            info['shards'].append({'name': shard.name, 'class': str(shard.__class__)})

        self.memory.memorize(id_=self.current_id, content=info)

        self.current_id += 1

    def remember(self, from_date=None, to_date=None):
        """Retrieve particular states from memory."""
        info = self.memory.remember(from_date=from_date, to_date=to_date)
        ids = sorted(list(info.keys()))

        memory = []
        for id_ in ids:
            snippet = {shard.name: shard.remember(id_=id_) for shard in self.shards}
            snippet['timestamp'] = info[id_]['timestamp']
            memory.append(snippet)
        return memory

    def dream(self, from_date=None, to_date=None):
        """Re-run an older sequence of states."""
        logging.info("Mirror starting to dream.")

        try:
            for rays in self.remember(from_date=from_date, to_date=to_date):
                t1 = time.time()

                self.lens.show(rays)

                # Wait a bit if we are too fast
                t2 = time.time()
                if t2-t1 < self.timestep:
                    time.sleep(self.timestep - (t2-t1))
        finally:
            logging.info("Waking up from the dream.")

    def run(self, memorize=False, memory_blocks=[]):
        """Run the Mirror.

        Arguments:
        - memorize: If True, states of Shards are memorized
        - memory_blocks: Iterable of functions, where each function
            takes the currently reflected Rays and outputs names of Shards
            which should not memorize the current state.
        """
        logging.info("Activating the Mirror.")

        try:
            while(True):
                t1 = time.time()

                rays = self.reflect()

                if memorize:
                    blocked_shards = []
                    for block in memory_blocks:
                        blocked_shards.extend(block(rays))

                    self.memorize(blocked_shards=set(blocked_shards))

                if self.lens is not None:
                    self.lens.show(rays)

                # Wait a bit if we are too fast
                t2 = time.time()
                if t2-t1 < self.timestep:
                    time.sleep(self.timestep - (t2-t1))
        finally:
            logging.info("Deactivating the Mirror.")


class CountdownBlock:

    def __init__(self, frequencies: dict, classes, blocking_shards: list, base_frequency=1):
        self.frequencies = frequencies
        self.base_frequency = base_frequency
        self.countdowns = {c: self.frequencies[c] if c in self.frequencies else self.base_frequency
                            for c in classes}
        self.block = blocking_shards

    def apply(self, rays):
        #TODO this stuff shouldn't be hardcoded for a particular shard
        c = rays['emotions'][0]['emotion']

        if self.countdowns[c]>1:
            self.countdowns[c] -= 1
            return self.block
        else:
            self.countdowns[c] = self.frequencies[c] if c in self.frequencies else self.base_frequency
            return []


if __name__=='__main__':
    import logger
    from emotions import EmotionShard, EmotionLens
    from behavior import WindowShard, ScreenShard
    from faces import FaceShard
    from config import MIRRORLOG, WINDOWLOG, SCREENSHOT_DIR, SCREENSHOT_RESOLUTION, TIMESTEP

    emotion_shard = EmotionShard()
    #shards = [CamShard(logdir='logs/webcam/'), FaceShard('logs/faces/'), emotion_shard]
    shards = [CamShard(), FaceShard('logs/faces/'), emotion_shard]

    # Viewing live
    #mirror = Mirror(shards=shards, lens=EmotionLens(), timestep=0., logfile=MIRRORLOG)
    #mirror.run(memorize=False)

    # Logic to not remember everything in each step
    cam_block = CountdownBlock(blocking_shards=['webcam'], classes=emotion_shard.classes,
                                frequencies={'neutral': 20})
    screenshot_block = CountdownBlock(blocking_shards=['screenshot'], classes=emotion_shard.classes,
                                      frequencies={'neutral': 50}, base_frequency=2)

    # Logging
    #shards.append(WindowShard(logfile=WINDOWLOG))
    #shards.append(ScreenShard(logdir=SCREENSHOT_DIR, resolution=SCREENSHOT_RESOLUTION))
    mirror = Mirror(shards=shards, lens=None, timestep=TIMESTEP, logfile=MIRRORLOG)
    #mirror.run(memorize=True, memory_blocks=[cam_block.apply, screenshot_block.apply])
    mirror.run(memorize=True)

    # Dreaming
    #mirror = Mirror(shards=shards, lens=EmotionLens(), timestep=.5, logfile=MIRRORLOG)
    #mirror.dream(from_date=datetime.datetime(year=2020, month=10, day=29, hour=12))
