from psycopg2 import OperationalError
from sqlalchemy import create_engine
import pandas as pd

INITIAL_DATE = '2023/01/02'
END_DATE = '2023/01/19'

def connection() -> create_engine:
  '''Conecta com o banco de dados'''
  con = None
  try:
    con = create_engine('postgresql://postgres:aquiles159753@localhost:5432/telegramData')                 
    print("Conexão feita com sucesso.")
    return con

  except OperationalError as e:
    print(f"Error: {e}")
    return None

conn = connection()
if conn is not None:
  print(conn)

def retrieved_db(group_id) -> pd.DataFrame:
    '''Retorna um dataframe a partir de uma consulta no banco de dados'''
    try:
        query = f"SELECT messages.message_id, messages.message, messages.message_utc, messages.from_id " \
                f"FROM messages " \
                f"INNER JOIN channels ON messages.channel_id = channels.channel_id " \
                f"WHERE channels.channel_id = {group_id} AND message_utc BETWEEN '{INITIAL_DATE}' AND '{END_DATE}' "
        
        df_messages = pd.read_sql(query, conn)

        # Remover linhas vazias do df_messages
        df_messages['message'] = df_messages['message'].replace('', None)
        df_messages = df_messages.dropna(subset = ['message'])
        number_of_messages = len(df_messages)

        print(f"ID do grupo a ser analisado: {group_id}:")
        print(f"Número total de mensagens no grupo no timestamp analisado: {number_of_messages}")
        
    except Exception as e:
        print("Error: ", e)
    
    return df_messages

def get_groups() -> pd.DataFrame:
    '''Seleciona os 100 grupos com mais mensagens no Timestamp analisado'''
    try:
        query = f"(SELECT m.channel_id, " \
                f"COUNT(*) AS quantidade_mensagens " \
                f"FROM messages m " \
                f"WHERE m.channel_id " \
                f"IN (SELECT channel_id FROM messages GROUP BY channel_id HAVING COUNT(DISTINCT from_id) > 1) AND message_utc BETWEEN '{INITIAL_DATE}' AND '{END_DATE}' " \
                f"GROUP BY m.channel_id) " \
                f"ORDER BY quantidade_mensagens DESC " \
                f"LIMIT 5 " \
        
        df_groups = pd.read_sql(query, conn)

    except Exception as e:
        print("Error: ", e)
        print("Tipo do erro: ", type(e))
    
    df_groups = df_groups.sort_values('channel_id', ascending = False)
    return df_groups