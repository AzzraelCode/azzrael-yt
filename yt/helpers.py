import csv
import datetime
from datetime import *

'''
Parse date RFC 3339
'''
def parse_date(text):
    for fmt in ('%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S%z'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

'''
Array of dicts [{}, {}, {}] saves to csv
'''
def darr_to_csv(arr, path):
    with open(path, 'w+', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, arr[0].keys(),delimiter="\t")
        w.writeheader()
        w.writerows(arr)
