from types import NoneType


JSON_SUPPORTED_TYPES = [str, int, float, bool, NoneType]


def formatJsonLikeObj(obj: tuple | dict | list):
    """DEPRECATED/NOT NEEDED! Experimental object expander

    Args:
        obj (tuple | dict | list): The object to expand

    Returns:
        list[str]: The expanded object
    """
    st = str(obj)
    if len(st) < 20:
        return [st]

    new = []
    line = ""
    indents = 0
    type_symbol = False  # I mean this: < or >; <=True and >=False
    comma_newline = True
    for c in st:
        if c in "({[":
            if not type_symbol:
                indents += 1
                if line != "":
                    new.append(("    " * (indents - 1)) + line)
                new.append(("    " * (indents - 1) + c))
                line = ""
            else:
                line += c
            continue
        elif c in "]})":
            if not type_symbol:
                new.append("    " * indents + line)
                line = ""
                indents -= 1
            comma_newline = False
        if c == "<":
            type_symbol = True
        elif c == ">":
            type_symbol = False
        line += c
        if c == "," and comma_newline:
            new.append("    " * indents + line)
            line = ""
        comma_newline = True
    if line != "":
        new.append(line)

    return new


def replacePythonObjInJsonLike(obj: list | dict | tuple):
    result = obj.copy()
    del obj

    def iterate_list(l):
        for index, item in enumerate(l):
            if type(item) in [list, tuple]:
                iterate_list(item)
            elif type(item) == dict:
                iterate_dict(item)
            elif not type(item) in JSON_SUPPORTED_TYPES:
                l[index] = str(item)

    def iterate_dict(d):
        for key in d:
            if type(d[key]) in [list, tuple]:
                iterate_list(d[key])
            elif type(d[key]) == dict:
                iterate_dict(d[key])
            elif not type(d[key]) in JSON_SUPPORTED_TYPES:
                d[key] = str(d[key])

    if type(result) == dict:
        iterate_dict(result)
    else:
        iterate_list(result)

    return result
