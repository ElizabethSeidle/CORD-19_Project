#adding new field to 'preprocess' collection -- NOTE: took me ~1hr to run


#pd_df = your pandas dataframe
#pd_df_variable = your column/variable from pandas dataframe that you want to copy into the collection
#newField = new field being created in MongoDB collection


client = pymongo.MongoClient("mongodb+srv://group3:group3psu!@squid.36jsw.mongodb.net/CORD19?retryWrites=true&w=majority")
db = client.CORD19
collection = db.preprocess

#Your other code.....

cursor = collection.find()
 
for document in cursor:
    id = document["_id"]
    record = pd_df.loc[(pd_df['_id'] == id)]
    pd_df_variable = record["pd_df_variable"]
    newField = document.get("newField")
 
    if newField is None:
        collection_clean.update_one({"_id": id}, {"$set": {"newField": pd_df_variable.tolist()}})
