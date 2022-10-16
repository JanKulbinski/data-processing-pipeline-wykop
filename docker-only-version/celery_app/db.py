import os

from typing import Collection
from pymongo import MongoClient

mongo_pass = os.getenv("MONGO_PASS")

client = MongoClient(f"mongodb://root:{mongo_pass}@mongo:27017/")
db = client["wykopDB"]
posts_collection = db["posts"]


def insert_post(post):
    posts_collection.update_one(post, {"$set": post}, upsert=True)
