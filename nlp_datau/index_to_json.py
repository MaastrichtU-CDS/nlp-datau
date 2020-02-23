from elasticsearch import Elasticsearch
from nlp_datau.data_utils import DataUtils
import spacy
import json

from spacy.matcher import PhraseMatcher

es = Elasticsearch()


class IndexToJson(object):

    def __init__(self, model):
        self.nlp = spacy.load(model)

    def get_docs(self, es_index, field_text, query_string):
        body = {"query": query_string}
        res = es.search(index=es_index, body=body)
        print("Got %d Hits:" % res['hits']['total']['value'])

        docs = []
        for hit in res['hits']['hits']:
            # print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
            source = hit["_source"]
            text = DataUtils.get_json_field_dot_notation(field_text, source)
            print(text)
            doc = self.nlp(text)
            docs.append(doc)
        return docs

    def doccano_snippet_training_out(self, docs, terms, path):
        patterns = [self.nlp.make_doc(text) for text in terms]
        matcher = PhraseMatcher(self.nlp.vocab)
        matcher.add("TerminologyList", None, *patterns)

        snippets = []
        for doc in docs:
            match_start_spans = []
            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                match_start_spans.append(start)
                snippets.append(json.dumps({"text": span.sent.text}))

        with open(path, 'w') as fh:
            for snippet in snippets:
                fh.write(snippet+"\n")

    @staticmethod
    def spacy_training_out(path, docs):
            result = []
            with open(path, 'w') as fh:
                for doc in docs:
                    result.append(spacy.gold.docs_to_json(doc))
            fh.write(json.dumps(result)+"\n")

    @staticmethod
    def get_query_string(field, query):
        return {
            "query_string": {
                "query": query,
                "default_field": field
            }
        }
