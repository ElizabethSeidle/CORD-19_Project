import pymongo
client = pymongo.MongoClient("mongodb+srv://scott:bluegreen50@squid.36jsw.mongodb.net/CORD19?retryWrites=true&w=majority")
db = client.CORD19
collection = db.scratch

import numpy as np
import pandas as pd
import umap.umap_ as umap
import pprint

cursor = db.preprocess.find({}, {"bert_abstract":1})
#cursor.count()

#pprint.pprint(list(cursor))

json = pd.json_normalize(list(cursor))

df =  pd.DataFrame(json)

df.head(5)

# expand df.bert_abstract into its own dataframe
values = df['bert_abstract'].apply(pd.Series)
# rename each variable is tags
values = values.rename(columns = lambda x : 'value_' + str(x))
# view the tags dataframe
values
# join the tags dataframe back to the original dataframe
df = pd.concat([df["_id"], values[:]], axis=1)
df.head(5)

dfNumpy = df.to_numpy()
type(dfNumpy)
umap_embeddings = umap.UMAP(n_neighbors=200, n_components=5, metric='cosine', low_memory=True).fit_transform(dfNumpy[:,1:769])
#print(umap_embeddings)
umap_df = pd.DataFrame(umap_embeddings)
df_umap = pd.concat([df["_id"], umap_df[:]], axis=1)
print(df_umap.head(5))

df_umap.columns = df_umap.columns.astype(str)
data = df_umap.to_dict(orient='records')
#print(data)
#db.umap.insert_many(data)
