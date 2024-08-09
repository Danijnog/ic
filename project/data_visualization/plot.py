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
    df['ID'] = df['ID'].astype(str)

    return df

def embedding_scatter_plot(df) -> Tuple[px.scatter, pd.DataFrame]:
  """Cria um Scatter Plot com os embeddings de baixa dimensão."""
  fig = px.scatter(df, x = 'x', y = 'y', 
                   hover_name = df['label']
                   .apply(lambda x: '<br>'
                   .join(x[i:i + 50] for i in range(0, len(x), 50))),
                   hover_data = {'date', 'ID'}, color = 'clusters', title = 'Embedding Summary')

  return fig, df