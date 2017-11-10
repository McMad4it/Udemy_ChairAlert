import os
import pymongo


__author__ = 'neil'


# inherit all the object methods as well as having Database class methods.
class Database(object):
    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None

    @staticmethod
    def initialise():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)  # equivalent to (example) db.fullstack.find_one({"_id": "atc346gfdx..."})

    @staticmethod
    def update(collection, query, data):
        return Database.DATABASE[collection].update(query, data, upsert=True)  # upsert means if query does not work then insert in data.

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
