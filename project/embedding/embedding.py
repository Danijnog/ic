import torch
import pickle
import pandas as pd
import os
import numpy as np

def embedding(text, tokenizer, model):
    inputs_ids = tokenizer.encode(str(text), return_tensors = 'pt', truncation = True, max_length = 512)   # 512 é o limite máximo de max_length para garantir que o texto extraído não ultrapasse a quantidade de tokens que o modelo é capaz de lidar
    
    with torch.no_grad():
        outputs = model(inputs_ids)
        embedding = outputs.last_hidden_state[0, 1:-1]
    
    return embedding.mean(dim = 0)

def get_embeddings(summaries, tokenizer, model):
    ''' Retorna o embedding de todos os sumários da lista de dicionários summaries'''
    all_embeddings = []

    for group in summaries:
        group_id = group["ID"]
        group_summaries = group["Sumário"]

        if group_summaries: # Verificar se a lista de sumarios do grupo não está vazia
            embeddings = torch.stack([embedding(text, tokenizer, model) for text in group_summaries])
            all_embeddings.append(embeddings)
        
        else:
            print(f"O grupo {group_id} não possui sumários. " \
                  f"Isso se deve ao fato do grupo não possuir mensagens no período analisado de fato, ou " \
                  f"as mensagens terem sido limpas e não haver informação útil para sumarizar.")
    
    all_embeddings = torch.cat(all_embeddings, dim = 0)
    return all_embeddings

def gpt_embedding(text, model, client):
    response = client.embeddings.create(
        input = text,
        model = model,
    )

    return response.data[0].embedding

def get_gpt_embeddings(summaries, model, client):
    all_embeddings = []

    for group in summaries:
        group_id = group["ID"]
        group_summaries = group["Sumário"]

        if group_summaries:
            embeddings = [gpt_embedding(text, model, client) for text in group_summaries]
            all_embeddings.extend(embeddings)
        
        else:
            print(f"O grupo {group_id} não possui sumários. " \
                  f"Isso se deve ao fato do grupo não possuir mensagens no período analisado de fato, ou " \
                  f"as mensagens terem sido limpas e não haver informação útil para sumarizar.")
        
    return all_embeddings

def normalize_l2(embeddings):
    embeddings = np.array(embeddings)

    if embeddings.ndim == 1:
        l2_norm = np.linalg.norm(embeddings)
        return np.where(l2_norm == 0, embeddings, embeddings / l2_norm) # Se o valor da norma for 0, retorna o valor do embedding, se não retorna o valor normalizado

    l2_norm = np.linalg.norm(embeddings, ord = 2, axis = 1, keepdims = True) # Para uma matriz (array 2D), a normalização tem de ser feita linha a linha (cada vetor individualmente) (axis = 1)

    return np.where(l2_norm == 0, embeddings, embeddings / l2_norm)

def save_embedding(embeddings, file_name):
    """ Salva o embedding em um arquivo binário através do Pickle, que converte objetos Python em um fluxo de bytes."""
    with open(file_name, 'wb') as f:
        pickle.dump(embeddings, f)
        f.close()

def get_embedding_saved(file_name):
    """ Converte o arquivo binário que já foi salvo em um Tensor. """
    with open(file_name, 'rb') as f:
        embeddings = pickle.load(f)
        f.close()
    
    return embeddings

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

def remove_groups(df, group_list):
    new_group_df = df[~df['ID'].isin(group_list)]

    return new_group_df

