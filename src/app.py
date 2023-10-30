from dash import Dash, Input, Output, State, dcc, html, no_update
import dash_bootstrap_components as dbc
import pdfkit
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import dotenv
from datetime import datetime, date


style = {
    "border": f"0px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
}


app = Dash(
    __name__,
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
    title="CurriculAI",
    update_title="CurriculAI | Loading...",
    assets_folder="assets",
    include_assets_files=True,
)


header = dmc.Center(
    html.Div(
        "CurriculAI",
        style={
            "fontSize": 40,
            "fontWeight": 900,
            "color": dmc.theme.DEFAULT_COLORS["indigo"][4],
            "margin": 0,
        },
    )
    # html.A(
    #     dmc.Image(
    #         src="https://raw.githubusercontent.com/chatgpt/chart/9ff8b9b96f01a5ee7091ee5e69a2795381bf5031/docs/assets/chartgpt_logo.svg",
    #         alt="ChartGPT Logo",
    #         width=300,
    #         m=20,
    #         caption="Plot your data using GPT",
    #     ),
    #     href="https://github.com/chatgpt/chart",
    #     style={"textDecoration": "none"},
    # )
)


body = dmc.Tabs(
    children=[
        dmc.TabsList(
            [
                dmc.Tab("Class", value="class", icon=DashIconify(icon="tabler:chart-bar")),
                dmc.Tab("Curriculum", value="curriculum", icon=DashIconify(icon="tabler:book")),
                dmc.Tab("Skills", value="skills", icon=DashIconify(icon="tabler:star")),
                dmc.Tab("Print", value="print", icon=DashIconify(icon="tabler:printer")),
                dmc.Tab("Email", value="email", icon=DashIconify(icon="tabler:mail")),
            ],
            position="center"
        ),
        dmc.TabsPanel(
            value="class",
            children=[
                dmc.Grid(
                    children=[
                        dmc.Col(html.Div(
                            children=[
                                dmc.TextInput(
                                    id="class-name",
                                    label="Class:",
                                    value="Captains",
                                    style={"width": 200})
                                ],
                            style=style), span=4),
                        dmc.Col(html.Div(
                            children=[
                                dmc.TextInput(
                                    id="teachers",
                                    label="Teachers:",
                                    value="Ms. Josselin & Mrs. Riece",
                                    style={"width": 200},
                                ),
                                ],
                            style=style), span=4),
                        dmc.Col(html.Div(
                            children=[
                                dmc.DatePicker(
                                    id="week-of",
                                    label="Week of",
                                    value=datetime.now().date(),
                                    dropdownPosition="bottom-start",
                                    style={
                                        "width": 200
                                    },
                                ),
                                ],
                            style=style), span=4),
                    ],
                    gutter="xl",
                    justify="center",
                ),

                dmc.Grid(
                    children=[
                        dmc.Col(html.Div(
                            children=[
                                dmc.TextInput(
                                    id="theme",
                                    label="Theme:",
                                    value="What are you doing this week?",
                                    style={"width": 200},
                                ),
                                ],
                            style=style), span=12),
                        ],
                    gutter="xl",
                    justify="center",
                ),
            ],
        ),
        dmc.TabsPanel(
            "Messages tab content",
            value="curriculum"
        ),
        dmc.TabsPanel("Settings tab content", value="skills"),
    ],
    color="red",
    orientation="horizontal",
)


page = [
    dcc.Store(id="dataset-store", storage_type="local"),
    dmc.Container(
        [
            dmc.Stack(
                [
                    header,
                    body,
                ]
            ),
        ]
    ),
]


app.layout = dmc.MantineProvider(
    id="mantine-provider",
    theme={
        "fontFamily": "'Inter', sans-serif",
        "colorScheme": "light",
        "primaryColor": "dark",
        "defaultRadius": "md",
        "white": "#fff",
        "black": "#404040",
    },
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=page,
    inherit=True,
)


if __name__ == '__main__':
    app.run_server(debug=True)
