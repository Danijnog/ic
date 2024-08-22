import plotly.express as px

def plot_elbow_method(df):
    fig = px.line(df, x = 'num_clusters', y = 'wcss', title = "Elbow Method", width = 800, height = 600)

    return fig

def plot_days_per_cluster(filtered_df):
    
    # Agrupa o DataFrame pelo valor das colunas 'clusters' e 'date'.
    # .size() conta a quantidade de ocorrências para a combinação de 'clusters' e 'date'
    # .reset_index() transforma a série resultante em um novo df com as colunas 'clusters' e 'date' e uma nova coluna com o n de ocorrências.
    df_days_per_cluster = filtered_df.groupby(['clusters', 'date']).size().reset_index(name = 'count')
    df_cluster_total = df_days_per_cluster.groupby('clusters')['count'].sum().reset_index(name = 'total_days')
    df_days_per_cluster = df_days_per_cluster.merge(df_cluster_total, on = "clusters")
    df_days_per_cluster['proportion'] = df_days_per_cluster['count'] / df_days_per_cluster['total_days']
    df_days_per_cluster['clusters'] = df_days_per_cluster['clusters'].astype(str)

    fig = px.bar(df_days_per_cluster, x = 'date', y = 'proportion', color = 'clusters', title = 'Dias por cluster', range_x = [df_days_per_cluster['date'].min(), df_days_per_cluster['date'].max()])
    fig.update_layout(yaxis_title = 'Proporção de dias/cluster', xaxis_title = 'Data')

    return fig