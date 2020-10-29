import logging
import time
import datetime

from memory import CSVMemory
from lenses import Lens


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

