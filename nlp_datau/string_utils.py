import re


def select_regex(txt, regex=r"Conclusie:(.*?)DISCLAIMER"):
    if not txt:
        return None
    txt = str(txt).replace("\n", "").replace("\t", "")
    iter = re.finditer(regex, txt)
    list = []
    for item in iter:
        list.append(txt[item.start(): item.end()])
    return "\n".join(list)
