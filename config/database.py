from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://mansi:mansi123@cluster0.qhxmewv.mongodb.net/?ssl=true"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.get_database("info")
collection_name = db.get_collection("students")