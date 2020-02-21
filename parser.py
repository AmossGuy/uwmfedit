import string
import re

import uwmfmap

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
    map_ = uwmfmap.UwmfMap()

    while True:
        try:
            token = next(tokens)
        except StopIteration:
            break

        if token[0] == "identifer":
            g_name = token[1]
            token = next(tokens)
            if token[0] == "leftbracket":
                if g_name.casefold() == "planemap":
                    width = int(map_.global_["width"])
                    height = int(map_.global_["height"])
                    map_.init_planemap(width, height)
                    i = 0
                    while True:
                        token = next(tokens)
                        if token[0] == "leftbracket":
                            token = next(tokens)
                            if token[0] == "integer":
                                msa = token[1]
                                token = next(tokens)
                                if token[0] == "comma":
                                    token = next(tokens)
                                    if token[0] == "integer":
                                        msb = token[1]
                                        token = next(tokens)
                                        if token[0] == "comma":
                                            token = next(tokens)
                                            if token[0] == "integer":
                                                msc = token[1]
                                                map_.fill_mapspot(i%width, i//width, uwmfmap.UwmfMap.mapspot(msa, msb, msc))
                                                token = next(tokens)
                                                if token[0] == "comma":
                                                    token = next(tokens)
                                                    if token[0] == "integer":
                                                        if token[0] == "rightbracket":
                                                            token = next(tokens)
                                                            if token[0] == "comma":
                                                                pass
                                                            elif token[0] == "rightbracket":
                                                                break
                                                            else: raise Exception
                                                        else: raise Exception
                                                    else: raise Exception
                                                elif token[0] == "rightbracket":
                                                    token = next(tokens)
                                                    if token[0] == "comma":
                                                        pass
                                                    elif token[0] == "rightbracket":
                                                        break
                                                    else: raise Exception
                                                else: raise Exception
                                            else: raise Exception
                                        else: raise Exception
                                    else: raise Exception
                                else: raise Exception
                            else: raise Exception
                        else: raise Exception
                        i += 1
                else:
                    block = (g_name, {})
                    map_.blocks.append(block)
                    while True:
                        token = next(tokens)
                        if token[0] == "identifer":
                            b_name = token[1]
                            token = next(tokens)
                            if token[0] == "equals":
                                token = next(tokens)
                                if token[0] in ["identifer", "string", "integer", "float"]:
                                    block[1][b_name] = token[1]
                                    token = next(tokens)
                                    if token[0] == "semicolon":
                                        pass
                                    else: raise Exception
                                else: raise Exception
                            else: raise Exception
                        elif token[0] == "rightbracket":
                            break
                        else: raise Exception
            elif token[0] == "equals":
                token = next(tokens)
                if token[0] in ["identifer", "string", "integer", "float"]:
                    map_.set_global(g_name, token[1])
                    token = next(tokens)
                    if token[0] == "semicolon":
                        pass
                    else: raise Exception
                else: raise Exception
            else: raise Exception
        else: raise Exception
    return map_

if __name__ == "__main__":
    f = open(r"../textmap.txt", "r", encoding="ascii") # Use ASCII encoding because I don’t feel like dealing with Unicode yet.
    s = f.read()
    f.close()

    map_ = parse(tokenize(s))
    print(map_.global_)
    print(map_.blocks)
    print(map_.planemap)
