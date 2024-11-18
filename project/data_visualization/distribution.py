import pandas as pd
import plotly.express as px
import os

def get_dfs_for_distribution_function(groups, min_number_of_messages):
    """Retorna dois DataFrames que serão utilizado para construir os gráficos de distribuição acumulada.
    O primeiro df é utilizado para construir os CDFs da quantidade de mensagens/dia e usuários ativos/dia, enquanto o segundo df
    é utilizado para construir o CDF da quantidade de dias/grupo que possuem mensagens após o limiar estabelecido com o 
    mínimo número de mensagens."""

    data_messages_active_users = []
    data_days = []

    for _, row in groups.iterrows():
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
    messages_distribution_fig = px.ecdf(df_cdf, x = 'quantidade_mensagens', title = "Figura 1")
    active_users_distribution_fig = px.ecdf(df_cdf, x = 'active_users', title = "Figura 3")
    messages_distribution_fig.update_layout(yaxis_title = 'P(X <= x)', width = 400, height = 300)
    active_users_distribution_fig.update_layout(yaxis_title = 'P(X <= x)', width = 400, height = 300)

    dff_cdf = pd.DataFrame(df_cdf_days)
    days_distribution_fig = px.ecdf(dff_cdf, x = 'num_dias_grupo_com_mensagem', title = "Figura 2")
    days_distribution_fig.update_layout(yaxis_title = 'P(X <= x)', xaxis_title = f'qtd_dias_grupo_com_msg (Limiar acima de {min_number_of_messages} mensagens)', width = 400, height = 300)

    return messages_distribution_fig, active_users_distribution_fig, days_distribution_fig

def plot_groups_per_cluster(filtered_df):
    """Retorna uma figura que mostra a proporção da quantidade de grupos por cluster em cada dia.
    O agrupamento é feito por cluster."""

    # Agrupa o DataFrame pelo valor das colunas 'clusters' e 'date'.
    # .size() conta a quantidade de ocorrências para a combinação de 'clusters' e 'date'
    # .reset_index() transforma a série resultante em um novo df com as colunas 'clusters' e 'date' e uma nova coluna com o n de ocorrências.
    df_days_per_cluster = filtered_df.groupby(['cluster', 'date']).size().reset_index(name = 'count')
    df_cluster_total = df_days_per_cluster.groupby('cluster')['count'].sum().reset_index(name = 'total_days')
    df_days_per_cluster = df_days_per_cluster.merge(df_cluster_total, on = "cluster")

    # Calcular a proporção da quantidade de grupos em cada cluster por cluster
    df_days_per_cluster['proportion'] = df_days_per_cluster['count'] / df_days_per_cluster['total_days']
    df_days_per_cluster['cluster'] = df_days_per_cluster['cluster'].astype(str)

    # Ajustar a data para mostrar no formato dd/mm
    df_days_per_cluster['date'] = pd.to_datetime(df_days_per_cluster['date'])
    df_days_per_cluster['date'] = df_days_per_cluster['date'].dt.strftime("%d/%m")

    fig = px.bar(df_days_per_cluster, x = 'date', y = 'proportion', color = 'cluster', title = 'Proporção de grupos por cluster de cada dia', barmode = 'group')
    fig.update_layout(yaxis_title = 'Proporção de grupos/cluster', xaxis_title = 'Data')

    return fig

def plot_groups_per_date(filtered_df):
    """Retorna uma figura que mostra a proporção da quantidade de grupos por dia de cada cluster.
    O agrupamento é feito por data."""

    df_groups_per_day = filtered_df.groupby(['cluster', 'date']).size().reset_index(name = 'count_groups')
    df_total_groups_per_day = df_groups_per_day.groupby('date')['count_groups'].sum().reset_index(name = 'total_groups_per_day')
    df_groups_per_day = df_groups_per_day.merge(df_total_groups_per_day, on = 'date')

    # Calcular a proporção da quantidade de grupos em cada cluster por dia
    df_groups_per_day['proportion'] = df_groups_per_day['count_groups'] / df_groups_per_day['total_groups_per_day']
    df_groups_per_day['cluster'] = df_groups_per_day['cluster'].astype(str)

    # Ajustar a data para mostrar no formato dd/mm
    df_groups_per_day['date'] = pd.to_datetime(df_groups_per_day['date'])
    df_groups_per_day['date'] = df_groups_per_day['date'].dt.strftime("%d/%m")

    fig = px.bar(df_groups_per_day, x = 'date', y = 'proportion', color = 'cluster', barmode = 'group', title = "Proporção de grupos por dia de cada cluster")
    fig.update_layout(xaxis_title = "Data", yaxis_title = "Proporção de grupos/dia")

    return fig