import pandas as pd
import os
import csv
import emoji
import re

from .db_connection import retrieved_db

def separate_messages_in_days(df_messages, group_id) -> None:
    '''Separa as mensagens em dias e salva em arquivos csv separados no timestamp 2023/01/02 e 2023/01/18'''
    try:
        df_messages['message_utc'] = pd.to_datetime(df_messages['message_utc'])
        df_messages['date'] = df_messages['message_utc'].dt.date # Separar a data da hora
        df_messages['time'] = df_messages['message_utc'].dt.time # Separar a hora da data

        # Salvar as mensagens em arquivos csv separados por dia
        for date in df_messages['date'].unique():
            csv_path = f'data/msgPerGroup/ID_{group_id}/messages_{date}.csv'

            if not os.path.exists(csv_path):
                df_messages_date = df_messages[df_messages['date'] == date]
                df_messages_date.to_csv(csv_path, header = 'True', index = False, quoting = csv.QUOTE_ALL)
                print(f"Mensagens do dia {date} salvas com sucesso em {csv_path}")
    
    except Exception as e:
        print("Tipo do erro: ", type(e))
        print("Error: ", e)

def get_separated_messages(groups) -> None:
    '''Seleciona as mensagens de cada grupo e as separa em arquivos csv por dias'''
    df_groups = groups
    
    for index, row in df_groups.iterrows():
        group_id = row['channel_id']

        # Criar diretórios para cada grupo
        group_dir = f'data/msgPerGroup/ID_{group_id}'
        os.makedirs(group_dir, exist_ok = True)

        df_retrieval = retrieved_db(group_id)
      
        # Separar as mensagens em dias e salvar em arquivos csv separados
        separate_messages_in_days(df_retrieval, group_id)

def clear_messages(file_name) -> str:
    """Leitura do arquivo csv e limpeza das mensagens. Retorna as mensagens limpas."""
    try:
        df = pd.read_csv(file_name)
        messages = df['message']
        messages = messages.dropna()
        messages = messages.drop_duplicates()
        messages = messages.tolist()
        messages = ' '.join(str(message) for message in messages) # Cada elemento da lista será separado por um espaço em branco quando concatenado

        messages = emoji.replace_emoji(messages, "") # Remover emojis
        
        messages = re.sub(r"https?\S+", "", messages) # Remover links (https e http)
        messages = re.sub("@\w+", "", messages) # Remover menções de usuários
        messages = re.sub(r' +', r' ', messages) # Remover espaços repetidos
        messages = re.sub(r"([\r\n]+)+", r' ', messages) # Remover quebras de linha repetidas

        messages = re.sub(r'(.)\1{2,}', r'\1', messages)  # Remover caracteres repetidos consecutivos
        messages = re.sub(r'\b(\w+)( \1\b)+', r'\1', messages)  # Remover palavras repetidas consecutivas
        #messages = re.sub(r'\b(\w+\s+\w+)( \1\b)+', r'\1', messages) # Remover frases repetidas mais de uma vez

    except Exception as e:
        print("Error: ", e)
    
    return messages