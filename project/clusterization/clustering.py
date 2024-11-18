from sklearn.cluster import KMeans
from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np


def get_silhouette_score_kmeans(high_dim_embeddigs, max_clusters):
    silhouette_scores = []
    k_values = []
    wcss = []  # Within-Cluster Sum of Squares. Soma dos quadrados das distâncias entre cada ponto no cluster e o centróide do cluster. Portanto, menores valores significam que os pontos estão mais próximos ao centróide do cluster.

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


def get_silhouette_score_hdbscan(high_dim_embeddigs, min_cluster_size):
    """Calcula o coeficiente de silhueta para cada parâmetro de 'min_cluster_size' do algoritmo HDBSCAN.
    'min_cluster_size' é o número mínimo de amostras em um grupo para esse grupo ser considerado um cluster."""
    silhouette_scores = []
    min_cluster_size_values = []

    for i in range(2, min_cluster_size + 1):
        clusterer = HDBSCAN(i)
        labels = clusterer.fit_predict(high_dim_embeddigs)
        min_cluster_size_values.append(i)

        if len(set(labels)) > 1:
            valid_labels = labels[labels != -1]
            valid_embeddings = high_dim_embeddigs[labels != -1]
            scores = silhouette_score(valid_embeddings, valid_labels)
            silhouette_scores.append(scores)

        else:
            silhouette_scores.append(-1)  # Se houver apenas um cluster ou outliers

    data = {
        "min_cluster_size": min_cluster_size_values,
        "silhouette_score": silhouette_scores,
    }

    df = pd.DataFrame(data)
    best_hdbscan_cluster = min_cluster_size_values[np.argmax(silhouette_scores)]

    return df, best_hdbscan_cluster


def k_means_clustering(n_clusters, high_dim_embeddings):
    kmeans = KMeans(n_clusters).fit(high_dim_embeddings)

    return kmeans


def hdbscan_clustering(high_dim_embeddings, min_cluster_size):
    clusterer = HDBSCAN(min_cluster_size)
    cluster_labels = clusterer.fit_predict(high_dim_embeddings)

    return clusterer, cluster_labels


def get_cluster_labels(df, model, max_tokens, APIclient):
    df_copy = df.copy()
    dict_summaries_clusters = df_copy.groupby("cluster")["label"].apply(list).to_dict()

    # Converte o dicionário para uma string formatada
    dict_as_string = "\n".join(
        [
            f"Cluster {cluster}: {labels}"
            for cluster, labels in dict_summaries_clusters.items()
        ]
    )

    try:
        response = APIclient.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em análise de texto e vai classificar grupos de mensagens (clusters) com base em seus temas. Sua tarefa é identificar as características mais distintivas de cada cluster e fornecer uma categorização clara que discrimine ao máximo um cluster do outro.",
                },
                {
                    "role": "user",
                    "content": f"A seguir está um dicionário com <chave>: <valor>, onde a chave é um cluster e o valor é uma lista de sumários de texto associadas a esse cluster.\n\n{dict_as_string}\n\nPara cada cluster, forneça:\n1. Um título ou rótulo curto que resume o cluster.",
                },
            ],
        )

    except Exception as e:
        print("Tipo do erro: ", type(e))
        print("Error: ", e)

    return response.choices[0].message.content


def get_cluster_labels_maritalk(df, cluster, max_tokens, APIclient):
    df_copy = df.copy()
    df_copy["clusters"] = df_copy["clusters"].astype(int)
    df_copy = df_copy[df_copy["clusters"].isin([cluster])]

    text = "\n".join(df_copy["label"].tolist())

    try:
        response = APIclient.generate(
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": "Analise e classifique os sumários abaixo em uma categoria. Forneça apenas o texto da categoria e nenhuma informação a mais.",
                },
                {"role": "user", "content": text},
            ],
        )

    except Exception as e:
        print("Tipo do erro: ", type(e))
        print("Error: ", e)

    answer = response["answer"]
    return answer


