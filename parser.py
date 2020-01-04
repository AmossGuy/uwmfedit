import string

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
                raise Exception

if __name__ == "__main__":
    f = open(r"C:\Users\User\Downloads\TEXTMAP.txt", "r")
    s = f.read()
    f.close()

    p = Parser(s)

    while True:
        t = p.gettoken()
        if t is None:
            break
        else:
            print(t)
