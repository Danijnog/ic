import plotly.express as px
import pandas as pd

from typing import Tuple

def get_df_for_plot(low_dim_embeddings, labels, date_labels, clusters_labels) -> pd.DataFrame:
    """Cria um DataFrame com os embeddings e labels para ser usado no Scatter Plot."""
    assert low_dim_embeddings.shape[0] >= len(labels), "More labels than embeddings."

    # Criar um DataFrame com os embeddings, labels, ID e data
    df = pd.DataFrame(low_dim_embeddings, columns = ['x', 'y'])
    df['label'] = [groups["Sumário"] for groups in labels]
    df['ID'] = [groups["ID"] for groups in labels]
    df['date'] = date_labels
    df['clusters'] = clusters_labels

    # Transformar o ID em string para fazer a legenda
    df['clusters'] = df['clusters'].astype(str)
    df['ID'] = df['ID'].astype(str)

    return df

def remove_cluster(df, cluster_list):
    df_copy = df.copy()

    df_copy['clusters'] = df_copy['clusters'].astype(int)
    new_cluster_df = df_copy[~df_copy['clusters'].isin(cluster_list)]
    
    return new_cluster_df 

def remove_groups(df, group_list):
    df_copy = df.copy()

    df_copy['ID'] = df_copy['ID'].astype(int)
    new_group_df = df_copy[~df_copy['ID'].isin(group_list)]

    return new_group_df

def get_df_for_recluster(df, cluster_list, group_list, days) -> pd.DataFrame:
    new_df = df.copy()
    new_df = remove_cluster(new_df, cluster_list)
    new_df = remove_groups(new_df, group_list)
    new_df = filter_df(new_df, days)

    new_df['clusters'] = new_df['clusters'].astype(str)

    return new_df

def get_new_high_dim_embedding(high_dim_embeddings, labels, date_labels, clusters_labels, cluster_list, group_list, days) -> pd.DataFrame:
    """Retorna um novo embedding de alta dimensão após a remoção de outliers."""
    assert high_dim_embeddings.shape[0] >= len(labels), "More labels than embeddings."

    # Criar um DataFrame com os embeddings, labels, ID e clusters
    df = pd.DataFrame(high_dim_embeddings, columns = [f"dim{i}" for i in range(high_dim_embeddings.shape[1])])
    df['label'] = [groups["Sumário"] for groups in labels]
    df['ID'] = [groups["ID"] for groups in labels]
    df['date'] = date_labels
    df['clusters'] = clusters_labels

    # Transformar o ID e clusters em string
    df['clusters'] = df['clusters'].astype(str)
    df['ID'] = df['ID'].astype(str)

    df_for_recluster = remove_cluster(df, cluster_list)
    df_for_recluster = remove_groups(df_for_recluster, group_list)
    df_for_recluster = filter_df(df_for_recluster, days)

    new_high_dim_embeddings_umap = df_for_recluster.iloc[:, 0:high_dim_embeddings.shape[1]]

    return new_high_dim_embeddings_umap

def filter_df(df, days):
   """Filtrar o DataFrame para conter apenas os dias que queremos analisar.
   Dias 4, 6, 8, 10, 12."""
   filtered_df = df.copy()
   filtered_df['date'] = pd.to_datetime(filtered_df['date'])
   filtered_df = filtered_df[filtered_df['date'].dt.day.isin(days)] # Contém apenas os dias que queremos analisar.
   filtered_df['date'] = filtered_df['date'].dt.strftime('%Y-%m-%d') # Converte a data de volta pra string para remover o tempo que estava incluso na data.

   return filtered_df

def embedding_scatter_plot(df) -> Tuple[px.scatter, pd.DataFrame]:
  """Cria um Scatter Plot com os embeddings de baixa dimensão."""
  fig = px.scatter(df, x = 'x', y = 'y', 
                   hover_name = df['label']
                   .apply(lambda x: '<br>'
                   .join(x[i:i + 50] for i in range(0, len(x), 50))),
                   hover_data = {'date', 'ID'}, color = 'clusters', title = 'Embedding Summary',
                   width = 800, height = 600)

  return fig, df