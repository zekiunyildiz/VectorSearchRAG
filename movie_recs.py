import pymongo
from dotenv import load_dotenv
import os

load_dotenv()  # .env dosyasını yükler

mongodb_uri = os.getenv("MONGODB_URI")  # .env dosyasından MONGODB_URI değişkenini alır


client = pymongo.MongoClient(mongodb_uri)
print(client)
db = client.sample_mflix
print("db:",db)
collection = db.movies

items = collection.find().limit(5)

for item in items:
    print("item:",item)