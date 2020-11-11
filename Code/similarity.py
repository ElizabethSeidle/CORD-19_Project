import pymongo
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from tqdm import tqdm 

client = pymongo.MongoClient("mongodb+srv://group3:group3psu!@squid.36jsw.mongodb.net/CORD19?retryWrites=true&w=majority")
db = client.CORD19

#####

query = input("What would you like to know?: ")

#####
print("I'm loading my English brain...")
model = SentenceTransformer('distilbert-base-nli-mean-tokens')
query_encoded = model.encode(query, show_progress_bar=False)

#####
print("Getting document cursor...")
cursor = db.preprocess.find({}, {"_id":1, "bert_abstract":1})

df = pd.DataFrame(columns = ['_id', 'diff'])

articles = []

print("Counting total number of documents...")
total_docs = 57921
for document in tqdm(cursor, desc ="I'm reading, wait a bit please", total=total_docs):
    _id = document["_id"]
    bert_abstract = document["bert_abstract"]
    diff = cosine(query_encoded, bert_abstract)
    if (len(articles) < 6):
        articles.append({"_id":_id, "diff":diff})
        articles = sorted(articles, key = lambda i: i['diff'])
    elif (diff < max([x['diff'] for x in articles])):
        articles.pop()
        articles.append({"_id":_id, "diff":diff})
        articles = sorted(articles, key = lambda i: i['diff'])

print("Here are the top five articles I think best address your query...")
for article in articles:
    article = db.preprocess.find_one({"_id":article["_id"]})
    print("Title:", article["title"])
    print()
    print("Abstract:", article["abstract"])
    print()
