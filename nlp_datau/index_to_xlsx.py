
from elasticsearch import Elasticsearch
from nlp_datau.data_utils import DataUtils
import logging

logging.basicConfig()
logger = logging.getLogger('index_to_xlsx')
logger.setLevel(level=logging.INFO)


class IndexToXlsx(object):

    def __init__(self, es_index, es_host="localhost"):
        self.es_index = es_index
        self.es = Elasticsearch(host=es_host)

    def get_source(self, doc_id):
        try:
            return self.get_doc(doc_id)["_source"]
        except Exception as e:
            logger.error(e)
        return None

    def get_source_field(self, source, key):
        try:
            return DataUtils.get_json_field_dot_notation(key, source)
        except Exception as e:
            logger.error(e)
        return None

    def get_doc(self, doc_id):
        return self.es.get(index=self.es_index, id=doc_id)

    def merge(self, df, df_id_column, field_map):
        df['source'] = df.apply(lambda row: self.get_source(row[df_id_column]), axis=1)
        for key in field_map:
            df[key] = df.apply(lambda row: self.get_source_field(row['source'], field_map[key]), axis=1)
        df = df.drop(columns=['source'])
        return df
