import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([
    html.H1("curriculAI", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Edit Curriculum', children=[
            dbc.Row([
                dbc.Col(html.Div("Class name"), width=4),
                dbc.Col(html.Div("Teachers"), width=4),
                dbc.Col(html.Div("Week of"), width=4),
            ]),
            dbc.Row([
                dbc.Col(dbc.Input(value='Captains', type='text'), width=4),
                dbc.Col(dbc.Input(value='Ms. Josselyn & Mrs. Riece', type='text'), width=4),
                dbc.Col(dcc.DatePickerSingle(), width=4),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(html.Div("Theme", style={'textAlign': 'center'}), width=12),
            ]),
            dbc.Row([
                dbc.Col(dbc.Input(value='Trick or treat shenanigans', type='text', style={'width': '50%'}), style={'textAlign': 'center'}, width=12),
            ]),
            html.Br(),
            # Repeat this pattern for each day
            *[
                dbc.Row([
                    dbc.Col(html.Div(f'Day {i+1}'), width=12),
                ]),
                dbc.Row([
                    dbc.Col(html.Div("Activities"), width=6),
                    dbc.Col(dbc.Input(type='text'), width=5),
                    dbc.Col(dbc.Button("Get Help", color="primary"), width=1),
                ]),
                dbc.Row([
                    dbc.Col(html.Div("Skills"), width=6),
                    dbc.Col(dbc.Input(type='text'), width=5),
                    dbc.Col(dbc.Button("Get Help", color="primary"), width=1),
                ]),
                html.Hr(),
            ] for i in range(5)
        ]),
        dcc.Tab(label='Print Curriculum', children=[
            html.Div("coming soon")
        ]),
        dcc.Tab(label='Draft Email', children=[
            html.Div("coming soon")
        ]),
    ])
], style={'margin': 'auto', 'width': '80%'})


if __name__ == '__main__':
    app.run_server(debug=True)
