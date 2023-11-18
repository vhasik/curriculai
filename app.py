from dash import Dash, Input, Output, State, dcc, html, no_update, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
# from dash_extensions import Download
# from dash_extensions.snippets import send_bytes
from dash_iconify import DashIconify
import pandas as pd
import dotenv
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import os
import openai
import flask
import print_doc

# Load the environment variables from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

""" STYLES """

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

""" HELPER FUNCTIONS """


def use_gpt(instructions, prompt_text):
    # Load the prompt from the text file
    with open(instructions, 'r', encoding='utf-8') as file:
        instructions_text = file.read().strip()

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


def process_activities(input_text):
    days = []
    activities = []

    # Split the input text on newlines
    entries = input_text.split('\n')
    print(f"Entries: {entries}")

    for entry in entries:
        print(f"Entry: {entry}")
        # Split each entry on the colon
        parts = entry.split(':', 1)  # Split only on the first colon

        if len(parts) == 2:
            day, activity = parts
            days.append(day.strip())  # Remove any extra whitespace
            activities.append(activity.strip())

    return days, activities


def process_skills(input_text):
    skills = []

    # Split the input text on newlines
    entries = input_text.split('\n')

    for entry in entries:
        # Split each entry on the colon
        parts = entry.split(':', 1)  # Split only on the first colon

        if len(parts) == 2:
            skill = parts[1]
            skills.append(skill.strip())  # Remove any extra whitespace

    return skills


""" DASH APP """

app = Dash(
    __name__,
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
    title="CurriculA1",
    update_title="CurriculA1 | Loading...",
    assets_folder="assets",
    include_assets_files=True,
)
server = app.server

header = dmc.Center(
    html.Div(
        "CurriculA1",
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
        dmc.Tab("Email", value="email", icon=DashIconify(icon="tabler:mail")),
    ], position="center", ),

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
                ), ],
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
        ], ),

        dmc.Space(h=20),

        dmc.Group(
            position="left",
            spacing="xl",
            children=[
                dmc.Button(
                    "Generate skills",
                    id="generate-skills",
                    color="indigo", variant="filled", size="sm",
                    leftIcon=DashIconify(icon="ri:openai-fill"),
                ),
            ]
        ),
        dcc.Loading(
            id="loading-skills-text",
            type="circle",
            children=[
                dmc.Textarea(
                    id="skills-text",
                    label="Skills:",
                    style={"textAlign": "center"},
                    placeholder="Let ChatGPT generate skills for you! Click the button above.",
                    minRows=7,
                    autosize=True), ],
        ),

        dmc.Space(h=20),

        dmc.Button(
            "Create document",
            id="download-button",
            color="indigo", variant="filled", size="sm",
            leftIcon=DashIconify(icon="mdi:download"),
        ),
        # dcc.Download(id="download-file"),
        # dcc.Link("Download", id="download-button", href="", style={"display": "none"}, ),
        html.A("Download",
               id="download-file",
               href="",
               download="",
               style={"display": "none"}, )
    ],
        value="curriculum",
    ),

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
            ), ], ),
        dmc.Space(h=10),
        dcc.Loading(
            id="loading-email-text",
            type="circle",
            children=[
                dmc.Textarea(
                    id="email-text",
                    placeholder="Let ChatGPT generate an email for you! Click the button above.",
                    minRows=25,
                    autosize=True), ],
        )
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

"""APP LAYOUT"""
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


# @callback(
#     Output('download-file', 'style'),
#     Input('download-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def show_download_link(n_clicks):
#     if n_clicks:
#         return {'display': 'block'}  # Make the link visible
#     else:
#         raise PreventUpdate


@callback(
    Output("skills-text", "value"),  # Output for the loader's style
    Input("generate-skills", "n_clicks"),
    State("activities", "value")
)
def generate_skills(n_clicks, activities_text):
    if n_clicks:
        generated_skills = use_gpt("prompt-skills.txt", activities_text)
        print(f"Activities text: {activities_text}")
        return generated_skills
    # If the button hasn't been clicked, don't change anything
    return no_update


@callback(
    Output("email-text", "value"),  # Output for the loader's style
    Input("generate-email", "n_clicks"),
    State("activities", "value")
)
def generate_email(n_clicks, activities_text):
    if n_clicks:
        generated_text = use_gpt("prompt-email.txt", activities_text)
        print(f"Activities text: {activities_text}")
        # Once the email is generated, hide the loader and the loading message
        return generated_text
    # If the button hasn't been clicked, don't change anything
    return no_update  # Keep both loader and text hidden


"""DOWNLOAD DOCUMENT"""


@callback(
    Output('download-file', 'href'),
    Output('download-file', 'download'),
    Output('download-file', 'style'),
    Input('download-button', 'n_clicks'),
    State('class-name', 'value'),
    State('teachers', 'value'),
    State('week-of', 'value'),
    State('theme', 'value'),
    State('activities', 'value'),
    State('skills-text', 'value'),
    prevent_initial_call=True,
)
def update_href(n_clicks, class_name, teachers, week_of, theme, activities, skills):
    if n_clicks is None:
        raise PreventUpdate

    # Check if any of the inputs are None and set default values
    activities = activities if activities is not None else "Monday: No Activities"
    skills = skills if skills is not None else "Monday Skills: No Skills"

    days_list, activities_list = process_activities(activities)
    skills_list = process_skills(skills)

    # Call your script with the user input and return its path
    new_doc_path = print_doc.generate_doc(
        class_name, teachers, week_of,
        theme, days_list, activities_list, skills_list)

    # Use new_doc_path directly for the href attribute
    # file_url = f"\{new_doc_path}"
    file_name = os.path.basename(new_doc_path)
    # file_url = flask.url_for('static', filename=new_doc_path)
    file_url = f"/assets/{file_name}"

    print(f"File URL: {file_url}")
    print(f"File name: {file_name}")

    link_style = {'display': 'block'}

    return file_url, file_name, link_style


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
