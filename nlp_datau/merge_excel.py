import math

import pandas as pd


def merge_subject(subject, col_subject, col_timestamp, pre, post):

    subject_rows_pre = pre.loc[pre[col_subject] == subject]
    subject_rows_pre = subject_rows_pre.sort_values(col_timestamp)
    subject_rows_pre["timestamp_next"] = subject_rows_pre["timestamp"].shift(-1)
    subject_rows_post = post.loc[post[col_subject] == subject]

    for index, row in subject_rows_pre.iterrows():
        start_current = row['timestamp']
        start_next = row['timestamp_next']

        if math.isnan(start_next):
            result = subject_rows_post[subject_rows_post[col_timestamp] > start_current]
        else:
            start_next = int(start_next)
            result = subject_rows_post[subject_rows_post[col_timestamp] > start_current]
            result = result[result[col_timestamp] < start_next]

        if len(result.index) > 0:
            pre.loc[pre['instance_key'] == row['instance_key'], ['POST_instance_key']] = result.iloc[0]['instance_key']
        else:
            print('warn no hit', str(subject), start_current)

    return pre

def merge_pre_post(path_pre, path_post, col_subject, col_timestamp):
    pre = pd.read_csv(path_pre)
    post = pd.read_csv(path_post)

    pre["POST_instance_key"] = None

    subjects = pre[col_subject].unique()
    subjects_len = str(len(subjects))

    print('unique subjects', subjects_len)

    for index, subject in enumerate(subjects):
        print('Subject ' + str(subject) + ' (' + str(index) + '/' + subjects_len + ')')
        pre = merge_subject(subject, col_subject, col_timestamp, pre, post)

    return pre