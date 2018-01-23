# -*- coding: utf-8 -*-

# This will get movie information form the Sqlite database generated by
# imdb2sql.py and record the relevant information into a MongoDB collection.

import os
from datetime import datetime

import sqlite3
from dateutil import parser

from imdb import IMDb
from pymongo import MongoClient

root_path = os.path.dirname(os.path.realpath(__file__))
path = root_path + "/../imdb.sqlite"
conn = sqlite3.connect(path)
cur = conn.cursor()

ia = IMDb('sql', uri='sqlite://'+path)

db = MongoClient().imdb

counter = 0
total_counter = 0
cur.execute("SELECT id FROM title WHERE kind_id = 1")

i = 0
while True:
    row = cur.fetchone()
    if not row:
        break

    total_counter += 1
    if total_counter % 100 == 0:
        print total_counter

    if db.movies.find_one({'_id': row[0], 'budget': {'$exists': False}}):
        m = ia.get_movie(row[0])

        budget = m.get('business', {}).get('budget', [''])[0]

        if budget:
            i += 1
            print '    ', budget

        db.movies.update({'_id': m.getID()},
                         {'$set': {'budget':  budget}})

print "%d budgets added." % i
conn.close()
