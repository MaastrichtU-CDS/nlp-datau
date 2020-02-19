from elasticsearch import Elasticsearch

import xmltodict
import json
from pathlib import Path

from nlpdatau.data_utils import DataUtils

directory_in_str = "/Users/sanderputs/Data/Corpora/MEANTIME/meantime_newsreader_english_raw_NAF/corpus_gm"

EXTENSION = ".naf"
ID_FIELD = "NAF.nafHeader.public.@publicId"
ES_INDEX = "xml-index"

es = Elasticsearch()


def iterate_xml_dir(directory_in_str):
    pathlist = Path(directory_in_str).glob('**/*' + EXTENSION)
    for path in pathlist:
        path_in_str = str(path)
        with open(path_in_str) as in_file:
            print('read {}', path_in_str)
            xml = in_file.read()
            doc = json.loads(json.dumps(xmltodict.parse(xml)))
            index(doc)


def index(doc):
    print('doc={}', doc)
    print(doc)

    id = DataUtils.get_json_field_dot_notation(ID_FIELD, doc)
    print('id={}', id)

    res = es.index(index=ES_INDEX, id=id, body=doc)
    print(res['result'])



iterate_xml_dir(directory_in_str)