import re


def select_regex(txt, regex=r"Conclusie:(.*?)DISCLAIMER"):
    if not txt:
        return None
    txt = str(txt).replace("\n", "").replace("\t", "")
    item = None
    list = []
    for item in re.finditer(regex, txt):
        list.append(txt[item.start(): item.end()])
    if item is None:
        return "NOT_FOUND " + str(regex)
    return "\n".join(list)
