import numpy as np
import pandas as pd
from graphviz import Digraph

def build_transition_matrix(df, day1, day2):
    # Filtrar os dados para os dois dias
    day1_data = df[df['date'] == day1][['ID', 'cluster']]
    day2_data = df[df['date'] == day2][['ID', 'cluster']]

    # Número de estados (clusters) que temos
    num_clusters = df['cluster'].nunique()
    df['date'] = pd.to_datetime(df['date'])

    # Unir os dois dias pelos IDs dos grupos
    merged_data = pd.merge(day1_data, day2_data, on = 'ID', suffixes = ('_day1', '_day2'))

    # Inicializar matriz de transição
    transition_matrix = np.zeros((num_clusters, num_clusters))

    # Preencher a matriz de transição de acordo com a transição do grupo de um cluster para outro entre dois dias
    for _, row in merged_data.iterrows():
        cluster_day1 = row['cluster_day1']
        cluster_day2 = row['cluster_day2']
        transition_matrix[int(cluster_day1), int(cluster_day2)] += 1
    
    # Normalização da matriz (Norma L1)
    for i in range(num_clusters):
        total_values_row = transition_matrix[i].sum()
        if total_values_row > 0:
            transition_matrix[i] /= total_values_row
    
    return transition_matrix

def plot_transition_graph(transition_matrix, day1, day2):
    dot = Digraph(format = 'png')

    # Nós (clusters)
    for i in range(len(transition_matrix)):
        dot.node(str(i), label = f"Cluster {i}", fontsize = '12')
    
    # Arestas (matriz de transição)
    for a in range(len(transition_matrix)):
        for b in range(len(transition_matrix)):
            if transition_matrix[a][b] > 0:
                dot.edge(str(a), str(b), label = f"{transition_matrix[a][b]*100:.2f}%", fontsize = '10')
    
    dot.attr(label = f"Transição entre {day1.date()} e {day2.date()}")
    dot.attr(labelloc = 'top')

    print(f"Matriz de Transição utilizada para construir o grafo: {transition_matrix}")
    
    #Renderizar o grafo para um arquivo e exibir
    path = f'utils/transition_graph/transition_graph_{day1.date()}_{day2.date()}'
    dot.render(path, view = True)

def transition_graph(df):
    unique_dates = df['date'].sort_values().unique()

    for i in range(len(unique_dates) - 1):
        day1 = unique_dates[i]
        day2 = unique_dates[i + 1]
        transition_matrix = build_transition_matrix(df, day1, day2)
        plot_transition_graph(transition_matrix, day1, day2)