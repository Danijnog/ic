import pandas as pd
import plotly.express as px
import numpy as np
import os

def get_df_for_distribution_function(groups):
    """Retorna um DataFrame que será utilizado para construir os gráficos de distribuição acumulada."""
    data = []

    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_dir = f'data/msgPerGroup/ID_{group_id}'
        csv_files = os.listdir(group_dir)
        csv_files.sort()

        for file in csv_files:
            file_path = f'{group_dir}/{file}'
            df = pd.read_csv(file_path)
            date = file.split('_')[-1].split('.')[0] 

            data.append({
                'ID': group_id,
                'quantidade_mensagens': len(df),
                'date': date,
                'active_users': df['from_id'].nunique()
            })

    df_cdf = pd.DataFrame(data)

    return df_cdf

def cumulative_distribution_function(df):
    """ Retorna os gráficos de distribuição acumulada da quantidade de mensagens de cada dia por grupo, e a quantidade de usuários ativos de cada dia por grupo."""
    df_cdf = pd.DataFrame(df)
 
    messages_distribution_fig = px.ecdf(df_cdf, x = 'quantidade_mensagens')
    active_users_distribution_fig = px.ecdf(df_cdf, x = 'active_users')
    messages_distribution_fig.update_layout(yaxis_title = 'P(X <= x)')
    active_users_distribution_fig.update_layout(yaxis_title = 'P(X <= x)')

    return messages_distribution_fig, active_users_distribution_fig