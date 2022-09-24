import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader("Dodaj nowego dostawcę"),
                dbc.CardBody(
                    [
                        dbc.FormFloating(
                            [
                                dbc.Input(type="Nazwa"),
                                dbc.Label("Nazwa dostawcy"),
                                dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),
                            ]
                        )
                    ],
                ),
            ]
        ),
    ]
)
