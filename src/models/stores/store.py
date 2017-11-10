import uuid
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors
from src.common.database import Database

__author__ = 'neil'


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, query={"_id": id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json(),)

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, query={"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        '''
        Return a store from a url like "http://www.johnlewis.com/sdfj43g4g21k.html"
        :param url: The item's URL
        :return: a Store, or raises a StoreNotFoundException if no store matches the URL
        '''

        for i in range(0, len(url)+1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The URL Prefix was not found")

    @classmethod
    def all(cls):
        return [cls(**element) for element in Database.find(StoreConstants.COLLECTION, query={})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})