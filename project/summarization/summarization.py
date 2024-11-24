import os

import pandas as pd

from connection.db_processing import clear_messages

from .tokens import num_tokens_from_string, truncate_text_tokens_decode


def generate_summary(input_text, model, api_client) -> str:
    """
    Sends a conversation to an API for summarization.
    """
    try:
        response = api_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Você receberá mensagens de conversas do Telegram, e sua tarefa " 
                    "é gerar um sumário conciso de no máximo 150 palavras das mensagens.",
                },
                {
                    "role": "user", 
                    "content": input_text},
            ],
        )

    except Exception as e:
        print("Error type: ", type(e))
        print("Error: ", e)

    return response.choices[0].message.content


def group_summary(group_id, text_encoding, text_model, 
                  max_tokens, min_number_of_messages, api_client) -> list[str]:
    """
    Generates summaries for messages from a specific group using an API.
    """
    group_dir = f"data/msgPerGroup/ID_{group_id}"
    csv_files = os.listdir(group_dir)
    csv_files.sort()
    summaries = []
    print(f"Group: {group_id}")

    count = 0
    total_tokens = 0
    total_clear_messages = 0

    for file in csv_files:
        print(file)
        file_path = f"{group_dir}/{file}"
        df = pd.read_csv(file_path)
        num_messages = len(df)

        if num_messages > min_number_of_messages:
            messages, df_clear_messages = clear_messages(file_path)
            num_clear_messages = len(df_clear_messages)
            truncated_messages = truncate_text_tokens_decode(messages, text_encoding, max_tokens)
            prompt_tokens = num_tokens_from_string(truncated_messages, text_encoding)

            print("Tokens amount for the prompt: ", prompt_tokens)
            total_tokens = total_tokens + prompt_tokens
            total_clear_messages = total_clear_messages + num_clear_messages
            count += 1

            try:
                # Append each summary to a list
                generated_summary = generate_summary(truncated_messages, text_model, api_client)
                summaries.append(generated_summary)
                print(count)

            except Exception as e:
                print(f"Error generating summary for file: {file}: {e}")
                print("/n")

        else:
            print(
                f"File {file_path} was not summarized. "
                f"Messages amount in the file is less than {min_number_of_messages}."
            )

    print(f"Group: {group_id}, Total tokens amount: ", total_tokens)
    print(f"Group: {group_id}, Total messages amount (after been cleaned): ", total_clear_messages)

    return summaries


def get_summaries_for_groups(groups, text_encoding, text_model, 
                             max_tokens, min_number_of_messages, api_client) -> list[dict]:
    """
    Generates summaries for messages of all groups using an API.
    """
    summaries = []

    for _, row in groups.iterrows():
        group_id = int(row["channel_id"])
        group_summaries = group_summary(
            group_id, text_encoding, text_model, max_tokens, min_number_of_messages, api_client
        )

        # Appends group ID and group summary in a list of dict
        summaries.append({"ID": group_id, "Sumário": group_summaries})

    return summaries


def get_date_from_summary(file_name) -> str:
    """
    Splits a file name with a certain format to get the date from the name.
    """
    date = file_name.split("_")[-1].split(".")[0]

    return date


def remove_item_from_summaries(id_list, summaries) -> list[dict]:
    """
    Removes items from a list of dictionaries based on a list of IDs.
    """
    new_summaries = [item for item in summaries if item["ID"] not in id_list]

    return new_summaries
