from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import os

from summarization.summarization import clear_messages, truncate_text_tokens_decode, num_tokens_from_string

def tsne_reduce_dim(embeddings, summaries):
    perplexity = min(5, len(summaries) - 1)  # Definindo perplexidade como 3 ou n_samples-1, o que for menor
    tsne = TSNE(n_components = 2, perplexity = perplexity)
    low_dim_embeddings = tsne.fit_transform(embeddings)

    print(f"Dimensão do embedding original: {embeddings.shape[1]}")
    print(f"Dimensão do embedding depois de aplicar o t-SNE: {np.array(low_dim_embeddings).ndim}")

    return low_dim_embeddings

def get_labels(summaries):
    labels = []

    for group in summaries:
      for text in group["Sumário"]:
          labels.append({
            "ID": group["ID"],
            "Sumário": text
            })

    return labels

def get_date_labels(groups, text_encoding, max_tokens, min_number_of_messages):
    date_labels = []

    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_dir = f'data/msgPerGroup/ID_{group_id}' # Diretório que está organizado os arquivos de mensagens separados por grupos
        csv_files = os.listdir(group_dir)
        csv_files.sort()

        group_dates = []
        for file in csv_files:
            file_path = f'{group_dir}/{file}'
            df = pd.read_csv(file_path)
            num_messages = len(df)

            if num_messages > min_number_of_messages: # Temos que fazer essa verificação, para não adicionarmos as datas de arquivos que não possuem sumários
                group_dates.append(file)
    
        date_labels.append(group_dates)

    date_list = []
    for date in date_labels:
        for file in date:
                date_list.append(file.split('_')[-1].split('.')[0]) # Extrair somente a data do nome do arquivo

    return date_list
