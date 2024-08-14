import pandas as pd
import plotly.express as px
import numpy as np
import os

def get_dfs_for_distribution_function(groups, min_number_of_messages):
    """Retorna dois DataFrames que serão utilizado para construir os gráficos de distribuição acumulada.
    O primeiro df é utilizado para construir os CDFs da quantidade de mensagens/dia e usuários ativos/dia, enquanto o segundo df
    é utilizado para construir o CDF da quantidade de dias/grupo que possuem mensagens após o limiar estabelecido com o 
    mínimo número de mensagens."""

    data_messages_active_users = []
    data_days = []

    for index, row in groups.iterrows():
        group_id = row['channel_id']
        group_dir = f'data/msgPerGroup/ID_{group_id}'
        csv_files = os.listdir(group_dir)
        csv_files.sort()
        num_days_message = 0

        for file in csv_files:
            file_path = f'{group_dir}/{file}'
            df = pd.read_csv(file_path)
            date = file.split('_')[-1].split('.')[0]
            num_messages = len(df)

            data_messages_active_users.append({
                'ID': group_id,
                'quantidade_mensagens': len(df),
                'date': date,
                'active_users': df['from_id'].nunique()
            })

            if num_messages > min_number_of_messages:
                num_days_message += 1
        
        data_days.append({
            'ID': group_id,
            'num_dias_grupo_com_mensagem': num_days_message,
        })

    df_cdf_messages_active_users = pd.DataFrame(data_messages_active_users)
    df_cdf_days = pd.DataFrame(data_days)

    return df_cdf_messages_active_users, df_cdf_days

def cumulative_distribution_function(df_cdf_messages_active_users, df_cdf_days, min_number_of_messages):
    """ Retorna os gráficos de distribuição acumulada da quantidade de mensagens de cada dia por grupo, a quantidade de usuários ativos de cada dia por grupo e
    a quantidade de dias-grupo que possuem mensagens após o limiar estabelecido com o mínimo número de mensagens."""
    
    df_cdf = pd.DataFrame(df_cdf_messages_active_users)
    messages_distribution_fig = px.ecdf(df_cdf, x = 'quantidade_mensagens')
    active_users_distribution_fig = px.ecdf(df_cdf, x = 'active_users')
    messages_distribution_fig.update_layout(yaxis_title = 'P(X <= x)', width = 800, height = 600)
    active_users_distribution_fig.update_layout(yaxis_title = 'P(X <= x)', width = 800, height = 600)

    dff_cdf = pd.DataFrame(df_cdf_days)
    days_distribution_fig = px.ecdf(dff_cdf, x = 'num_dias_grupo_com_mensagem')
    days_distribution_fig.update_layout(yaxis_title = 'P(X <= x)', xaxis_title = f'quantidade_dias_grupo_com_mensagem (Limiar acima de {min_number_of_messages} mensagens)', width = 800, height = 600)

    return messages_distribution_fig, active_users_distribution_fig, days_distribution_fig