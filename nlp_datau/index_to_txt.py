import time

from elasticsearch import Elasticsearch
from nlp_datau.data_utils import DataUtils
import logging

logging.basicConfig()
logger = logging.getLogger('index_to_txt')
logger.setLevel(level=logging.INFO)


class IndexToTxt(object):

    def __init__(self, es_index, es_host="localhost"):
        self.es_index = es_index
        self.es = Elasticsearch(host=es_host)

    def get_source_field(self, source, key):
        try:
            return DataUtils.get_json_field_dot_notation(key, source)
        except Exception as e:
            logger.error(e)
        return None

    def write_index(self, file_name, field):

        start_time = time.time()
        doc_count = 0
        with open(file_name, "w") as myfile:

        # declare a filter query dict object
            match_all = {
                "size": 100,
                "query": {
                    "match_all": {}
                }
            }

            # make a search() request to get all docs in the index
            resp = self.es.search(index=self.es_index, body=match_all, scroll='2s')

            # keep track of pass scroll _id
            old_scroll_id = resp['_scroll_id']

            # use a 'while' iterator to loop over document 'hits'
            while len(resp['hits']['hits']):

                # make a request using the Scroll API
                resp = self.es.scroll(
                    scroll_id = old_scroll_id,
                    scroll='2s' # length of time to keep search context
                )

                # check if there's a new scroll ID
                if old_scroll_id != resp['_scroll_id']:
                    print ("NEW SCROLL ID:", resp['_scroll_id'])

                # keep track of pass scroll _id
                old_scroll_id = resp['_scroll_id']

                # print the response results
                print ("\nresponse for index:", self.es_index)
                print ("_scroll_id:", resp['_scroll_id'])
                print ('response["hits"]["total"]["value"]:', resp["hits"]["total"]["value"])

                # iterate over the document hits for each 'scroll'
                for doc in resp['hits']['hits']:
                    myfile.write(self.get_source_field(doc['_source'], field))
                    doc_count += 1
                    print ("DOC COUNT:", doc_count)

            # print the total time and document count at the end
            print ("\nTOTAL DOC COUNT:", doc_count)

            # print the elapsed time
            print ("TOTAL TIME:", time.time() - start_time, "seconds.")