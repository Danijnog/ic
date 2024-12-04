import os

import pandas as pd
import plotly.express as px


def get_dfs_for_distribution_function(groups, min_number_of_messages) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process a set of groups and extracts message and user activity data for each day,
    as well as counts the number of days a group exceeds a threshold of messages.
    The first returned DataFrame will be used for the CDF of the amount of messages/day and active users/day.
    The second returned DataFrame will be used for the CDF of the amount of days/group that have messages after
    the threshold established with the min_number_of_messages.
    """
    data_messages_active_users = []
    data_days = []

    for _, row in groups.iterrows():
        group_id = row["channel_id"]
        group_dir = f"data/msgPerGroup/ID_{group_id}"
        csv_files = os.listdir(group_dir)
        csv_files.sort()
        num_days_message = 0

        for file in csv_files:
            file_path = f"{group_dir}/{file}"
            df = pd.read_csv(file_path)
            date = file.split("_")[-1].split(".")[0]
            num_messages = len(df)

            data_messages_active_users.append(
                {
                    "ID": group_id,
                    "num_messages": len(df),
                    "date": date,
                    "active_users": df["from_id"].nunique(),
                }
            )

            if num_messages > min_number_of_messages:
                num_days_message += 1

        data_days.append(
            {
                "ID": group_id,
                "num_days_groups_with_messages": num_days_message,
            }
        )

    df_cdf_messages_active_users = pd.DataFrame(data_messages_active_users)
    df_cdf_days = pd.DataFrame(data_days)

    return df_cdf_messages_active_users, df_cdf_days


def cumulative_distribution_function(df_cdf_messages_active_users, df_cdf_days, min_number_of_messages) -> tuple[px.ecdf, px.ecdf, px.ecdf]:
    """
    Returns the CDF graphs of the amount of messages per day for each group, the amount of active users per day for each group,
    and the amount of days-group that have messages after the threshold established with the min_number_of_messages.
    """
    df_cdf = pd.DataFrame(df_cdf_messages_active_users)

    # Messages CDF
    messages_distribution_fig = px.ecdf(df_cdf, x="num_messages", title="Figure 1")
    messages_distribution_fig.update_layout(yaxis_title="P(X <= x)", width=400, height=300)

    # Active users CDF
    active_users_distribution_fig = px.ecdf(df_cdf, x="active_users", title="Figure 3")
    active_users_distribution_fig.update_layout(yaxis_title="P(X <= x)", width=400, height=300)

    # Days distribution CDF
    dff_cdf = pd.DataFrame(df_cdf_days)
    days_distribution_fig = px.ecdf(dff_cdf, x="num_days_groups_with_messages", title="Figure 2")
    days_distribution_fig.update_layout(
        yaxis_title="P(X <= x)",
        xaxis_title=f"num_days_groups_with_msg (Threshold above {min_number_of_messages} messages)",
        width=400,
        height=300,
    )

    return messages_distribution_fig, active_users_distribution_fig, days_distribution_fig


def plot_groups_per_cluster(filtered_df) -> px.bar:
    """
    Creates a bar plot showing the proportion of groups per cluster on each day.
    The data is grouped by cluster.
    """

    # .size() counts the number of occurrence for the pair 'clusters' and 'date'
    # .reset_index() transforms the result in a new DataFrame with the columns 'clusters' and 'date'
    # and a final column with the n of occurrences.
    df_days_per_cluster = filtered_df.groupby(["cluster", "date"]).size().reset_index(name="count")
    df_cluster_total = (
        df_days_per_cluster.groupby("cluster")["count"].sum().reset_index(name="total_days")
    )
    df_days_per_cluster = df_days_per_cluster.merge(df_cluster_total, on="cluster")

    # Calculates the proportion of groups in each cluster per cluster
    df_days_per_cluster["proportion"] = (df_days_per_cluster["count"] / df_days_per_cluster["total_days"])

    # Format the date and cluster
    df_days_per_cluster["date"] = pd.to_datetime(df_days_per_cluster["date"])
    df_days_per_cluster["date"] = df_days_per_cluster["date"].dt.strftime("%d/%m")
    df_days_per_cluster["cluster"] = df_days_per_cluster["cluster"].astype(str)

    fig = px.bar(
        df_days_per_cluster,
        x="date",
        y="proportion",
        color="cluster",
        title="Proportion of groups per cluster of each day",
        barmode="group",
    )
    fig.update_layout( xaxis_title="Date", yaxis_title="Proportion of groups/cluster")

    return fig


def plot_groups_per_date(df) -> px.bar:
    """
    Creates a bar plot showing the proportion of groups per week on each cluster.
    The data is grouped by week.
    """
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.to_period("W")
    df["week"] = df["week"].astype(str)

    df_groups_per_week = df.groupby(["cluster", "week"]).size().reset_index(name="count_groups")
    df_total_groups_per_week = (
        df_groups_per_week.groupby("week")["count_groups"]
        .sum()
        .reset_index(name="total_groups_per_week")
    )
    df_groups_per_week = df_groups_per_week.merge(df_total_groups_per_week, on="week")

    # Calculates the propotion of groups in each cluster per week
    df_groups_per_week["proportion"] = (df_groups_per_week["count_groups"] / df_groups_per_week["total_groups_per_week"])

    # Format the cluster type
    df_groups_per_week["cluster"] = df_groups_per_week["cluster"].astype(str)

    fig = px.bar(
        df_groups_per_week,
        x="week",
        y="proportion",
        color="cluster",
        barmode="group",
        title="Proportion of groups per week of each cluster",
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Proportion of groups/week")

    return fig