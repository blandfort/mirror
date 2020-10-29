
class CountdownBlock:

    def __init__(self, frequencies: dict, classes, blocking_shards: list, base_frequency=1):
        self.frequencies = frequencies
        self.base_frequency = base_frequency
        self.countdowns = {c: self.frequencies[c] if c in self.frequencies else self.base_frequency
                            for c in classes}
        self.block = blocking_shards

    def apply(self, rays):
        #TODO this stuff shouldn't be hardcoded for a particular shard
        if len(rays['emotions'])<1:
            return []
        c = rays['emotions'][0]['emotion']

        if self.countdowns[c]>1:
            self.countdowns[c] -= 1
            return self.block
        else:
            self.countdowns[c] = self.frequencies[c] if c in self.frequencies else self.base_frequency
            return []

