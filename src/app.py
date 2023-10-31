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

heading_style = {
    "textAlign": "left"
}

# fmt: off
swatch1 = [
    "#25262b", "#868e96", "#fa5252", "#e64980", "#be4bdb", "#7950f2", "#4c6ef5",
    "#228be6", "#15aabf", "#12b886", "#40c057", "#82c91e", "#fab005", "#fd7e14"
]

swatch2 = [
    "gray",
    "red",
    "pink",
    "grape",
    "violet",
    "indigo",
    "blue",
    "lime",
    "yellow",
    "orange",
]

colors = {
    "heading1": "orange",
    "heading2": "indigo",
    "heading3": "green",
    "text1": "#e64980",
    "text2": "#82c91e",
    "text3": "#7950f2",
}
# fmt: on


def daily_activity(day):
    day_id = day.lower()[:3]

    return dmc.Grid([
        # ACTIVITY
        dmc.Col(html.Div([
            dmc.Text(f"{day}: ", size="lg", color=colors["heading1"], underline=True), ],
            style=heading_style), span=2),
        dmc.Col(html.Div([
            dmc.Textarea(id=f"{day_id}-activity", placeholder="Enter activity", autosize=True), ],
            style=style), span=9),
        dmc.Col(html.Div([
            dmc.ActionIcon(
                DashIconify(icon="arcticons:openai-chatgpt"),
                size="lg", color=colors["heading1"], variant="filled", id=f"{day_id}-a-gpt", n_clicks=0), ],
            style=style), span=1),

        # SKILLS
        dmc.Col(html.Div([
            dmc.Text(f"Skills: ", size="lg", color=colors["heading2"], underline=False), ],
            style=heading_style), span=2),
        dmc.Col(html.Div([
            dmc.Textarea(
                id=f"{day_id}-skills", placeholder="Enter skills", autosize=True),],
            style=style), span=9),
        dmc.Col(html.Div([
            dmc.ActionIcon(
                DashIconify(icon="arcticons:openai-chatgpt"),
                size="lg", color=colors["heading2"], variant="filled", id=f"{day_id}-s-gpt", n_clicks=0), ],
            style=style), span=1),

        # SPACE
        dmc.Col(html.Div([dmc.Space(h=10)]), span=12),
    ],
        gutter="xl",
        justify="center",
    )


def print_layout_for_day(day):
    day_id = day.lower()[:3]
    return dmc.Grid([
        dmc.Col(html.Div([
            dmc.Text(f"{day} Activity:", size="lg", color=colors["heading1"], underline=True),
            html.Div(id=f"print-{day_id}-activity", style=style),
        ], style=style), span=4),
        dmc.Col(html.Div([
            dmc.Text(f"{day} Skills:", size="lg", color=colors["heading1"], underline=True),
            html.Div(id=f"print-{day_id}-skills", style=style),
        ], style=style), span=4),
    ])


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Add more days if needed
day_layouts = [daily_activity(day) for day in days]
print_layouts = [print_layout_for_day(day) for day in days]


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
)


body = dmc.Tabs([
    dmc.TabsList([
        dmc.Tab("Curriculum", value="curriculum", icon=DashIconify(icon="tabler:book")),
        dmc.Tab("Skills", value="skills", icon=DashIconify(icon="tabler:star")),
        dmc.Tab("Print", value="print", icon=DashIconify(icon="tabler:printer")),
        dmc.Tab("Email", value="email", icon=DashIconify(icon="tabler:mail")),
    ], position="center",),

    # CLASS INFO
    dmc.TabsPanel([
        dmc.Space(h=20),

        dmc.Grid([
            dmc.Col(html.Div([
                dmc.TextInput(
                    id="class-name",
                    label="Class:",
                    value="Captains"
                ),
            ], style=style), span=4),
            dmc.Col(html.Div([
                dmc.TextInput(
                    id="teachers",
                    label="Teachers:",
                    value="Ms. Josselin & Mrs. Riece",
                ),
            ], style=style), span=4),
            dmc.Col(html.Div([
                dmc.DatePicker(
                    id="week-of",
                    label="Week of",
                    value=datetime.now().date(),
                    dropdownPosition="bottom-start",
                ),
            ], style=style), span=4),
            dmc.Col(html.Div([
                dmc.TextInput(
                    id="theme",
                    label="Theme:",
                    value="What are you doing this week?",
                ),],
                style=style), span=12),
                ],
            gutter="xl",
            justify="center",
        ),

        dmc.Space(h=40),

        *day_layouts,

        dmc.Space(h=40),

        dmc.Grid([
            dmc.Col(html.Div([
                dmc.Text(f"Day color: ", size="lg", color=colors["heading2"], underline=False), ],
                style=heading_style), span=2),
            dmc.Col(html.Div([
                dmc.ColorPicker(swatches=swatch2, swatchesPerRow=10, withPicker=False),
            ], style=style), span=10),
            dmc.Col(html.Div([
                dmc.Text(f"Skill color: ", size="lg", color=colors["heading2"], underline=False), ],
                style=heading_style), span=2),
            dmc.Col(html.Div([
                dmc.ColorPicker(swatches=swatch2, swatchesPerRow=10, withPicker=False),
            ], style=style), span=10),],
        ),

    ],
        value="curriculum",
    ),

    dmc.TabsPanel("Settings tab content", value="skills"),

    dmc.TabsPanel([
        dmc.Space(h=20),
        dmc.Grid([
            dmc.Col(html.Div([
                dmc.Text("Class Name:", size="lg", color=colors["heading1"], underline=True),
                html.Div(id="print-class-name", style=style),  # Add this line
            ], style=style), span=4),
            dmc.Col(html.Div([
                dmc.Text("Teachers:", size="lg", color=colors["heading1"], underline=True),
                html.Div(id="print-teachers", style=style),  # Add this line
            ], style=style), span=4),
            dmc.Col(html.Div([
                dmc.Text("Week Of:", size="lg", color=colors["heading1"], underline=True),
                html.Div(id="print-week-of", style=style),  # Add this line
            ], style=style), span=4),
            dmc.Col(html.Div([
                dmc.Text("Theme:", size="lg", color=colors["heading1"], underline=True),
                html.Div(id="print-theme", style=style),  # Add this line
            ], style=style), span=12),
        ]),
        dmc.Space(h=20),
        *print_layouts,  # Unpack the list of print layouts
        dmc.Space(h=20),
    ], value="print"),

    dmc.TabsPanel("Messages tab content", value="email"),

    ],
    color="red",
    orientation="horizontal",
    value="curriculum",
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


@app.callback(
    [Output("print-class-name", "children"),
     Output("print-teachers", "children"),
     Output("print-week-of", "children"),
     Output("print-theme", "children")],
    [Input("class-name", "value"),
     Input("teachers", "value"),
     Input("week-of", "date"),
     Input("theme", "value")]
)
def update_print_tab(class_name, teachers, week_of, theme):
    return class_name, teachers, week_of, theme


@app.callback(
    # Outputs for each day's activity and skills
    [Output(f"print-{day.lower()[:3]}-activity", "children") for day in days] +
    [Output(f"print-{day.lower()[:3]}-skills", "children") for day in days],
    # Inputs for each day's activity and skills
    [Input(f"{day.lower()[:3]}-activity", "value") for day in days] +
    [Input(f"{day.lower()[:3]}-skills", "value") for day in days]
)
def update_print_tab_for_activity_and_skills(*args):
    return args


if __name__ == '__main__':
    app.run_server(debug=True)
