import pandas as pd
import plotly.express as px

def trajectory_plot(trajectory):
    trajectory_df = pd.DataFrame(trajectory)

    fig = px.scatter(trajectory_df, x = 'Media', y = 'Desvio Padrao', 
                    color = "ID", opacity = 0.8, 
                    title = 'Média e desvio padrão da trajetória de grupos na evolução do tempo',
                    width = 800, height = 600)

    return fig