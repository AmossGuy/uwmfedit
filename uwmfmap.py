import random

class UwmfMap:
    def __init__(self):
        self.tilesize = 64
        self.data = [random.choices([-1, 0], k=10) for i in range(10)]
