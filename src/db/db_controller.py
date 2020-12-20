import pymongo as pm
from src.db.db_constants import host_name, port_number, default_db

USERS_COLLECTION = 'users'
PRODUCTS_COLLECTION = 'products'


class MongoClient(object):
    __instance = None

    def __new__(cls):
        """
        Description:
        Parameters:
        ----------

        Return:
        ----------

        """
        if MongoClient.__instance is None:
            MongoClient.__instance = object.__new__(cls)
            MongoClient.__instance.mongo = None
            MongoClient.__instance.db = None
            MongoClient.__instance.connect()
        return MongoClient.__instance

    def connect(self):
        """
        Description:
        Parameters:
        ----------

        Return:
        ----------

        """
        try:
            self.mongo = pm.MongoClient(host=host_name, port=port_number)
            self.db = self.mongo[default_db]
        except Exception as e:
            raise Exception('Failed to connect to Mongo: {}'.format(str(e)))

    def insert_new_document(self, collection, data):
        id_value = None
        if collection and data:
            id_value = self.db[collection].insert(data)
        return id_value

    def find_document(self, collection, query):
        data = self.db[collection].find_one(query)
        return data

    def find_elements(self, collection, query=None):
        data = self.db[collection].find(query)
        return data
