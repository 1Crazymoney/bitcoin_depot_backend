'''Saves info to database'''
from flask_pymongo import pymongo
from Const import Const

CONNCECTION_STRING = Const.DB_CONNECTION_STRING


client = pymongo.MongoClient(CONNCECTION_STRING)
db = client.get_database('bitcoin_depot')
atms_collection = pymongo.collection.Collection(db, 'atm_locations')
states_collection = pymongo.collection.Collection(db, 'states')


