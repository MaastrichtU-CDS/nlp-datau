import unittest
import pandas as pd

from nlp_datau.link_subject_pre_post_responses import link_pre_post_responses

path_pre = "C:\\Users\\sander.puts\\Downloads\\report.3559000.14321.csv"
path_post = "C:\\Users\\sander.puts\\Downloads\\report.3694000.14321-3.csv"

col_subject_id = 'subject_id'
col_timestamp = 'timestamp'


class TestIndexMethods(unittest.TestCase):

    result, merged = link_pre_post_responses(path_pre, path_post, col_subject_id, col_timestamp)
    result.to_excel('pre_merged.xlsx')
    merged.to_excel('pre_merged_post.xlsx')

