import uuid
from src.common.database import Database
import src.models.items.constants as ItemsConstants
from src.models.stores.store import Store

__author__ = 'neil'

import requests
import re
from bs4 import BeautifulSoup


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)  #links to store
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return " <Item {} with URL {}".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        # creates a regular expression object which can be used with search() and match() methods.
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)  # look for string and return match object.
        self.price = float(match.group())
        return self.price  # return the value e.g $115.00 = 115.00

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(ItemsConstants.COLLECTION, query={"_id": _id}))

    def save_to_mongo(self):
        Database.update(ItemsConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def from_mongo(cls, name):
        data = Database.find_one(ItemsConstants.COLLECTION, query={"name": name})
        if data is not None:
            return cls(**data)
