import random

class UwmfMap:
    def __init__(self):
        self.tilesize = 64
        self.width = 10
        self.height = 10
        self.data = [random.choice([-1, 0]) for i in range(self.width*self.height)]
