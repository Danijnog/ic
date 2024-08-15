import plotly.express as px

def plot_elbow_method(df):
    fig = px.line(df, x = 'num_clusters', y = 'wcss', title = "Elbow Method", width = 800, height = 600)

    return fig