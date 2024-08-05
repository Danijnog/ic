import os

from data.db_processing import clear_messages
from .tokens import num_tokens_from_string, truncate_text_tokens_decode

def maritalk_response(input_text, max_tokens, APIclient):
    response = APIclient.generate(
        max_tokens = max_tokens,
        messages = [
            {"role": "system", "content": "Resuma a seguinte conversa do Telegram em até 50 palavras. O sumário deve capturar os pontos-chave e destacar as informações mais relevantes. Forneça apenas o texto do sumário, sem introduções ou conclusões adicionais."},
            {"role": "user", "content": input_text}
        ]
    )

    answer = response["answer"]
    return answer

def group_summary_maritalk(group_id, text_encoding, APIclient, max_tokens) -> list:
    '''Gera o sumário para um grupo de mensagens através da API Maritalk'''
    group_dir = f'utils/msgPerGroup/ID_{group_id}'
    csv_files = os.listdir(group_dir)
    csv_files.sort()
    summaries = []

    contagem = 0

    for file in csv_files:
        file_path = f'{group_dir}/{file}'
        messages = clear_messages(file_path)
        truncated_messages = truncate_text_tokens_decode(messages, text_encoding, max_tokens)
        prompt_tokens = num_tokens_from_string(truncated_messages, text_encoding)

        #with open('utils/messages_truncated_maritalk.txt', 'a') as f:
            #f.write(f"Arquivo: {file}\n")
            #f.write(f"Mensagem truncada: {truncated_messages}\n")
            #print("\n")

        print("Número de tokens para o prompt: ", prompt_tokens)
        contagem += 1

        try:
            # Append each summary to a list
            generated_summary = maritalk_response(truncated_messages, prompt_tokens, APIclient)
            summaries.append(generated_summary)
            print(contagem)
            
        except Exception as e:
            print(f"Erro ao gerar sumarização para o arquivo: {file}: {e}")

    return summaries

def get_summaries_for_groups_maritalk(groups, text_encoding, APIclient, max_tokens) -> list:
    ''' Gera o sumário para todos os grupos através da API Maritalk'''
    summaries = []
    
    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_summaries = group_summary_maritalk(group_id, text_encoding, APIclient, max_tokens)

        # Guardar o id do grupo e o sumário do grupo em uma lista de dicionários
        summaries.append({
            "ID": group_id,
            "Sumário": group_summaries
        })

    return summaries