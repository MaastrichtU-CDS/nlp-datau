from json import JSONDecodeError
import logging
import requests


class SpacyClient(object):

    def __init__(self, url, models):
        self.url = url
        self.models = models

    def annotate(self, text, identifier, document_date, lang):

        if not text:
            return None

        try:
            data = {"text": text.strip(), "identifier": identifier, "spacy_model": self.get_model(lang)}
            response = requests.post(url=self.url, json=data)
            print("SpacyClient response ", response.status_code, response.reason)
            return response.json()
        except JSONDecodeError as err:
            print("SpacyClient JSONDecodeError", err, response)
            return None

    def get_model(self, language):
        return self.models[language]
