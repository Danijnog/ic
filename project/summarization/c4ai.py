import os

from .tokens import num_tokens_from_string, truncate_text_tokens_decode
from data.db_processing import clear_messages

def c4_ai_response(input_text, max_tokens, model, client):
    response = client.chat(
        message = """
## Instruções
Faça um pequeno sumário de no máximo 50 palavras a partir da seguinte conversa do Telegram. O sumário deve capturar os pontos-chave e destacar as informações mais relevantes da conversa.

## Input text
""" + input_text,
        model = model,
        max_tokens = max_tokens,
    )
    return response.text


# Summary from a group of messages
def group_summary_C4AI(group_id, text_encoding, text_model, max_tokens, APIclient) -> list:
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

        contagem += 1

        try:
            # Append each summary to a list
            generated_summary = c4_ai_response(truncated_messages, prompt_tokens, text_model, APIclient)
            summaries.append(generated_summary)
            print(contagem)
            
        except Exception as e:
            print(f"Erro ao gerar sumarização para o arquivo: {file}: {e}")

    return summaries
