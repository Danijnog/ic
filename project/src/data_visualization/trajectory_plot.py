import pandas as pd
import plotly.express as px


def trajectory_plot(trajectory) -> px.scatter:
    """
    Creates a scatter plot visualizing the mean and standard deviation of group trajectories
    over time.
    """
    trajectory_df = pd.DataFrame(trajectory)

    fig = px.scatter(
        trajectory_df,
        x="Mean",
        y="Standard Deviation",
        color="ID",
        opacity=0.8,
        title="Mean and standard deviation of the trajectory of groups in the evolution of time",
        width=800,
        height=600,
    )

    return fig
