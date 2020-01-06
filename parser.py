import string
import re

class Parser:
    def __init__(self, buffer):
        self.buffer = buffer
        self.lasttokenend = 0
    def gettoken(self):
        scan = self.lasttokenend

        if scan == len(self.buffer):
            return None

        identifer_start = string.ascii_letters + "_"
        identifer_continue = identifer_start + string.digits

        while True:
            if self.buffer[scan].isspace():
                scan += 1
            elif self.buffer[scan] in identifer_start:
                t = self.buffer[scan]
                scan += 1
                while self.buffer[scan] in identifer_continue:
                    t += self.buffer[scan]
                    scan += 1
                self.lasttokenend = scan
                return t
            elif self.buffer[scan] in "{}=;,":
                scan += 1
                self.lasttokenend = scan
                return self.buffer[scan - 1]
            elif self.buffer[scan] == '"':
                t = self.buffer[scan]
                scan += 1
                while self.buffer[scan] != '"':
                    if self.buffer[scan] == "\\":
                        t += self.buffer[scan] + self.buffer[scan+1]
                        scan += 2
                    else:
                        t += self.buffer[scan]
                        scan += 1
                t += self.buffer[scan]
                scan += 1
                self.lasttokenend = scan
                return t
            else:
                zeroregex  = re.compile(r"[+-]?0")
                intregex1  = re.compile(r"[+-]?[1-9][0-9]*")
                intregex2  = re.compile(r"0[0-7]+")
                intregex3  = re.compile(r"0x[0-9A-Fa-f]+")
                floatregex = re.compile(r"[+-]?[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?")

                for i in (floatregex, zeroregex, intregex1, intregex2, intregex3):
                    match = i.match(self.buffer, scan)
                    if match is not None:
                        self.lasttokenend = match.end()
                        return match.group()

                raise Exception

if __name__ == "__main__":
    f = open(r"../textmap.txt", "r", encoding="ascii") # Use ASCII encoding because I don’t feel like dealing with Unicode yet.
    s = f.read()
    f.close()

    p = Parser(s)

    while True:
        t = p.gettoken()
        if t is None:
            break
        else:
            print(t)
