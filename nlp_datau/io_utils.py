import docx2txt


def txt_from_doc(path_in):
    return docx2txt.process(path_in)
