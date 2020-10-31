import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

client = pymongo.MongoClient("mongodb+srv://group3:group3psu!@squid.36jsw.mongodb.net/CORD19?retryWrites=true&w=majority")
db = client.CORD19
db.list_collection_names()
a_coll_1017 = db.preprocess
a_1017 = pd.DataFrame(list(a_coll_1017.aggregate([
    {
        '$lookup': {
            'from': 'clusterFiftyTen', 
            'localField': '_id', 
            'foreignField': '_id', 
            'as': 'cluster'
        }
    }, {
        '$unwind': {
            'path': '$cluster'
        }
    }, {
        '$match': {
            'cluster.labels': 124
        }
    }
])))

####### abstract_string_conversion #####
def convert_list_to_string(list, seperator=' '):
    return seperator.join(list)
a_1017 ['ab_string'] = a_1017 ['cleanAbtstract'].apply(lambda row: convert_list_to_string(row))

#List of Abstracts
w2 = []
for i in range(0,len(a_1017 .index)):
    abstract = a_1017['ab_string'].iloc[i]
    w2.append(abstract)
    
##### tf-idf calc from sklearn max_df=.50, min_df=.25 ###

vectorizer = TfidfVectorizer(max_df=.01, min_df=.0001, stop_words=None, use_idf=True, norm=None)
vectors = vectorizer.fit_transform(w2)
feature_names = vectorizer.get_feature_names()
sums = vectors.sum(axis=0) #sum tf-idf for each term throughout

#connects term and sum freq
data = []
for col, term in enumerate(feature_names):
    data.append((term,sums[0,col]))

##### Output: tf-idf sorted descending top 50

ranking = pd.DataFrame(data, columns=['term','rank']) 
print(ranking.sort_values('rank', ascending=False).head(10))




# ############################
# def extract_topic_sizes(df):
#     topic_sizes = (df.groupby(['labels'])
#                      .count()
#                      .reset_index()
#                      .sort_values("x", ascending=False))
#     return topic_sizes

# topic_sizes = extract_topic_sizes(result); topic_sizes.head(10)