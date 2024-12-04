import pandas as pd
from psycopg2 import OperationalError
from sqlalchemy import create_engine


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


def get_groups(initial_date, end_date) -> pd.DataFrame:
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
            f"AND message_utc BETWEEN '{initial_date}' AND '{end_date}' "
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
