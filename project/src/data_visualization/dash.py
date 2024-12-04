import dash
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output


def create_graph_layout(id, figure, description="") -> html.Div:
    """
    Creates an HTML layout for a graph with a centered title.
    """
    return html.Div(
        [
            dcc.Graph(figure=figure, id=id, style={"width": "100%", "margin": "0px"}),
            html.P(
                children=description,
                style={
                    "width": "60%",
                    "text-align": "start",
                    "font-size": "14px",
                    "color": "#5559",
                    "margin-top": "8px",
                }
                if description
                else None,
            ),
        ],
        style={},
    )


def create_title_h1(children) -> html.H1:
    """
    Creates an H1 title with centered text.
    """
    return html.H1(children, style={"textAlign": "center"})


def create_title_h2(children) -> html.H2:
    """
    Creates an H2 title with centered text.
    """
    return html.H2(children, style={"textAlign": "center"})


def create_dropdown(id, options, placeholder) -> dcc.Dropdown:
    """
    Creates a Dropdown component with the provided options.
    """
    return dcc.Dropdown(
        options=sorted(options),
        id=id,
        placeholder=placeholder,
        multi=True,
        className="dash-dropdown",
    )


def create_flex_div(children) -> html.Div:
    """
    Creates a div with a flex display for organizing child elements.
    """
    return html.Div(children, style={"display": "flex", "marginBottom": "16px"})


def create_separator() -> html.Hr:
    """
    Creates a styled horizontal line (separator).
    """
    return html.Hr(style={"margin": "40px", "color": "#F1F1F1"})


def create_summary_display(summary, date) -> html.Div:
    """
    Creates an HTML component to display a summary and its date.
    """
    return html.Div(
        [html.P(f"Sumário: {summary}"), html.Label(f"Data: {date}")], style={"margin-left": "2vw"}
    )


