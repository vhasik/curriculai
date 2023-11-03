from dash import Dash, Input, Output, State, dcc, html, no_update
import dash_bootstrap_components as dbc
import pdfkit
import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import dotenv
from datetime import datetime, date
from dotenv import load_dotenv
import os
import openai


# Load the environment variables from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

swatch2 = ["gray", "red", "pink", "grape", "violet", "indigo", "blue", "lime", "yellow", "orange"]

colors = {
    "heading1": "orange",
    "heading2": "indigo",
    "heading3": "green",
    "text1": "#e64980",
    "text2": "#82c91e",
    "text3": "#7950f2",
}
# fmt: on


# def daily_activity(day):
#     day_id = day.lower()[:3]
#
#     return dmc.Grid([
#         # ACTIVITY
#         dmc.Col(html.Div([
#             dmc.Text(f"{day}: ", size="lg", color=colors["heading1"], underline=True), ],
#             style=heading_style), span=2),
#         dmc.Col(html.Div([
#             dmc.Textarea(id=f"{day_id}-activity", placeholder="Enter activity", autosize=True), ],
#             style=style), span=9),
#         dmc.Col(html.Div([
#             dmc.ActionIcon(
#                 DashIconify(icon="arcticons:openai-chatgpt"),
#                 size="lg", color=colors["heading1"], variant="filled", id=f"{day_id}-a-gpt", n_clicks=0), ],
#             style=style), span=1),
#
#         # SKILLS
#         dmc.Col(html.Div([
#             dmc.Text(f"Skills: ", size="lg", color=colors["heading2"], underline=False), ],
#             style=heading_style), span=2),
#         dmc.Col(html.Div([
#             dmc.Textarea(
#                 id=f"{day_id}-skills", placeholder="Enter skills", autosize=True),],
#             style=style), span=9),
#         dmc.Col(html.Div([
#             dmc.ActionIcon(
#                 DashIconify(icon="arcticons:openai-chatgpt"),
#                 size="lg", color=colors["heading2"], variant="filled", id=f"{day_id}-s-gpt", n_clicks=0), ],
#             style=style), span=1),
#
#         # SPACE
#         dmc.Col(html.Div([dmc.Space(h=10)]), span=12),
#     ],
#         gutter="xl",
#         justify="center",
#     )


def print_layout_for_day(day):
    day_id = day.lower()[:3]
    return dmc.Grid([
        dmc.Col(html.Div([
            dmc.Text(f"{day}:", size="lg", color=colors["heading1"], underline=True),
            html.Div(id=f"print-{day_id}-activity", style=style),
        ], style=style), span=4),
        dmc.Col(html.Div([
            dmc.Text(f"Skills:", size="lg", color=colors["heading2"], underline=True),
            html.Div(id=f"print-{day_id}-skills", style=style),
        ], style=style), span=4),
    ])


def use_gpt(instructions, prompt_text):
    # Load the prompt from the text file
    with open(instructions, 'r', encoding='utf-8') as file:
        instructions_text = file.read().strip()

    # # Load the prompt from the text file
    # with open(prompt, 'r', encoding='utf-8') as file:
    #     prompt_text = file.read().strip()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": instructions_text + prompt_text
            }
        ],
        temperature=0,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the response from OpenAI
    return response.choices[0].message['content']


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # Add more days if needed
# day_layouts = [daily_activity(day) for day in days]
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
            "fontSize": 30,
            "fontWeight": 900,
            "color": dmc.theme.DEFAULT_COLORS["indigo"][4],
            "margin": 0,
        },
    )
)


