import pymongo
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # .env dosyasını yükler

mongodb_uri = os.getenv("MONGODB_URI")  # .env dosyasından MONGODB_URI değişkenini alır
hf_token = os.getenv("HF_TOKEN")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


client = pymongo.MongoClient(mongodb_uri)
print(client)
db = client.sample_mflix
print("db:",db)
collection = db.movies

def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text})
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    return response.json()

for doc in collection.find({'plot':{"$exists": True}}).limit(50):
    doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
    collection.replace_one({'_id': doc['_id']}, doc)