def initialize_dash_app(scatter_plot_fig, scatter_plot_without_outliers_fig, messages_distribution_fig,
                        active_users_distribution_fig, days_distribution_fig, fig_groups_per_date,
                        trajectory_scatter_plot, df) -> dash.Dash:
    """
    Initializes the Dash application with the specified layout and figures.
    """
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            html.Link(
                href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap",
                rel="stylesheet",
            ),
            # Menu
            html.Div(
                [
                    html.H3(
                        "LoCuS - Laboratório de Computação Social",
                        style={"color": "#f1f1f1", "margin-left": "100px"},
                    ),
                    html.Div(
                        [
                            # Navigation links
                            dcc.Link(
                                "Metodologia",
                                href="/metodologia",
                                style={
                                    "color": "#f1f1f1",
                                    "margin-right": "20px",
                                    "font-size": "16px",
                                },
                            ),
                            dcc.Link(
                                "Nuvem de palavras",
                                href="/nuvem-palavras",
                                style={
                                    "color": "#f1f1f1",
                                    "margin-right": "20px",
                                    "font-size": "16px",
                                },
                            ),
                        ],
                        style={
                            "text-align": "center",
                            "margin-top": "16px",
                            "justify-content": "center",
                            "margin-right": "100px",
                        },
                    ),
                ],
                style={
                    "background-color": "rgba(29, 45, 68, 0.8)",
                    "padding": "10px",
                    "display": "flex",
                    "justify-content": "space-between",
                    "width": "100%",
                },
            ),

            create_title_h2("Estudo de Caso da evolução temporal de grupos do Telegram"),
            # Body page
            html.Div(
                [
                    html.H3("Metodologia"),
                    html.P(
                        [
                            "O presente projeto tem como objetivo realizar uma análise temporal da evolução de grupos do Telegram relacionados aos eventos que "
                            "culminaram nos ataques de 8 de janeiro de 2023, após o resultado das eleições no país.",
                            html.Br(),
                            "Sua metodologia é descrita de forma simples e simplificada, para um fácil entendimento e visualização dos dados e resultados.",
                        ]
                    ),
                    html.Ul(
                        [
                            html.Li(
                                [
                                    html.Strong(
                                        "Coleta e Preparação dos dados",
                                        style={"color": "rgba(29, 45, 68, 0.9)"},
                                    ),
                                    html.Br(),
                                    "A primeira etapa envolveu a coleta e a limpeza dos dados de mensagens de grupos do Telegram. " 
                                    "A partir disso, foi definido um TimeStamp para análise (25/09/2022 até 15/01/2023).",
                                ]
                            ),
                            html.Br(),
                            html.Li(
                                [
                                    html.Strong(
                                        "Análise Exploratória dos Dados (EDA)",
                                        style={"color": "rgba(29, 45, 68, 0.9)"},
                                    ),
                                    html.Br(),
                                    "Com os dados, foi realizada uma análise exploratória (EDA) para entender a natureza das mensagens e identificar padrões preliminares. "
                                    "Para isso, fizemos uso da Função de Distribuição Acumulada ",
                                    html.A(
                                        "(CDF)",
                                        href="https://support.minitab.com/pt-br/minitab/help-and-how-to/probability-distributions-random-data-and-resampling-analyses/supporting-topics/basics/using-the-cumulative-distribution-function-cdf/",
                                        title="Cumulative Distribution Function",
                                        target="_blank",
                                    ),
                                    ", método estatístico para analisarmos uma certa variável aleatória X.",
                                    html.Br(),
                                    html.Br(),
                                    "Abaixo, é calculado o CDF das seguintes variáveis: ",
                                ]
                            ),
                            html.Ul(
                                [
                                    html.Li("quantidade de mensagens por dia de cada grupo."),
                                    html.Li(
                                        "quantidade de dias por grupo que sobram para analisar depois de fazermos o corte com o mínimo número de mensagens que desejamos por dia grupo."
                                    ),
                                    html.Li("quantidade de usuários ativos por dia de cada grupo."),
                                ]
                            ),
                            # CDFs graphs
                            html.Div(
                                [
                                    create_graph_layout(
                                        "messages-distribution-fig",
                                        messages_distribution_fig,
                                        "Se selecionarmos aleatoriamente uma quantidade de mensagens, qual a probabilidade de que contenha até 25 mensagens? "
                                        "De acordo com a Figura 1, aproximadamente 53.4%. Ou seja, ao definirmos o limite mínimo da quantidade de mensagens por dia-grupo que queremos como 25, "
                                        "eliminamos cerca de 53.4% dos dias-grupo.",
                                    ),
                                    create_graph_layout(
                                        "days-distribution-fig",
                                        days_distribution_fig,
                                        "Do restante (46.6%) que possuem mais que 25 mensagens/dia-grupo, quantos dias por grupo que temos para analisar? "
                                        "Para responder essa pergunta, é feito o CDF da quantidade de dias/grupo com o mínimo número de mensagens definido como 25 nesse exemplo.",
                                    ),
                                    create_graph_layout(
                                        "active-users-distribution-fig",
                                        active_users_distribution_fig,
                                        "Se selecionarmos aleatoriamente uma quantidade de usuários ativos, qual a probabilidade de que contenha até 100 usuários? "
                                        "De acordo com a Figura 2, aproximadamente 96%.",
                                    ),
                                ],
                                style={
                                    "backgroundColor": "#f4f4f8",
                                    "padding": "40px",
                                    "border-radius": "8px",
                                    "box-shadow": "4px 0 10px rgba(0, 0, 0, 0.15)",
                                    "display": "flex",
                                    "justify-content": "space-around",
                                    "margin-bottom": "64px",
                                    "margin-top": "32px",
                                },
                            ),
                            html.Li(
                                [
                                    html.Strong(
                                        "Sumarização e Embedding",
                                        style={"color": "rgba(29, 45, 68, 0.9)"},
                                    ),
                                    html.Br(),
                                    "A partir da análise do CDF dos gráficos anteriores, foi definido o limite mínimo de mensagens por dia-grupo como 25, já que queremos analisar grupos que sejam mais dinâmicos e movimentados. "
                                    "Dessa forma, ficamos com cerca de 46.6% de dias-grupo em nossa base comparado ao valor inicial (Figura 1).",
                                    html.Br(),
                                    html.Br(),
                                    "Com isso, foi feita a sumarização das mensagens desses grupos através de uma LLM ",
                                    html.A(
                                        "(gpt-4o-mini)",
                                        href="https://platform.openai.com/docs/models/gpt-4o-mini",
                                        target="_blank",
                                    ),
                                    " e o Embedding com um modelo pré-treinado ",
                                    html.A(
                                        "(text-embedding-3-large)",
                                        href="https://platform.openai.com/docs/guides/embeddings#embedding-models",
                                        title="Embedding oferecido pela OpenAI.",
                                        target="_blank",
                                    ),
                                    " para uma representação dos sumários em um espaço de alta dimensão.",
                                    " A partir dessa representação, reduzimos a dimensionalidade através do ",
                                    html.A(
                                        "UMAP",
                                        href="https://pair-code.github.io/understanding-umap/?source=post_page-----e972cf607801--------------------------------",
                                        title="UMAP é uma técnica de Redução de Dimensionalidade para facilitar a visualização de datasets.",
                                        target="_blank",
                                    ),
                                    " para visualização em 2D de nosso Embedding.",
                                    " Para a clusterização, foi utilizado o",
                                    html.A(
                                        " K-Means",
                                        href="https://medium.com/cwi-software/entendendo-clusters-e-k-means-56b79352b452",
                                        title="K-Means é uma técnica de agrupamento (clusterização) de um conjunto de pontos em comum.",
                                        target="_blank",
                                    ),
                                    " para definir e rotular conjuntos de pontos semelhantes entre si, já que nossos dados não são rotulados.",
                                ]
                            ),
                            # Embedding graphs
                            html.Div(
                                [
                                    create_flex_div(
                                        [
                                            create_dropdown(
                                                "date-dropdown",
                                                df["date"].unique(),
                                                "Selecione uma data",
                                            ),
                                            create_dropdown(
                                                "id-dropdown", df["ID"].unique(), "Selecione um id"
                                            ),
                                        ]
                                    ),
                                    create_graph_layout("scatter-plot", scatter_plot_fig),
                                ],
                                style={
                                    "backgroundColor": "#f4f4f8",
                                    "padding": "40px",
                                    "borderRadius": "8px",
                                    "box-shadow": "4px 0 10px rgba(0, 0, 0, 0.15)",
                                    "margin-top": "32px",
                                },
                            ),
                            html.Div(id="output-div", children=[], style={"margin": "16px"}),
                        ]
                    ),
                ],
                style={"margin": "16px"},
            ),
            create_separator(),
            create_title_h2("Clusterização após remoção de outliers"),
            create_graph_layout(
                "scatter-plot-without-outliers-fig", scatter_plot_without_outliers_fig
            ),
            create_separator(),
            create_flex_div(
                [
                    create_graph_layout("trajectory-plot", trajectory_scatter_plot),
                    dcc.Graph(
                        id="days-per-cluster",
                        figure=fig_groups_per_date,
                        style={"margin-left": "6vw"},
                    ),
                ]
            ),
        ],
        style={"margin": "0px", "padding": "0px"},
    )

    # Defined style for the body and html to remove margin and extra paddings
    app.index_string = """
    <!DOCTYPE html>
    <html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
    </html>
    """
  
    return app


