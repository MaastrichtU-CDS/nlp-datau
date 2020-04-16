import unittest

from nlp_datau.io_utils import txt_from_doc
from nlp_datau.template_parser import create_definition
from nlp_datau.string_utils import select_regex

import pandas

path_in_covid = "C:\\Data\\Research\\COVID-19\\01._corads_standaardverslag_versie 30 maart 2020.docx"
path_out_def = "C:\\Data\\Research\\COVID-19\\01._corads_standaardverslag_versie 30 maart 2020_def.yaml"

path_in_covid_bevinding = "C:\\Data\\Research\\COVID-19\\01._corads_standaardverslag_versie 30 maart 2020 - Bevinding.docx"


class TestIndexMethods(unittest.TestCase):

    # convert xml documents to json and index in elasticsearch
    def test_create_definition_word(self):
        create_definition(path_in_covid, path_out_def)

    def test_regex_select(self):
        regex_conclusion = r"Conclusie:(.*?)DISCLAIMER"
        regex_incidental_findings = r"(?<=Nevenbevindingen:)(.*?)(?=DISCLAIMER)"

        txt = txt_from_doc(path_in_covid_bevinding)
        txt = select_regex(txt, regex_conclusion)
        txt = select_regex(txt, regex_incidental_findings)
        print(txt)