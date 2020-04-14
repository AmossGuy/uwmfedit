import wx
from pathlib import Path
import struct

def readvgahead(path):
    with open(path, "rb") as vgahead:
        l = []
        while True:
            element = vgahead.read(3)
            if len(element) == 0:
                break
            l.append(element[0] + element[1]*0x100 + element[2]*0x10000)
    return l

def readvgadict(path):
    with open(path, "rb") as vgadict:
        l = []
        while True:
            element = vgadict.read(4)
            if len(element) == 0:
                break
            l.append((element[0]+element[1]*0x100, element[2]+element[3]*0x100))
    return l

def readvswap(path):
    with open(path, "rb") as vswap:
        numchunks, spritestart, soundstart = struct.unpack("<3H", vswap.read(6))
        chunksheader = vswap.read(6*numchunks)
        chunks = []
        for i in range(0, spritestart):
            pos = struct.unpack("<I", chunksheader[i*4:i*4+4])[0]
            size = struct.unpack("<H", chunksheader[i*2+4*numchunks:i*2+4*numchunks+2])[0]
            vswap.seek(pos)
            datac = vswap.read(size)
            datar = [None] * 64 * 64
            for x in range(64):
                for y in range(64):
                    datar[x+y*64] = datac[x*64+y]
            datar = bytes(datar)
            chunks.append(datar)
    return chunks

if __name__ == "__main__":
    #print(readvgahead(Path("~/.config/ecwolf/vgahead.wl6").expanduser()))
    #print(readvgadict(Path("~/.config/ecwolf/vgadict.wl6").expanduser()))
    xes = readvswap(Path("~/.config/ecwolf/vswap.wl6").expanduser())
    for pos in range(len(xes)):
        x = xes[pos]
        b = b""
        for c in x:
            b += bytes([c, c, c])
        i = wx.Image(64, 64, b)
        i.SaveFile("out{}.png".format(pos), wx.BITMAP_TYPE_PNG)