def register_dash_callbacks(app, df, new_df) -> None:
    """
    Registers the callbacks to update the scatter plot figures and display selected data summaries.
    """

    @app.callback(
        [
            Output(component_id="scatter-plot", component_property="figure"),
            Output(component_id="scatter-plot-without-outliers-fig", component_property="figure"),
        ],
        [
            Input(component_id="date-dropdown", component_property="value"),
            Input(component_id="id-dropdown", component_property="value"),
        ],
    )
    def update_figures(selected_dates, selected_ids):
        """
        Updates scatter plot figures based on selected dates and IDs.
        """
        filtered_df = df.copy()
        new_filtered_df = new_df.copy()

        # Ensure consistent coloring by sorting the DataFrame
        filtered_df = filtered_df.sort_values(by=["cluster", "ID", "date"])
        new_filtered_df = new_filtered_df.sort_values(by=["cluster", "ID", "date"])

        # Convert ID and cluster to string for filtering and consistent plotting
        new_filtered_df["ID"] = new_filtered_df["ID"].astype(str)
        new_filtered_df["cluster"] = new_filtered_df["cluster"].astype(str)

        if selected_dates:
            filtered_df = filtered_df[filtered_df["date"].isin(selected_dates)]
            new_filtered_df = new_filtered_df[new_filtered_df["date"].isin(selected_dates)]

        if selected_ids:
            filtered_df = filtered_df[filtered_df["ID"].isin(selected_ids)]
            new_filtered_df = new_filtered_df[new_filtered_df["ID"].isin(selected_ids)]

        fig = px.scatter(
            filtered_df,
            x="x",
            y="y",
            hover_name=filtered_df["label"].apply(
                lambda x: "<br>".join(x[i : i + 50] for i in range(0, len(x), 50)) # Break the line for the summary on a point in the scatter plot
            ),
            hover_data={"date", "ID"},
            color="cluster",
            title="Embedding Summary",
            width=800,
            height=600,
        )

        new_fig = px.scatter(
            new_filtered_df,
            x="x",
            y="y",
            hover_name=new_filtered_df["label"].apply(
                lambda x: "<br>".join(x[i : i + 50] for i in range(0, len(x), 50)) # Break the line for the summary on a point in the scatter plot
            ),
            hover_data={"date", "ID"},
            color="cluster",
            title="Embedding Summary",
            width=800,
            height=600,
        )

        return fig, new_fig

    @app.callback(
        Output(component_id="output-div", component_property="children"),
        Input(component_id="scatter-plot", component_property="selectedData"),
    )
    def display_selected_data(selected_data):
        """
        Display summaries of the points selecteds in the scatter plot.
        """
        if not selected_data:
            return "Faça uma seleção para visualizar o sumário e sua data."

        summaries_list = [
            create_summary_display(row["hovertext"].replace("<br>", ""), row["customdata"])
            for row in selected_data["points"]
        ]

        return summaries_list


def run_server(app):
    """
    Runs the Dash application server in debug mode.
    """
    app.run_server(debug=True)
