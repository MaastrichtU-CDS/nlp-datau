import re
import yaml


def create_definition(txt, path_out):
    create_dict(txt, path_out)


def create_dict(text, path_out, template_regex_curly_brackets=r"\{(.*?)\}", template_regex_square_brackets=r"\[(.*?)\]"):

    lines = text.splitlines()
    template_list = []
    count = 0

    for sent in lines:
        sent_start = 0

        iter = re.finditer(template_regex_curly_brackets, sent)
        for m in iter:
            count = count + 1
            prefix = sent[sent_start: m.start()].replace(":", "").strip()
            template_item = {}
            template_item['id'] = count
            template_item['bracket_type'] = 'curly'
            template_item['text'] = prefix
            template_item['uid'] = ''
            template_item['accepted_values'] = ''
            template_list.append(template_item)
            sent_start = m.end()

    print('length', template_list)

    with open(path_out, 'w') as file:
        documents = yaml.dump(template_list, file, sort_keys=False)


def parse():
    read_config()
    validate_config()
    parse_documents()

def read_config():
    return

def validate_config():
    return


def parse_documents():
    validate_length()


def validate_length():
    return

