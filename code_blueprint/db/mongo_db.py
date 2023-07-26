from pymongo import MongoClient
from pymongo.database import Database


class MongoDb:

    def __init__(self):
        client = MongoClient( 'mongodb://127.0.0.1:27017', serverSelectionTimeoutMS=300 )
        client.server_info()  # verify connection
        self.db: Database = client['tourism']