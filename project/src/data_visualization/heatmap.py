import pandas as pd
import plotly.express as px

from src import clusterization


def get_transitions_list_for_heatmap(df) -> list[list]:
    """
    Transforms the Transition Matrix to a list to build the heatmap.
    """
    df["date"] = pd.to_datetime(df["date"])
    unique_dates = df["date"].sort_values().unique()
    num_clusters = df["cluster"].nunique()
    num_transitions = num_clusters * num_clusters

    # Initialize a larger list with empty sublists for each transition
    heatmap = [[] for _ in range(num_transitions)]

    for i in range(len(unique_dates) - 1):
        day1 = unique_dates[i]
        day2 = unique_dates[i + 1]
        transition_matrix = clusterization.build_transition_matrix(df, day1, day2)

        for from_cluster in range(num_clusters):
            for to_cluster in range(num_clusters):
                index = from_cluster * num_clusters + to_cluster
                heatmap[index].append(transition_matrix[from_cluster, to_cluster])
        
    return heatmap

def plot_heatmap(heatmap: list[list], df) -> None:
    """
    Generates the Heatmap based on the transitions that we have.
    """
    unique_dates = df["date"].sort_values().unique()
    num_clusters = df["cluster"].nunique()
    fig = px.imshow(heatmap, labels=dict(x="Date", y="Clusters Transition", color="Transition Probability", title="Transition Matrix Heatmap"),
              x=unique_dates[1:], y=[f"{a} -> {b}" for a in range(num_clusters) for b in range(num_clusters)])
    
    return fig