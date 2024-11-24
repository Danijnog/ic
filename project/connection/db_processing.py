import csv
import os
import re

import emoji
import pandas as pd

from .db_connection import retrieved_db


def separate_messages_in_days(df_messages, group_id) -> None:
    """
    Splits messages into separate days based on their timestamp and saves them as CSV files.
    The function creates a CSV file for each unique date per group within the provided DataFrame.
    """
    try:
        df_messages["message_utc"] = pd.to_datetime(df_messages["message_utc"])
        df_messages["date"] = df_messages["message_utc"].dt.date  # Separates date from hour
        df_messages["time"] = df_messages["message_utc"].dt.time  # Separates hour from date

        # Save messages for each unique date in separated CSV files
        for date in df_messages["date"].unique():
            csv_path = f"data/msgPerGroup/ID_{group_id}/messages_{date}.csv"

            if not os.path.exists(csv_path):
                df_messages_date = df_messages[df_messages["date"] == date]
                df_messages_date.to_csv(csv_path, header="True", index=False, quoting=csv.QUOTE_ALL)
                print(f"Messages from {date} saved successfully to {csv_path}")

    except Exception as e:
        print("Error type: ", type(e))
        print("Error: ", e)


def get_separated_messages(groups) -> None:
    """
    Retrieves messages for each group, splits them into days, and saves them as CSV files.
    """
    df_groups = groups
    amount = 0

    for _, row in df_groups.iterrows():
        group_id = row["channel_id"]

        # Creates a directory for each group if it doesn't exist
        group_dir = f"data/msgPerGroup/ID_{group_id}"
        os.makedirs(group_dir, exist_ok=True)

        # Retrieve messages from the database for the given group
        df_retrieval = retrieved_db(group_id)
        amount = amount + len(df_retrieval)

        # Split messages into days and save them as CSV files
        separate_messages_in_days(df_retrieval, group_id)

    print("Total de mensagens recuperadas de todos os grupos:", amount)

def clean_messages(messages) -> pd.Series:
    """
    Cleans a Series of messages by removing emojis, URLs, user mentions, extra spaces,
    repeated characters, and repeated words.
    """

    # Remove emojis
    messages = emoji.replace_emoji(messages, "")

    # Remove URLs
    messages = re.sub(r"https?\S+", "", messages)

    # Remove user mentions
    messages = re.sub("@\w+", "", messages)

    # Remove extra spaces
    messages = re.sub(r" +", r" ", messages)

    # Remove repeated line breaks
    messages = re.sub(r"([\r\n]+)+", r" ", messages)

    # Remove consecutive repeated characters
    messages = re.sub(r"(.)\1{2,}", r"\1", messages)

    # Remove consecutive repeated words
    messages = re.sub(r"\b(\w+)( \1\b)+", r"\1", messages)

    return messages


def clear_messages(file_name) -> tuple[str, pd.DataFrame]:
    """
    Reads a CSV file, cleans the messages, and returns the cleaned messages as a single concatenated
    string and a DataFrame.
    """
    try:
        df = pd.read_csv(file_name)

        # Drop null and duplicated messages
        messages = df["message"]
        messages = messages.dropna()
        messages = messages.drop_duplicates()

        # Apply cleaning function to messages
        messages = messages.apply(clean_messages)

        # Remove rows with only whitespace or empty strings
        df_clean_messages = pd.DataFrame(messages)
        df_clean_messages = df_clean_messages[
            ~df_clean_messages.apply(lambda row: row.str.strip().eq("").all(), axis=1)
        ]
        print("Number of messages after cleaning: ", len(df_clean_messages))

        # Converts cleaned messages to a single string for summarization
        clean_message = df_clean_messages["message"]
        clean_message = clean_message.tolist()
        clean_message = " ".join(str(message) for message in clean_message)

    except Exception as e:
        print("Error: ", e)

    return clean_message, df_clean_messages
