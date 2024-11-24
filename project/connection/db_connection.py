import pandas as pd
from psycopg2 import OperationalError
from sqlalchemy import create_engine

INITIAL_DATE = "2022/09/25"
END_DATE = "2023/01/16"


def connection() -> create_engine:
    """
    Connect with the database locally.
    """
    con = None
    try:
        con = create_engine("postgresql://postgres:aquiles159753@localhost:5432/telegramData")
        print("Successful connection.")
        return con

    except OperationalError as e:
        print(f"Error: {e}")
        return None


conn = connection()
if conn is not None:
    print(conn)


def retrieved_db(group_id) -> pd.DataFrame:
    """
    Consulte the database and returns a dataframe with 
    message_id, message_ message_utc and from_id from a certain group.
    """
    try:
        query = (
            f"SELECT messages.message_id, messages.message, messages.message_utc, messages.from_id "
            f"FROM messages "
            f"INNER JOIN channels ON messages.channel_id = channels.channel_id "
            f"WHERE channels.channel_id = {group_id} AND message_utc BETWEEN "
            f"'{INITIAL_DATE}' AND '{END_DATE}' "
        )

        df_messages = pd.read_sql(query, conn)

        # Remove empty rows
        df_messages["message"] = df_messages["message"].replace("", None)
        df_messages = df_messages.dropna(subset=["message"])
        number_of_messages = len(df_messages)

        print(f"Group ID: {group_id}:")
        print(f"Total number of messages in the group at the analyzed timestamp: {number_of_messages}")

    except Exception as e:
        print("Error: ", e)

    return df_messages


def get_groups() -> pd.DataFrame:
    """
    Get all groups from the defined TimeStamp.
    Returns a DataFrame with the group_id for each group.
    """
    try:
        query = (
            f"(SELECT m.channel_id, "
            f"COUNT(*) AS quantidade_mensagens "
            f"FROM messages m "
            f"WHERE m.channel_id "
            f"IN (SELECT channel_id FROM messages GROUP BY channel_id "
            f"HAVING COUNT(DISTINCT from_id) > 1) "
            f"AND message_utc BETWEEN '{INITIAL_DATE}' AND '{END_DATE}' "
            f"GROUP BY m.channel_id) "
            f"ORDER BY quantidade_mensagens DESC "
        )
        # f"LIMIT 1 " \

        df_groups = pd.read_sql(query, conn)

    except Exception as e:
        print("Error type: ", type(e))
        print("Error: ", e)

    df_groups = df_groups.sort_values("channel_id", ascending=False)
    return df_groups
