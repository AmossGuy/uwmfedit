import string
import re

def parse(buffer):
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

if __name__ == "__main__":
    f = open(r"../textmap.txt", "r", encoding="ascii") # Use ASCII encoding because I don’t feel like dealing with Unicode yet.
    s = f.read()
    f.close()

    p = parse(s)

    for i in p:
        print(i)
