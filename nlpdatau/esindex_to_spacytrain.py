from elasticsearch import Elasticsearch
from nlpdatau.data_utils import DataUtils
import spacy
import json

from spacy.matcher import PhraseMatcher

model = "en_core_web_sm"
OUT_DIR = "data/doccano"
DATASET_NAME = "TESTSET"

TEXT_FIELD = "NAF.raw"
ES_INDEX = "xml-index"

SNIPPET_MODE = True
snippet_regex = 'Ford'
SNIPPET_PRE = 1
SNIPPET_POST = 1

es = Elasticsearch()


class EsIndexToSpacyTrain(object):

    def __init__(self, model):
        self.nlp = spacy.load(model)


    def get_docs(self, query_string):

        body = {"query": query_string}

        res = es.search(index=ES_INDEX, body=body)
        print("Got %d Hits:" % res['hits']['total']['value'])

        docs = []
        for hit in res['hits']['hits']:
            # print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
            source = hit["_source"]
            text = DataUtils.get_json_field_dot_notation(TEXT_FIELD, source)
            print(text)
            doc = self.nlp(text)
            docs.append(doc)

        return docs


    def snippet_training_out(self, docs, terms, path):

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

            # sents = list(doc.sents)

        with open(path, 'w') as fh:
            for snippet in snippets:
                fh.write(snippet+"\n")


def spacy_training_out(self, path, docs):
        # './../data/train_set.json'
        result = []
        with open(path, 'w') as fh:
            for doc in docs:
                result.append(spacy.gold.docs_to_json(doc))
        fh.write(json.dumps(result)+"\n")


def get_query_string(field, query):
    return {
        "query_string": {
            "query": query,
            "default_field": field
        }
    }






query_string = get_query_string(TEXT_FIELD, "Ford")
terms = ["Ford"]

esIndex = EsIndexToSpacyTrain(model)
docs = esIndex.get_docs(query_string)
esIndex.snippet_training_out(docs, terms, '../data/snippet.json')