import unittest

from nlp_datau.index_to_json import IndexToJson
from nlp_datau.xml_to_index import XmlToIndex

# elasticsearch index (start elasticsearch with docker-compose)
es_index = "xml-index"


class TestIndexMethods(unittest.TestCase):

    # convert xml documents to json and index in elasticsearch
    def test_xml_to_index(self):
        # download MEANTIME corpus here: http://www.newsreader-project.eu/results/data/wikinews/
        directory_in_str = "/Users/sanderputs/Data/Corpora/MEANTIME/meantime_newsreader_english_raw_NAF/corpus_gm"
        extension = ".naf"
        # xml configuration using json dot notation
        field_id = "NAF.nafHeader.public.@publicId"
        # index directory
        XmlToIndex().iterate_xml_dir(directory_in_str, extension=extension, es_index=es_index, field_id=field_id)

    # write snippets of matching documents into doccano json format for annotation
    def test_index_to_doccano_json(self):

        model = "en_core_web_sm"
        index_to_json = IndexToJson(model)

        directory_out_str = '../../data/snippet.json'
        field_text = "NAF.raw"
        query_string = IndexToJson.get_query_string(field_text, "Ford")
        docs = index_to_json.get_docs(es_index, field_text, query_string)

        pattern_terms = ["Ford"]
        index_to_json.doccano_snippet_training_out(docs, pattern_terms, directory_out_str)


if __name__ == '__main__':
    unittest.main()