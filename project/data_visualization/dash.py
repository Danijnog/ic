import plotly.express as px
import pandas as pd
import dash

from dash import dcc, html
from dash.dependencies import Input, Output

def dash_app(fig, fig_hdbscan, trajectory_scatter_plot,  df) -> dash.Dash:
  """Inicializa o Dash App com o layout."""
  app = dash.Dash(__name__)

  app.layout = html.Div([
    html.Link(
      href = "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap",
      rel = "stylesheet"
    ),
    
    html.H2(
      "Embedding dos sumários de todos os grupos", 
      style = {'textAlign': 'center', 'fontFamily': 'Roboto'}
      ),
    
    # Div para organizar os dropdowns esteticamente
    html.Div([
      #Dropdown para selecionar a data
      dcc.Dropdown(
      options = sorted(df['date'].unique()),
      id = "date-dropdown",
      placeholder = "Selecione uma data",
      multi = True,
      style = {'width': '20vw'}
    ),

      #Dropdown para selecionar o ID
      dcc.Dropdown(
      options = sorted(df['ID'].unique()),
      id = "id-dropdown",
      placeholder = "Selecione um id",
      multi = True,
      style = {'width': '20vw', 'margin-left': '2vw'},
    )
    ], style = {'display': 'flex', 'margin': '16px'}),

    dcc.Graph(
      id = "scatter-plot",
      figure = fig,
    ),

    html.Div(
      id = "output-div", 
      children = [],
      style = {'fontFamily': 'Roboto', 'margin-left': '2vw'}
    ),

    html.Br(),

    html.Hr(style={'margin': '40px', 'color': '#F1F1F1'}),

    html.H2(
      "Comparação de Clusterização: K-Means x HDBScan",
      style = {'textAlign': 'center', 'fontFamily': 'Roboto'}
    ),

    html.Div([
      dcc.Graph(
        id = "scatter-plot-kmeans",
        figure = fig
      ),

      dcc.Graph(
        id = "scatter-plot-hdbscan",
        figure = fig_hdbscan
      )
    ], style = {'display': 'flex', 'justify-content': 'space-between'}),

    html.Br(),

    html.Hr(style={'margin': '40px', 'color': '#F1F1F1'}),

    html.H2(
      "Trajetória dos grupos na evolução dos dias",
      style = {'textAlign': 'center', 'fontFamily': 'Roboto'}
    ),

    dcc.Graph(
      id = "trajectory-plot",
      figure = trajectory_scatter_plot,
    )
  ])

  return app

def dash_callback(app, df) -> None:
  """Callbacks para atualizar o Scatter Plot e mostrar o sumário e a data com a seleção no gráfico."""
  @app.callback(
    Output(component_id = 'scatter-plot', component_property = 'figure'),
    [Input(component_id = 'date-dropdown', component_property = 'value'),
    Input(component_id = 'id-dropdown', component_property = 'value')]
)
  
  def update_figure(selected_dropdown_values, selected_ids):
    # Dropdown
    filtered_df = df.copy()
    if selected_dropdown_values:
      filtered_df = filtered_df[filtered_df['date'].isin(selected_dropdown_values)] # Filtrar o DataFrame para conter apenas as linhas onde foi selecionado a data no dropdown
    
    if selected_ids:
      filtered_df = filtered_df[filtered_df['ID'].isin(selected_ids)] # Filtrar o DataFrame para conter apenas as linhas onde foi selecionado o no dropdown

    fig = px.scatter(filtered_df, x = 'x', y = 'y',
                     hover_name = filtered_df['label']
                     .apply(lambda x: '<br>'
                     .join(x[i:i + 50] for i in range(0, len(x), 50))),
                     hover_data = {'date', 'ID'}, color = 'cluster', title = 'Embedding Summary')
    
    return fig
  
  @app.callback(
    # Callback para mostrar o sumário e a data com a seleção no gráfico
    Output(component_id = 'output-div', component_property = 'children'),
    Input(component_id = 'scatter-plot', component_property = 'selectedData'),
  )

  def display_selected_data(selected_data):
    summaries_list = []
    if selected_data is None: # Checar se a lista de pontos no dicionário 'selected_data' está vazia
      return "Faça uma seleção para visualizar o sumário e sua data."
    
    selected_points = selected_data['points']
    df_selected_points = pd.DataFrame(selected_points)

    for index, row in df_selected_points.iterrows():
      hover_text = row['hovertext']
      custom_data = row['customdata']
      hover_text = hover_text.replace("<br>", "") # Remover a quebra de linha que possui no texto.

      summaries_list.append(html.Div([
        html.P(f"Sumário: {hover_text}"),
        html.Label(f"Data: {custom_data}")
      ]))
    
    return summaries_list
      
def run_server(app):
  """Roda o servidor do Dash."""
  app.run_server(debug = True)