from sklearn.cluster import KMeans
from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np

def get_silhouette_score_kmeans(high_dim_embeddigs, max_clusters):
    silhouette_scores = []
    k_values = []

    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters = i).fit(high_dim_embeddigs)
        k_values.append(i)
        silhouette_scores.append(silhouette_score(high_dim_embeddigs, kmeans.labels_))
    
    data = ({
    'num_clusters': k_values,
    'silhouette_score': silhouette_scores
    })
    
    df = pd.DataFrame(data)
    best_k = k_values[np.argmax(silhouette_scores)]

    return df, best_k

def get_silhouette_score_hdbscan(high_dim_embeddigs, max_clusters):
    silhouette_scores = []
    clusters_values = []

    for i in range(2, max_clusters + 1):
        clusterer = HDBSCAN(i)
        labels = clusterer.fit_predict(high_dim_embeddigs)
        clusters_values.append(i)

        if len(set(labels)) > 1:
            valid_labels = labels[labels != -1]
            valid_embeddings = high_dim_embeddigs[labels != -1]
            scores = silhouette_score(valid_embeddings, valid_labels)
            silhouette_scores.append(scores)
        
        else:
            silhouette_scores.append(-1) # Se houver apenas um cluster ou outliers

    data = ({
    'num_clusters': clusters_values,
    'silhouette_score': silhouette_scores
    })
    
    df = pd.DataFrame(data)
    best_hdbscan_cluster = clusters_values[np.argmax(silhouette_scores)]

    return df, best_hdbscan_cluster

def k_means_clustering(n_clusters, high_dim_embeddings):
    kmeans = KMeans(n_clusters).fit(high_dim_embeddings)

    return kmeans

def hdbscan_clustering(high_dim_embeddings, min_cluster_size):
    clusterer = HDBSCAN(min_cluster_size)
    cluster_labels = clusterer.fit_predict(high_dim_embeddings)

    return clusterer, cluster_labels