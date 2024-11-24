import os

import pandas as pd
import plotly.express as px

from connection import clear_messages


def embedding_scatter_plot(df) -> tuple[px.scatter, pd.DataFrame]:
    """
    Creates a scatter plot for low-dimensional embeddings.
    """
    # Sort the cluster for consistent cluster colors on the scatter plot
    df = df.sort_values(by=["cluster", "ID", "date"])

    fig = px.scatter(
        df,
        x="x",
        y="y",
        hover_name=df["label"].apply(
            lambda x: "<br>".join(x[i : i + 50] for i in range(0, len(x), 50))
        ),
        hover_data={"date", "ID"},
        color="cluster",
        title="Embedding Summary",
        width=800,
        height=600,
    )

    return fig, df


def get_df_for_plot(low_dim_embeddings, labels, date_labels, clusters_labels) -> pd.DataFrame:
    """
    Creates a DataFrame containing embeddings and metadata for plotting.
    """
    assert low_dim_embeddings.shape[0] >= len(labels), "More labels than embeddings."

    df = pd.DataFrame(low_dim_embeddings, columns=["x", "y"])

    df["label"] = [groups["Sumário"] for groups in labels]
    df["ID"] = [groups["ID"] for groups in labels]
    df["date"] = date_labels
    df["cluster"] = clusters_labels

    # Cluster and ID transformation type for consistent plotting
    df["cluster"] = df["cluster"].astype(str)
    df["ID"] = df["ID"].astype(str)

    return df


def remove_cluster(df, cluster_list) -> pd.DataFrame:
    """
    Removes rows from the DataFrame corresponding to specific clusters.
    """
    df_copy = df.copy()

    df_copy["cluster"] = df_copy["cluster"].astype(int)
    new_cluster_df = df_copy[~df_copy["cluster"].isin(cluster_list)]

    return new_cluster_df


def remove_groups(df, group_list) -> pd.DataFrame:
    """
    Removes rows from the DataFrame corresponding to specific groups.
    """
    df_copy = df.copy()

    new_group_df = df_copy[~df_copy["ID"].isin(group_list)]

    return new_group_df


def remove_days_groups(df, group_list, day_list) -> pd.DataFrame:
    """
    Removes rows from the DataFrame corresponding to specific group and date combinations.
    """
    df_copy = df.copy()

    # Iterate through the pair of group_list and day_list
    for group, day in zip(group_list, day_list):
        df_copy = df_copy[
            ~((df_copy["ID"] == group) & (df_copy["date"] == day))
        ]  # Remove rows that correponds to the specific pair

    return df_copy


def get_df_for_recluster(df, cluster_labels, cluster_list, group_list, day_list) -> pd.DataFrame:
    """
    Prepares a DataFrame for re-clustering by removing specified clusters and group-day 
    combinations.
    """
    new_df = df.copy()
    new_df = remove_cluster(new_df, cluster_list)
    new_df = remove_days_groups(new_df, group_list, day_list)

    new_df["cluster"] = cluster_labels
    new_df["cluster"] = new_df["cluster"].astype(str)

    return new_df


def get_new_high_dim_embedding(high_dim_embeddings, labels, date_labels, 
                               clusters_labels, cluster_list, 
                               group_list, day_list) -> pd.DataFrame:
    """
    Returns a new high-dimensional embedding DataFrame after removing outliers.
    """
    assert high_dim_embeddings.shape[0] >= len(labels), "More labels than embeddings."

    df = pd.DataFrame(
        high_dim_embeddings, columns=[f"dim{i}" for i in range(high_dim_embeddings.shape[1])]
    )

    df["label"] = [groups["Sumário"] for groups in labels]
    df["ID"] = [groups["ID"] for groups in labels]
    df["date"] = date_labels
    df["cluster"] = clusters_labels

    # Cluster and ID transformation type for consistent operations
    df["cluster"] = df["cluster"].astype(str)
    df["ID"] = df["ID"].astype(str)

    df_for_recluster = remove_cluster(df, cluster_list)
    df_for_recluster = remove_days_groups(df_for_recluster, group_list, day_list)

    new_high_dim_embeddings_umap = df_for_recluster.iloc[:, 0 : high_dim_embeddings.shape[1]]

    return new_high_dim_embeddings_umap


def get_df_for_remove_days_groups_that_has_less_25_messages(groups, min_number_of_messages) -> pd.DataFrame:
    """
    Identifies group-day combinations with fewer than the minimum required messages after cleaning.
    """
    data = []

    for _, row in groups.iterrows():
        group_id = row["channel_id"]
        group_dir = f"data/msgPerGroup/ID_{group_id}"
        csv_files = os.listdir(group_dir)
        csv_files.sort()

        for file in csv_files:
            file_path = f"{group_dir}/{file}"
            df = pd.read_csv(file_path)
            date = file.split("_")[-1].split(".")[0]
            num_messages = len(df)

            if num_messages > min_number_of_messages:
                _, df_clear_messages = clear_messages(file_path)
                num_clear_messages = len(df_clear_messages)

                if num_clear_messages < min_number_of_messages:
                    data.append(
                        {
                            "ID": group_id,
                            "date": date,
                        }
                    )

    df = pd.DataFrame(data)

    return df


def remove_days_groups_that_has_less_25_messages(df, groups, min_number_of_messages):
    """
    Removes group-day combinations remained on the DataFrame clusterization
    with fewer than the specified number of messages.
    """
    df_copy = df.copy()

    dff = get_df_for_remove_days_groups_that_has_less_25_messages(groups, min_number_of_messages)

    df_copy["ID"] = df_copy["ID"].astype(int)
    dff["ID"] = dff["ID"].astype(int)
    
    # Merge both dataframes to identify the combination of rows of "ID" and "date" in df_copy e dff
    # 'Indicator' parameter from pd.merge adds a new column to de df that shows which rows
    # are present just in df_copy (left) or in both DataFrames
    merged_df = pd.merge(df_copy, dff, on=["ID", "date"], how="left", indicator=True)
    filtered_df = (
        merged_df[merged_df["_merge"] == "left_only"].drop(columns="_merge").reset_index(drop=True)
    )

    return filtered_df


def filter_df(df, days) -> pd.DataFrame:
    """
    Filters the DataFrame to specified days for analysis.
    """
    filtered_df = df.copy()

    filtered_df = filtered_df[filtered_df["date"].isin(days)]

    return filtered_df
