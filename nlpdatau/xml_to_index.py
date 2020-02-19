from elasticsearch import Elasticsearch
import xmltodict
import json

from pathlib import Path
from nlpdatau.data_utils import DataUtils

es = Elasticsearch()

class XmlToIndex(object):

    def iterate_xml_dir(self, directory_in_str, extension, es_index, field_id):
        pathlist = Path(directory_in_str).glob('**/*' + extension)
        for path in pathlist:
            path_in_str = str(path)
            with open(path_in_str) as in_file:
                print('read {}', path_in_str)
                xml = in_file.read()
                doc = json.loads(json.dumps(xmltodict.parse(xml)))
                self.index(doc, es_index, field_id)


    def index(self, doc, es_index, field_id):
        print('doc={}', doc)
        print(doc)

        id = DataUtils.get_json_field_dot_notation(field_id, doc)
        print('id={}', id)

        res = es.index(index=es_index, id=id, body=doc)
        print(res['result'])



