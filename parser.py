import string
import re

def tokenize(buffer):
    tokentypes = {
        "leftbracket": r"\{",
        "rightbracket": r"}",
        "equals": r"=",
        "semicolon": r";",
        "comma": r",",
        "identifer": r"[A-Za-z][A-Za-z0-9]*",
        "string": r'"([^"\\]|\\.)*"',
        "integer": r"([+-]?0|[+-]?[1-9][0-9]*|0[0-7]+|0x[0-9A-Fa-f]+)(?!\.)",
        "float": r"[+-]?[0-9]+\.[0-9]*([eE][+-]?[0-9]+)?",
        "comment": r"//.*$|/\*(.|$)*\*/",
        "whitespace": r"\s+"
    }

    regex = re.compile("|".join("(?P<{}>{})".format(*item) for item in tokentypes.items()) + "|(?P<mismatch>.)", re.MULTILINE)

    for match in regex.finditer(buffer):
        kind = match.lastgroup
        if kind == "mismatch":
            raise Exception
        elif kind not in ("comment", "whitespace"):
            yield kind, match.group()

def parse(tokens):
    begin = True
    block = None
    state = "global"

    for token in tokens:
        yield token[0], token[1], state
        if state == "global":
            if token[0] == "identifer" and block != "planemap":
                identifer = token[1]
                state = "begin"
            elif token[0] == "leftbracket" and block == "planemap":
                mapspotfield = 0
                state = "mapspot"
            elif token[0] == "rightbracket" and block != None:
                block = None
            else:
                raise Exception
        elif state == "mapspot":
            if token[0] == "integer":
                state = "mapspotbetween"
            else:
                raise Exception
        elif state == "mapspotbetween":
            if token[0] == "comma":
                mapspotfield += 1
                state = "mapspot"
            elif token[0] == "rightbracket" and mapspotfield in [2, 3]:
                state = "endmapspot"
            else:
                raise Exception
        elif state == "endmapspot":
            if token[0] == "comma":
                state = "global"
            elif token[0] == "rightbracket":
                block = None
                state = "global"
        elif state == "begin":
            if token[0] == "equals" and (begin or block != None):
                state = "assign"
            elif token[0] == "leftbracket" and block == None:
                begin = False
                block = identifer
                state = "global"
            else:
                raise Exception
        elif state == "assign":
            if token[0] in ["identifer", "string", "integer", "float"]:
                state = "endassign"
            else:
                raise Exception
        elif state == "endassign":
            if token[0] == "semicolon":
                state = "global"
            else:
                raise Exception
        else:
            raise Exception

if __name__ == "__main__":
    f = open(r"../textmap.txt", "r", encoding="ascii") # Use ASCII encoding because I don’t feel like dealing with Unicode yet.
    s = f.read()
    f.close()

    p = parse(tokenize(s))

    for i in p:
        print(i)
