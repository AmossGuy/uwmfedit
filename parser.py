import string

class Parser:
    def __init__(self, buffer):
        self.buffer = buffer
        self.lasttokenend = 0
    def gettoken(self):
        scan = self.lasttokenend

        identifer_start = string.ascii_letters + "_"
        identifer_continue = identifer_start + string.digits

        while True:
            if self.buffer[scan].isspace():
                scan += 1
            elif self.buffer[scan] in "{}#$":
                self.lasttokenend = scan + 1
                return self.buffer[scan]
            else:
                raise Exception
