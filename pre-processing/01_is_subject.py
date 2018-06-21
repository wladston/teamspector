from pymongo import MongoClient

import math

db = MongoClient().imdbws

i = 0
for m in db.titles.find({'is_subject': {'$exists': False}}):
        i += 1
        is_subject = True
        if not m['startYear'] or not (1912 <= m['startYear'] <= 2012):
            is_subject = False
        if m['titleType'] != 'movie':
            is_subject = False
        if m['isAdult']:
            is_subject = False

        db.titles.update_one({'_id': m['_id']},
            {'$set': {'is_subject':  is_subject}})

        if i % 1000 == 0:
            print("{} titles updated.".format(i))
