import unittest

from nlp_datau.merge_excel import merge_pre_post

path_pre = "C:\\Users\\sander.puts\\Downloads\\report.3559000.14321.csv"
path_post = "C:\\Users\\sander.puts\\Downloads\\report.3694000.14321-3.csv"

col_subject_id = 'subject_id'
col_timestamp = 'timestamp'


class TestIndexMethods(unittest.TestCase):

    result = merge_pre_post(path_pre, path_post, col_subject_id, col_timestamp)
    result.to_excel('merged.xlsx')