body = dmc.Tabs([
    dmc.TabsList([
        dmc.Tab("Curriculum", value="curriculum", icon=DashIconify(icon="tabler:book")),
        # dmc.Tab("Skills", value="skills", icon=DashIconify(icon="tabler:star")),
        dmc.Tab("Print", value="print", icon=DashIconify(icon="tabler:printer")),
        dmc.Tab("Email", value="email", icon=DashIconify(icon="tabler:mail")),
    ], position="center",),

    # CLASS INFO ====================================
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
                dmc.Textarea(
                    id="theme",
                    label="Theme:",
                    placeholder="What are you doing this week?",
                    autosize=True,
                ),],
                style=style), span=12),
                ],
            gutter="xl",
            justify="center",
        ),

        dmc.Space(h=40),

        dmc.Grid([
            dmc.Col(html.Div([
                dmc.Textarea(
                    id="activities",
                    label="Activities:",
                    placeholder="Enter list of activities like this:"
                                "\nMonday: Some activity."
                                "\nTuesday: Another activity."
                                "\nWednesday: Cool acitvity."
                                "\nThursday: Smart activity."
                                "\nFriday: Last activity.",
                    minRows=7,
                    autosize=True), ],
                style=style), span=12),
        ],),

        dmc.Space(h=20),

        dmc.Group(
            position="left",
            spacing="xl",
            children=[
                dmc.Button(
                    "Generate skills",
                    id="generate-skills",
                    color="indigo",
                    variant="filled",
                    size="sm",
                    leftIcon=DashIconify(icon="ri:openai-fill"),
                ),
                dmc.Loader(color="indigo", size="sm", variant="dots", id="loader-skills", style={"display": "none"}),
                html.Div([
                    dmc.Text("thinking, please wait..."),
                ],
                    id="loading-skills",
                    style={"display": "none"}  # Initially hidden
                )
            ]
        ),

        dmc.Grid([
            dmc.Col(html.Div([
                dmc.Textarea(
                    id="skills-text",
                    label="Skills:",
                    placeholder="Let ChatGPT generate skills for you! Click the button above.",
                    minRows=7,
                    autosize=True),
            ],
                style=style), span=12),
        ], gutter="xl", justify="center"),
    ],
        value="curriculum",
    ),
    dmc.TabsPanel("Settings tab content", value="skills"),

    # PRINT ====================================
    dmc.TabsPanel([
        dmc.Space(h=20),
        dmc.Grid([
            dmc.Col(html.Div([
                dmc.Text("Class Name:", size="lg", color=colors["heading1"], underline=True),
                html.Div(id="print-class-name", style=style),  # Add this line
            ], style={"fontFamily": "Roboto"}), span=4),
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

    # EMAIL ====================================
    dmc.TabsPanel([
        dmc.Space(h=20),

        dmc.Group([
            dmc.Button(
                "Generate email",
                id="generate-email",
                color="indigo",
                variant="filled",
                size="sm",
                fullWidth=False,
                leftIcon=DashIconify(icon="ri:openai-fill"),
            ),
            dmc.Loader(color="indigo", size="sm", variant="dots", id="loader-email", style={"display": "none"}),
            html.Div([
                dmc.Text("thinking, please wait..."),],
                id="loading-email",
                style={"display": "block"}  # Initially hidden
            ),],),
        dmc.Space(h=10),
        dmc.Grid([
            dmc.Col(html.Div([
                dmc.Textarea(
                    id=f"email-text",
                    placeholder="Let ChatGPT generate an email for you! Click the button above.",
                    minRows=25,
                    autosize=True), ],
                style={"textAlign": "left"}), span=12),
        ],),
    ], value="email"),
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
    [Output("loader-skills", "style"),
     Output("loading-skills", "style")],
    [Input("generate-skills", "n_clicks")]
)
def show_loader(n_clicks):
    if n_clicks:
        return {"display": "inline-block"}, {"display": "inline-block"}
    return {"display": "none"}, {"display": "none"}


@app.callback(
    Output("skills-text", "value"),  # Output for the loader's style
    [Input("generate-skills", "n_clicks"),
     Input("activities", "value")]
)
def generate_skills(n_clicks, activities_text):
    if n_clicks:
        generated_skills = use_gpt("prompt-skills.txt", activities_text)
        print(f"Activities text: {activities_text}")
        return generated_skills
    # If the button hasn't been clicked, don't change anything
    return no_update


@app.callback(
    [Output("loader-email", "style"),
     Output("loading-email", "style")],
    [Input("generate-email", "n_clicks")]
)
def show_loader(n_clicks):
    if n_clicks:
        return {"display": "inline-block"}, {"display": "inline-block"}
    return {"display": "none"}, {"display": "none"}


@app.callback(
    Output("email-text", "value"),  # Output for the loader's style
    [Input("generate-email", "n_clicks"),
     Input("activities", "value")]
)
def generate_email(n_clicks, activities_text):
    if n_clicks:
        generated_text = use_gpt("prompt-email.txt", activities_text)
        print(f"Activities text: {activities_text}")
        # Once the email is generated, hide the loader and the loading message
        return generated_text
    # If the button hasn't been clicked, don't change anything
    return no_update  # Keep both loader and text hidden


if __name__ == '__main__':
    app.run_server(debug=True)
