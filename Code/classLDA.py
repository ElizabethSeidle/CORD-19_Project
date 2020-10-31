import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
import re

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.stem.snowball import SnowballStemmer

import itertools
from langdetect import detect
import seaborn as sns

import gensim
from gensim import corpora
import pyLDAvis.gensim

#!pip install textblob
from textblob import TextBlob

#############################
cluster_iter = [117,30,121,77]
topic_list = []
for cluster in cluster_iter:
    cluster_label = cluster

#############################
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
                'cluster.labels': cluster_label
            }
        }
    ])))
            
    #############################
    
    #Create a Gensim dictionary from the tokenized data 
    cleaned = a_1017['cleanAbtstract']
    
    #Creating term dictionary of corpus, where each unique term is assigned an index.
    dictionary = corpora.Dictionary(cleaned)
    
    #Filter terms which occurs in less than 1 answer and more than X% of the abstracts.
    dictionary.filter_extremes(no_below=1, no_above=0.4)
    
    #convert the dictionary to a bag of words corpus 
    corpus = [dictionary.doc2bow(tokens) for tokens in cleaned]
    
    print(corpus[:1])
    
    [[(dictionary[id], freq) for id, freq in cp] for cp in corpus[:1]]
    
    #############################
    
    #Declare number of topics
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 1, id2word=dictionary, passes=30)
    ldamodel.save('model_combined.gensim')
    
    #Declare number of keywords to use for each topic
    topics = ldamodel.print_topics(num_words=20)
    for topic in topics:
       print(topic)
       
    get_document_topics = ldamodel.get_document_topics(corpus[0])
    print(get_document_topics) #entry 0 is x% related to topic n
    
    #############################
    
    def dominant_topic(ldamodel, corpus, texts):
         #Function to find the dominant topic in each review
         sent_topics_df = pd.DataFrame() 
         # Get main topic in each review
         for i, row in enumerate(ldamodel[corpus]):
             row = sorted(row, key=lambda x: (x[1]), reverse=True)
             # Get the Dominant topic, Perc Contribution and Keywords for each review
             for j, (topic_num, prop_topic) in enumerate(row):
                 if j == 0:  # =&gt; dominant topic
                     wp = ldamodel.show_topic(topic_num,topn=4)
                     topic_keywords = ", ".join([word for word, prop in wp])
                     sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                 else:
                     break
         sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
         contents = pd.Series(texts)
         sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
         return(sent_topics_df)
    
    #############################
    df_dominant_topic = dominant_topic(ldamodel=ldamodel, corpus=corpus, texts=a_1017['abstract']) 
    df_dominant_topic.head()
    topic_list.append(df_dominant_topic["Topic_Keywords"])
