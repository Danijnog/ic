import numpy as np
import pandas as pd

def get_df_for_trajectory(high_dim_embeddings, labels, date_labels):
    """Cria um DataFrame dos Embeddings de 10 dimensões para ser usado para calcular a trajetória dos pontos."""
    df = pd.DataFrame(high_dim_embeddings, columns = [f"dim{i}" for i in range(high_dim_embeddings.shape[1])])
    df['label'] = [groups["Sumário"] for groups in labels]
    df['ID'] = [groups["ID"] for groups in labels]
    df['date'] = date_labels

    # Transformar o ID em string para fazer a legenda
    df['ID'] = df['ID'].astype(str)

    return df

def get_group_trajectory(group_id, df):
    """Calcula a trajetória dos pontos de um grupo ao longo dos dias do período analisado."""
    group_data = df.copy()
    group_data = group_data[group_data['ID'] == group_id].sort_values(by = 'date') # Filtrar o df para conter apenas os dados do grupo escolhido
    trajectory = []

    for i in range(1, len(group_data)):
        distance = np.linalg.norm(group_data.iloc[i, :10] - group_data.iloc[i - 1, :10]) # Calcular a distância euclidianda entre os embeddings de dois dias consecutivos
        trajectory.append(distance)

    return trajectory

def get_all_groups_trajectories(df):
    """Calcula a trajetória dos pontos de todos os grupos ao longo dos dias do período analisado."""
    groups = df['ID'].unique()
    trajectories = []

    for group_id in groups:
        trajectory = get_group_trajectory(group_id, df)
        
        # Calcular a média e o desvio padrão da trajetória e verificar exceções
        trajectory_mean = 0 if len(trajectory) == 0 else np.mean(trajectory)
        trajectory_std = 0 if len(trajectory) == 1 | 0 else np.std(trajectory) # Se tivermos apenas uma trajetória (2 pontos) o desvio padrão é 0
        trajectories.append({
            'ID': group_id,
            'Trajetoria': trajectory,
            'Media': trajectory_mean,
            'Desvio Padrao': trajectory_std
        })
    
    return trajectories