import os

import pandas as pd

from src.data_process.data_processing import clear_messages

from .tokens import num_tokens_from_string, truncate_text_tokens_decode


def maritalk_response(input_text, max_tokens, api_client) -> str:
    """
    Sends a conversation to the Maritalk API for summarization.
    """
    response = api_client.generate(
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": "Resuma a seguinte conversa do Telegram em até 150 palavras, identificando e focando nos diferentes tópicos discutidos. "
                "Separe os tópicos utilizando um ponto final. Forneça apenas o texto dos tópicos, sem introduções ou conclusões adicionais "
                "e sem enumerar ou utilizar símbolos de divisão como hífens ou números.",
            },
            {
                "role": "user", 
                "content": input_text},
        ],
    )

    answer = response["answer"]
    return answer


def group_summary_maritalk(group_id, text_encoding, max_tokens, 
                           min_number_of_messages, api_client) -> list[str]:
    """
    Generates summaries for messages from a specific group using the Maritalk API.
    """
    group_dir = f"data/msgPerGroup/ID_{group_id}"
    csv_files = os.listdir(group_dir)
    csv_files.sort()
    summaries = []

    count = 0

    for file in csv_files:
        print(file)
        file_path = f"{group_dir}/{file}"
        df = pd.read_csv(file_path)
        num_messages = len(df)

        if num_messages > min_number_of_messages:
            messages = clear_messages(file_path)
            truncated_messages = truncate_text_tokens_decode(messages, text_encoding, max_tokens)
            prompt_tokens = num_tokens_from_string(truncated_messages, text_encoding)

            print("Amount of tokens for the prompt: ", prompt_tokens)
            count += 1

            try:
                # Append each summary to a list
                generated_summary = maritalk_response(truncated_messages, prompt_tokens, api_client)
                summaries.append(generated_summary)
                print(count)

            except Exception as e:
                print(f"Error generating summary for file: {file}: {e}")

        else:
            print(f"File {file_path} was not summarized. " 
                  f"Messages amount in the file is less than {min_number_of_messages}.")

    return summaries


def get_summaries_for_groups_maritalk(groups, text_encoding, max_tokens, 
                                      min_number_of_messages, api_client) -> list[dict]:
    """
    Generates summaries from messages for all groups using the Maritalk API.
    """
    summaries = []

    for _, row in groups.iterrows():
        group_id = row["channel_id"]
        group_summaries = group_summary_maritalk(
            group_id, text_encoding, max_tokens, min_number_of_messages, api_client
        )

        # Appends group ID and group summary in a list of dict
        summaries.append({"ID": group_id, "Sumário": group_summaries})

    return summaries
