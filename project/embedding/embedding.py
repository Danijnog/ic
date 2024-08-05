import torch
import pickle

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