# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:39:46 2020

@author: crdor
"""
import pymongo
import pandas as pd
import re 
import nltk


client = pymongo.MongoClient("mongodb+srv://group3:group3psu!@squid.36jsw.mongodb.net/CORD19?retryWrites=true&w=majority")
db = client.CORD19
#db.list_collection_names()
collection = db.preprocess
y = collection.find({}, {'abstract_tfidf':1})
df = pd.DataFrame(y)
df.info()

def convert_list_to_string(list, seperator=' '):
    return seperator.join(list)
########################

##### Create List of abstracts
w = []
for i in range(0,len(df.index)):
    abstract = df['abstract_tfidf'].iloc[i]
    w.append(abstract)
    

listToStr = ''.join([str(elem) for elem in w])
tokens = nltk.word_tokenize(listToStr)

#removing these prompted tagging error: string index out of range 
#b = ['background', 'group']
#tokens = [(lambda x: re.sub(r'|'.join(b),'', x))(x) for x in tokens]


##### Tagging pos 
tagged = nltk.pos_tag(tokens) #takes time to complete
tag_fd = nltk.FreqDist(tag for (word,tag) in tagged)
tag_fd.most_common() #for reference: over 4million Nouns


#Verbs & Adjectives Tagged
tagged_VADJ = [x for (x,y) in tagged if y in ('VBP', 'VB', 'VBD', 'VBZ', 'VBN', 'VBG', 
                                         'JJ', 'JJR', 'JJS')] 


remove_words = list(set(tagged_VADJ)) #unique list of verbs & adj

#loop through abstracts and remove words
w_final = []
for ct in range(0,len(df.index)):
    tl = list(w[ct].split())
    z = [x for x in tl if x not in remove_words]
    z = convert_list_to_string(z)
    w_final.append(z)
    tl = []
    z = []


# Create dataframe to push to Mongo
df2 = pd.DataFrame(w_final, columns=['abstract_final'])
df2['_id'] = df2.index
df2 = df2[['_id','abstract_final']]
df2.head()


############### push out to MongoDB


# db = client.CORD19
# db.list_collection_names()
# collection = db.preprocess 

# ##### 

# cursor = collection.find()
 
# for document in cursor:
#     id = document["_id"]
#     record = df2.loc[(df2['_id'] == id)]
#     abstract_final = record["abstract_final"]
#     abstract_final = document.get("abstract_final")
 
#     if abstract_final is None:
#         collection.update_one({"_id": id}, {"$set": {"abstract_final": abstract_final}})