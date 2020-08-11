from json import JSONDecodeError
import requests


class PyContextNlpClient(object):

    def __init__(self, url_lang_map):
        self.url_lang_map = url_lang_map

    def annotate(self, jsonnlp, lang='en'):
        if not jsonnlp:
            return None
        try:
            response = requests.post(url=self.get_url(lang), json=jsonnlp)
            print("PyContextNlpClient response ", response.status_code, response.reason)
            return response.json()
        except JSONDecodeError as err:
            print("JSONDecodeError", err, response)
            return None

    def get_url(self, lang):
        return self.url_lang_map[lang]