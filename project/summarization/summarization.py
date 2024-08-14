import os
import pandas as pd

from connection.db_processing import clear_messages
from .tokens import num_tokens_from_string, truncate_text_tokens_decode

def generate_summary(input_text, max_tokens, model, APIclient) -> str:
    try:
        response = APIclient.chat.completions.create(
            model = model,
            max_tokens = max_tokens,
            messages = [
                {"role": "system", "content": "Resuma a seguinte conversa do Telegram em até 50 palavras. O sumário deve capturar os pontos-chave e destacar as informações mais relevantes. Forneça apenas o texto do sumário, sem introduções ou conclusões adicionais."},
                {"role": "user", "content": input_text}
            ]
        )
        
    except Exception as e:
        print("Tipo do erro: ", type(e))
        print("Error: ", e)
    
    return response.choices[0].message.content


# Summary from a group of messages
def group_summary(group_id, text_encoding, text_model, max_tokens, min_number_of_messages, APIclient) -> list:
    group_dir = f'data/msgPerGroup/ID_{group_id}'
    csv_files = os.listdir(group_dir)
    csv_files.sort()
    summaries = []
    print(f"Grupo: {group_id}")

    contagem = 0

    for file in csv_files:
        print(file)
        file_path = f'{group_dir}/{file}'
        df = pd.read_csv(file_path)
        num_messages = len(df)

        if num_messages > min_number_of_messages:
            messages = clear_messages(file_path)
            truncated_messages = truncate_text_tokens_decode(messages, text_encoding, max_tokens)
            prompt_tokens = num_tokens_from_string(truncated_messages, text_encoding)

            print("Número de tokens para o prompt: ", prompt_tokens)
            contagem += 1

            try:
                # Append each summary to a list
                generated_summary = generate_summary(truncated_messages, max_tokens, text_model, APIclient)
                summaries.append(generated_summary)
                print(contagem)
            
            except Exception as e:
                print(f"Erro ao gerar sumarização para o arquivo: {file}: {e}")
                print("/n")
        
        else:
            print(f"Arquivo {file_path} não entrou para a sumarização. Quantidade de mensagens do arquivo é menor que {min_number_of_messages}.")

    return summaries

### Sumarização para todos os grupos
def get_summaries_for_groups(groups, text_encoding, text_model, max_tokens, min_number_of_messages, APIclient) -> list:
    summaries = []
    
    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_summaries = group_summary(group_id, text_encoding, text_model, max_tokens, min_number_of_messages, APIclient)

        # Guardar o id do grupo e o sumário do grupo em uma lista de dicionários
        summaries.append({
            "ID": group_id,
            "Sumário": group_summaries
        })

    return summaries

def get_date_from_summary(file_name):
    date = file_name.split('_')[-1].split('.')[0]

    # Formatar a data
    #date = pd.to_datetime(date).date()
    return date