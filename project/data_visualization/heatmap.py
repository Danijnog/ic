import pandas as pd

import clusterization


def generate_transition_list_for_heatmap(df, day1, day2) -> list:
    """
    Transforms the Transition Matrix to a list to build the heatmap.
    """
    df["date"] = pd.to_datetime(df["date"])
    num_clusters = df["cluster"].nunique()

    transition_list = []
    transition_matrix = clusterization.build_transition_matrix(df, day1, day2)

    for from_cluster in range(num_clusters):
        for to_cluster in range(num_clusters):
            transition_list.append(transition_matrix[from_cluster, to_cluster])
        
    return transition_list


def generate_transitions_for_heatmap(df) -> list[list]:
    """
    Generates a transition list that will be used to build the Heatmap.
    The len of the list is equal to the amount of transitions that we have
    for all clusters.
    """
    unique_dates = df["date"].sort_values().unique()
    num_clusters = df["cluster"].nunique()
    num_transitions = num_clusters * num_clusters

    # Initialize a larger list with empty sublists for each transition
    heatmap = [[] for _ in range(num_transitions)]
    index = 0

    for i in range(len(unique_dates) - 1):
        day1 = unique_dates[i]
        day2 = unique_dates[i + 1]
        heatmap[index].append(generate_transition_list_for_heatmap(df, day1, day2))
        index += 1
        index = 0 if index >= len(heatmap) else index 
    
    return heatmap