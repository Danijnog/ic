import os
import pickle

import numpy as np
import pandas as pd
import torch


def embedding(text, tokenizer, model) -> torch.Tensor:
    """
    Generates an embedding for the given text using a specified tokenizer and model.
    - Note: this function was used to use BERTimbau model for compute embeddings.
    """

    # 512 is the maximum limit of max_length to ensure that the extracted text does not exceed the
    #  amount of tokens that the model is capable of handling
    inputs_ids = tokenizer.encode(str(text), return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(inputs_ids)
        embedding = outputs.last_hidden_state[0, 1:-1]

    return embedding.mean(dim=0)


def get_embeddings(summaries, tokenizer, model) -> torch.Tensor:
    """
    Computes embeddings for all groups that are in the list of dict 'summaries'.
    - Note: this function was used to use BERTimbau model for compute embeddings.
    """
    all_embeddings = []

    for group in summaries:
        group_id = group["ID"]
        group_summaries = group["Sumário"]

        if group_summaries:  # Check if the list of summaries of the groups isn't empty
            embeddings = torch.stack(
                [embedding(text, tokenizer, model) for text in group_summaries]
            )
            all_embeddings.append(embeddings)

        else:
            print(
                f"The group {group_id} has no summaries. "
                f"This is because the group did not actually have any messages "
                f"in the analyzed period, or the messages were cleaned "
                f"and there is no useful information to summarize."
            )

    all_embeddings = torch.cat(all_embeddings, dim=0)
    return all_embeddings


def gpt_embedding(text, model, client) -> list:
    """
    Generates an embedding for the given text using a GPT-based embedding model.
    - Note: this function was used to use GPT model for compute embeddings.
    """
    response = client.embeddings.create(
        input=text,
        model=model,
    )

    return response.data[0].embedding


def get_gpt_embeddings(summaries, model, client) -> list:
    """
    Computes GPT-based embeddings for all groups that are in the list of dict 'summaries'.
    - Note: this function was used to use GPT model for compute embeddings.
    """
    all_embeddings = []

    for group in summaries:
        group_id = group["ID"]
        group_summaries = group["Sumário"]

        if group_summaries:
            embeddings = [gpt_embedding(text, model, client) for text in group_summaries]
            all_embeddings.extend(embeddings)

        else:
            print(
                f"The group {group_id} has no summaries. "
                f"This is because the group did not actually have any messages "
                f"in the analyzed period, or the messages were cleaned "
                f"and there is no useful information to summarize."
            )

    return all_embeddings


def normalize_l2(embeddings) -> np.ndarray:
    """
    Performs L2 normalization on embeddings.
    """
    embeddings = np.array(embeddings)

    if embeddings.ndim == 1:
        l2_norm = np.linalg.norm(embeddings)

        # If the norm value is 0, it returns the embedding value, if not it returns the normalized value
        return np.where(l2_norm == 0, embeddings, embeddings / l2_norm)

    # For a matrix (2D array), normalization has to be done row by row (each vector individually) 
    # (axis = 1)
    l2_norm = np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)

    return np.where(l2_norm == 0, embeddings, embeddings / l2_norm)


def save_embedding(embeddings, file_name):
    """
    Saves embeddings to a binary file using Pickle.
    """
    with open(file_name, "wb") as f:
        pickle.dump(embeddings, f)
        f.close()


def get_embedding_saved(file_name):
    """
    Loads embeddings from a saved binary file using Pickle.
    """
    with open(file_name, "rb") as f:
        embeddings = pickle.load(f)
        f.close()

    return embeddings


def get_labels(summaries) -> list:
    """
    Extracts IDs and summaries from a list of group dictionaries.
    """
    labels = []

    for group in summaries:
        for text in group["Sumário"]:
            labels.append({"ID": group["ID"], "Sumário": text})

    return labels


def get_date_labels(groups, min_number_of_messages):
    """
    Extracts date labels from message files of groups that meet a minimum message count.
    """
    date_labels = []

    for _, row in groups.iterrows():
        group_id = row["channel_id"]
        group_dir = f"data/msgPerGroup/ID_{group_id}"
        csv_files = os.listdir(group_dir)
        csv_files.sort()

        group_dates = []
        for file in csv_files:
            file_path = f"{group_dir}/{file}"
            df = pd.read_csv(file_path)
            num_messages = len(df)

            # Verification to add only date from files that has summaries
            if (num_messages > min_number_of_messages):
                group_dates.append(file)

        date_labels.append(group_dates)

    date_list = []
    for date in date_labels:
        for file in date:
            date_list.append(
                file.split("_")[-1].split(".")[0]
            )  # Extract only date from file name

    return date_list
