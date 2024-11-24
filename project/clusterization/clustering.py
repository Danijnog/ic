import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.metrics import silhouette_score


def get_silhouette_score_kmeans(high_dim_embeddigs, max_clusters) -> tuple[pd.DataFrame, int]:
    """
    Calculates the silhouette scores and Within-Cluster Sum of Squares (WCSS) for K-Means clustering
    across a range of cluster numbers. Identifies the best number of clusters based on the highest 
    silhouette score.
    """
    silhouette_scores = []
    k_values = []

    # Within-Cluster Sum of Squares. 
    # Low values means that the points of certain cluster is closer to the centroid of this cluster.
    wcss = []

    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=i).fit(high_dim_embeddigs)
        k_values.append(i)
        silhouette_scores.append(silhouette_score(high_dim_embeddigs, kmeans.labels_))
        wcss.append(kmeans.inertia_)

    data = {
        "num_clusters": k_values,
        "silhouette_score": silhouette_scores,
        "within_cluster_sum_of_squares": wcss,
    }

    df = pd.DataFrame(data)
    best_k = k_values[np.argmax(silhouette_scores)]

    return df, best_k


def k_means_clustering(n_clusters, high_dim_embeddings) -> KMeans:
    """
    Applies K-Means Clustering to high_dim_embeddings.
    """
    kmeans = KMeans(n_clusters).fit(high_dim_embeddings)

    return kmeans


def hdbscan_clustering(high_dim_embeddings, min_cluster_size) -> tuple[HDBSCAN, np.ndarray]:
    """
    Applies HDBSCAN Clustering to high_dim_embeddings.
    """
    clusterer = HDBSCAN(min_cluster_size)
    cluster_labels = clusterer.fit_predict(high_dim_embeddings)

    return clusterer, cluster_labels


def get_cluster_labels(df, model, max_tokens, api_client, batch_size=1) -> str:
    """
    Uses an API client to classify and label text clusters based on their themes.
    Sends cluster summaries to the API for categorization.
    """

    df_copy = df.copy()
    dict_summaries_clusters = df_copy.groupby("cluster")["label"].apply(list).to_dict()

    clusters = list(dict_summaries_clusters.items())
    batched_responses = []

    #Iterate through a sequence of numbers and skip batch_size for each iteration
    for i in (0, len(clusters), batch_size):
        batch = clusters[i : i + batch_size]
        print("Batch content: ", batch)

        # Converte o dicionário para uma string formatada
        dict_as_string = "\n".join([f"Cluster {cluster}: {labels}" for cluster, labels in batch])

        try:
            response = api_client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "system",
                        "content": 
                        (
                            "Você é um especialista em análise de texto e vai classificar "
                            "grupos de mensagens (clusters) com base em seus temas. Sua tarefa "
                            "é identificar as características mais distintivas de cada cluster "
                            "e fornecer uma categorização clara que discrimine ao máximo um "
                            "cluster do outro."
                        ),
                    },
                    {
                        "role": "user",
                        "content": 
                        (
                            f"A seguir está um dicionário com <chave>: <valor>, onde a chave é "
                            f"um cluster e o valor é uma lista de sumários de texto associadas "
                            f"a esse cluster.\n\n{dict_as_string}\n\n"
                            "Me forneça um rótulo que caracterize cada cluster, foque nos "
                            "diferentes assuntos que distinguem os clusters."
                        ),
                    },
                ],
            )
            batched_responses.append(response.choices[0].message.content)

        except Exception as e:
            print("Error type: ", type(e))
            print("Error: ", e)

    return " ".join(batched_responses)
