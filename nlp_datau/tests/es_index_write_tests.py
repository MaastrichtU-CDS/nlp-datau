import unittest
import pandas

from nlp_datau.index_to_json import IndexToJson
from nlp_datau.index_to_xlsx import IndexToXlsx
from nlp_datau.xml_to_index import XmlToIndex

# elasticsearch index (start elasticsearch with docker-compose)
es_index = "xml-mumc-index"


class TestIndexMethods(unittest.TestCase):

    # convert xml documents to json and index in elasticsearch
    def test_xml_to_index(self):
        # download MEANTIME corpus here: http://www.newsreader-project.eu/results/data/wikinews/
        # directory_in_str = "/Users/sanderputs/Data/Corpora/MEANTIME/meantime_newsreader_english_raw_NAF/corpus_gm"
        directory_in_str = '/Users/sanderputs/Data/Research/XML-data'
        extension = ".xml"
        # xml configuration using json dot notation
        field_id = "ClinicalDocument.setId.@extension"
        # index directory
        XmlToIndex().iterate_xml_dir(directory_in_str, extension=extension, es_index=es_index, field_id=field_id)

        # convert xml documents to json and index in elasticsearch
    def test_mumc_xml_to_index(self):
        # download MEANTIME corpus here: http://www.newsreader-project.eu/results/data/wikinews/
        # directory_in_str = "/Users/sanderputs/Data/Corpora/MEANTIME/meantime_newsreader_english_raw_NAF/corpus_gm"
        directory_in_str = '/Users/sanderputs/Data/Research/Longembolie28-02-2020'
        extension = ".xml"
        # xml configuration using json dot notation
        field_id = "ClinicalDocument.setId.@extension"

        mumc_whitelist_dict = {
            "text": {
                "field": "ClinicalDocument.component.structuredBody.component.section.entryRelationship.observationMedia.value.#text",
                "type": "base64"
            }
        }
        mumc_whitelist_dict = {
            "text": {
                "field": "ClinicalDocument.component.structuredBody.component.section.text",
                "type": "xml",
                "xml-field": "getReportTextByAccessionnrResult.REPORT.REPORT_BODY.TEXT",
                "start-line": "Verslagstatus:",
                "end-line": "Met collegiale groet,"
            }
        }


        # index directory
        XmlToIndex().iterate_xml_dir(
            directory_in_str,
            extension=extension,
            es_index=es_index,
            field_id=field_id,
            whitelist_dict=mumc_whitelist_dict)



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

    # merge excel docs
    def test_merge_excel(self):

        id_column = "Accessionnr"
        source_xlsx = "/Users/sanderputs/Data/Research/Longembolie/Longembolie - tekstsearch.xlsx"
        result_xlsx = "/Users/sanderputs/Data/Research/Longembolie/Longembolie - tekstsearch - result.xlsx"

        field_map = {"text": "text"}

        df_input = pandas.read_excel(source_xlsx, header=0)
        to_xlsx = IndexToXlsx(es_index, es_host="doccano-dataset-tools-es01")
        result_df = to_xlsx.merge(df_input, id_column, field_map=field_map)
        result_df.to_excel(result_xlsx)




if __name__ == '__main__':
    unittest.main()