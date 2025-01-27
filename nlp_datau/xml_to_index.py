from elasticsearch import Elasticsearch
import xmltodict
import json
import base64
import logging

from pathlib import Path
from nlp_datau.data_utils import DataUtils

logging.basicConfig()
logger = logging.getLogger('python-processor')
logger.setLevel(level=logging.INFO)


def clean_value(whitelist_value, field_value):
    if 'start-line' in whitelist_value:
        start_line = whitelist_value['start-line']
        start_index = field_value.find(start_line)
        if start_index:
            next_line_index = field_value.find('\n', start_index)
            if next_line_index:
                field_value = field_value[next_line_index:len(field_value) - 1]
    if 'end-line' in whitelist_value:
        end_line = whitelist_value['end-line']
        end_index = field_value.find(end_line)
        if end_index:
            field_value = field_value[0:end_index]
    return field_value


def get_list_item(list_value, key, match_key, match_value):
    for item in list_value:
        if match_key in item and item[match_key] == match_value:
            if key in item:
                return item[key]
    return None


def get_whitelist_value(key, whitelist_value, source_doc):
    field = whitelist_value['field']
    type = whitelist_value['type']

    logger.debug("whitelist key=%s field=%s  type=%s", key, field, type)
    field_value = DataUtils.get_json_field_dot_notation(field, source_doc)

    if type == "base64":
        field_value = base64.standard_b64decode(field_value)
    if type == "xml":
        if not whitelist_value['xml-field']:
            logger.debug('set xml-field for field=%s', field)
        json_value = json.loads(json.dumps(xmltodict.parse(field_value)))
        field_value = DataUtils.get_json_field_dot_notation(whitelist_value['xml-field'], json_value)
    if type == "list":
        if not whitelist_value['match-key']:
            logger.debug('set match-key for field=%s', field)
        field_value = get_list_item(field_value, whitelist_value['key'], whitelist_value['match-key'], whitelist_value['match-value'])

    return clean_value(whitelist_value, field_value)


def get_doc_whitelisted(doc, id, whitelist_dict):
    whitelist_doc = {
        "id": id
    }
    for key in whitelist_dict:
        logger.debug("Parse whitelist item=%s", key)
        value = get_whitelist_value(key, whitelist_dict[key], doc)
        whitelist_doc[key] = value

    return whitelist_doc


class XmlToIndex(object):

    def __init__(self, es_host="localhost"):
        self.es = Elasticsearch(host=es_host)


    def iterate_xml_dir(self, directory_in_str, extension, es_index, field_id, whitelist_dict=None, encoding="utf8"):
        logger.info('start iteration %s', directory_in_str)
        pathlist = Path(directory_in_str).glob('**/*' + extension)
        count = 0
        for path in pathlist:
            count = count + 1
            path_in_str = str(path)
            with open(path_in_str, encoding=encoding) as in_file:
                logger.debug('read %s', str(path_in_str))
                try:
                    xml = in_file.read()
                    doc = json.loads(json.dumps(xmltodict.parse(xml)))
                    self.index(doc, es_index, field_id, whitelist_dict)
                except Exception as e:
                    logger.error("Error indexing %s", in_file)

            if count % 100 == 0:
                logger.info('count %s', count)
        if count == 0:
            logger.warning("no files found in %s", directory_in_str)
        logger.info('iteration finished %s', directory_in_str)

    def index(self, doc, es_index, field_id, whitelist_dict=None):
        logger.debug('doc=%s', doc)

        id = DataUtils.get_json_field_dot_notation(field_id, doc)
        logger.debug('id=%s', id)

        if whitelist_dict:
            doc = get_doc_whitelisted(doc, id, whitelist_dict)

        res = self.es.index(index=es_index, id=id, body=doc)
        logger.debug("result %s", res['result'])

