from pathlib import Path

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

if __name__ == "__main__":
    print(readvgahead(Path("~/.config/ecwolf/vgahead.wl6").expanduser()))
    print(readvgadict(Path("~/.config/ecwolf/vgadict.wl6").expanduser()))
