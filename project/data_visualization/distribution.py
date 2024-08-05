import pandas as pd
import plotly.express as px
import numpy as np
import os

def get_df_for_distribution_function(groups):
    """Retorna um DataFrame que será utilizado para construir os gráficos de distribuição acumulada."""
    data = []

    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_dir = f'utils/msgPerGroup/ID_{group_id}'
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
    df_cdf = df_cdf.sort_values(by = 'quantidade_mensagens')
    df_cdf['messages_cumulative_distribution'] = np.cumsum(df_cdf['quantidade_mensagens']) / np.sum(df_cdf['quantidade_mensagens'])

    dff_cdf = pd.DataFrame(df)
    dff_cdf = dff_cdf.sort_values(by = 'active_users')
    dff_cdf['active_users_cumulative_distribution'] = np.cumsum(dff_cdf['active_users']) / np.sum(dff_cdf['active_users'])


    messages_distribution_fig = px.line(df_cdf, x = 'quantidade_mensagens', y = 'messages_cumulative_distribution', title = 'Distribuição acumulada de mensagens')
    messages_distribution_fig.update_layout(xaxis_title = 'quantidade de mensagens', yaxis_title = 'P(X <= x)')

    active_users_distribution_fig = px.line(dff_cdf, x = 'active_users', y = 'active_users_cumulative_distribution', title = 'Distribuição acumulada de usuários ativos')
    active_users_distribution_fig.update_layout(xaxis_title = 'quantidade de usuários ativos', yaxis_title = 'P(X <= x)')

    return messages_distribution_fig, active_users_distribution_fig


