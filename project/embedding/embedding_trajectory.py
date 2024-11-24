import numpy as np
import pandas as pd


def get_df_for_trajectory(high_dim_embeddings, labels, date_labels) -> pd.DataFrame:
    """
    Creates a DataFrame from 10-dimensional embeddings, labels, and date information
    to calculate the trajectory of points over time.
    """
    df = pd.DataFrame(
        high_dim_embeddings, columns=[f"dim{i}" for i in range(high_dim_embeddings.shape[1])]
    )
    df["label"] = [groups["Sumário"] for groups in labels]
    df["ID"] = [groups["ID"] for groups in labels]
    df["date"] = date_labels

    # Transforms ID type to string to make the legend of the graph
    df["ID"] = df["ID"].astype(str)

    return df


def get_group_trajectory(group_id, df) -> list:
    """
    Calculates the trajectory of a specific group over time based on the Euclidean
    distance between its embeddings on consecutive days.
    """
    trajectory = []
    group_data = df.copy()

    # Filter the df to contain just the data of the chosen group
    group_data = group_data[group_data["ID"] == group_id].sort_values(by="date")

    for i in range(1, len(group_data)):
        # Euclidean distance of embeddings on consecutive days
        distance = np.linalg.norm(group_data.iloc[i, :10] - group_data.iloc[i - 1, :10])
        trajectory.append(distance)

    return trajectory


def get_all_groups_trajectories(df) -> list:
    """
    Calculates the trajectory for all groups in the DataFrame over time, computing
    the mean and standard deviation of each group's trajectory.
    """
    groups = df["ID"].unique()
    trajectories = []

    for group_id in groups:
        trajectory = get_group_trajectory(group_id, df)

        # Mean and standard deviation of the trajectory
        trajectory_mean = 0 if len(trajectory) == 0 else np.mean(trajectory)
        trajectory_std = (0 if len(trajectory) == 1 | 0 else np.std(trajectory))  # If we have just one trajectory (2 points), trajectory_std = 0
        trajectories.append(
            {
                "ID": group_id,
                "Trajectory": trajectory,
                "Mean": trajectory_mean,
                "Standard Deviation": trajectory_std,
            }
        )

    return trajectories
