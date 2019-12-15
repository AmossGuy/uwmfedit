import random

class UwmfMap:
    def __init__(self):
        self.tilesize = 64
        self.width = 10
        self.height = 10
        self.data = random.choices([-1, 0], k=self.width*self.height)
