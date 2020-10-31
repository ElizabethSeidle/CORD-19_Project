# Prepare data
import umap.umap_ as umap
umap_2d_data = umap.UMAP(n_neighbors=50, n_components=10, min_dist=0.0, metric='cosine', low_memory=True).fit_transform(dfNumpy[:,1:769])
result = pd.DataFrame(umap_2d_data, columns=['x', 'y'])

import hdbscan
cluster = hdbscan.HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom').fit(umap_2d_data)

result['labels'] = cluster.labels_

# Visualize clusters
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(20, 10))
outliers = result.loc[result.labels == -1, :]
clustered = result.loc[result.labels != -1, :]
plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=0.05)
plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=0.05, cmap='hsv_r')
plt.colorbar()

df_cluster = pd.concat([df["_id"], result["labels"]], axis=1)

for index, row in df_cluster.iterrows():
    _id = row['_id']
    label = row['labels']
    db.preprocess.update_one({"_id":_id}, {"$set": {"cluster": label}})

#data = df_cluster.to_dict(orient='records')
#db.clusterFiftyTen.insert_many(data)
