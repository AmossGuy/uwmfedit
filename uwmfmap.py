from collections import namedtuple

class UwmfMap:
    mapspot = namedtuple("mapspot", ["tile", "sector", "zone"])

    def __init__(self):
        self.global_ = {}
        self.blocks = []

    def init_planemap(self, width, height):
        self.planemap = [[None] * width for i in range(height)]

    def fill_mapspot(self, x, y, contents):
        self.planemap[y][x] = contents

    def set_global(self, key, value):
        self.global_[key] = value
