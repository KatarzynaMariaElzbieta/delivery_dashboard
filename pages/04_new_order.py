from datetime import datetime as dt

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from dashboard_app.models.dictionaries import (delivery_method,
                                               delivery_problems,
                                               food_problems)
from dashboard_app.models.models import Deliverers, Restaurants
from dashboard_app.models.orm_settings import Session

dash.register_page(__name__)


def create_new_order_layout():
    with Session() as session:
        deliverers = session.query(Deliverers.id, Deliverers.name).all()
        restaurants = session.query(Restaurants.id, Restaurants.name, Restaurants.address).all()
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Dodaj nowe zamówienie:", className='card card-header bg-primary text-white'),
                    dbc.CardBody(
                        [
                            dbc.Form(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(dbc.Label("Podaj czas złożenia zamówienia")),
                                            dbc.Col(dcc.Input(type="datetime-local", step="1", id="order_start_time",
                                                              value=dt.strftime(dt.now(), '%Y-%m-%dT%H:%M'))),
                                        ]
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(dbc.Label("Podaj czas dostarczenia zamówienia")),
                                            dbc.Col(dcc.Input(type="datetime-local", step="1", id="order_stop_time",
                                                              value=dt.strftime(dt.now(), '%Y-%m-%dT%H:%M'))),
                                        ]
                                    ),

                                    html.Div([
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Wybierz restaurację")),
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": f"{restaurant.name} ({restaurant.address})",
                                                             "value": restaurant.id}
                                                            for restaurant in restaurants
                                                        ],
                                                        id="restaurant_name",
                                                    )
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Podaj koszt zamówienia")),
                                                dbc.Col(dbc.Input(type="number", id="order_cost")),
                                            ]
                                        ),
                                    ], id="restaurant_details"),
                                    html.Div(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(dbc.Label("Wybierz dostawcę")),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[
                                                                {"label": deliverer.name,
                                                                 "value": deliverer.id}
                                                                for deliverer in deliverers
                                                            ],
                                                            id="order_deliverer",
                                                        )
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(dbc.Label("Wybierz sposób dostawy")),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            options=[
                                                                {"label": value, "value": key}
                                                                for key, value in delivery_method.items()
                                                            ],
                                                            id="order_deliverer",
                                                        )
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(dbc.Label("Podaj koszt dostawy")),
                                                    dbc.Col(dbc.Input(type="number", id="delivery_cost")),
                                                ]
                                            ),
                                        ], id="delivery_details"),
                                    html.Div([
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Komentarz do dostawy:")),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": value, "value": key}
                                                            for key, value in delivery_problems.items()
                                                        ],
                                                        id="deliverer_problems_dropdown",
                                                        multi=True
                                                    ),
                                                    dcc.Textarea(
                                                        id='delivery_problem_text',
                                                        value='',
                                                        style={'width': '100%', 'height': 300},
                                                    ),
                                                ]),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Kometarz do jedzenia:")),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        options=[
                                                            {"label": value, "value": key}
                                                            for key, value in food_problems.items()
                                                        ],
                                                        id="food_problems_dropdown",
                                                        multi=True,
                                                    ),
                                                    dcc.Textarea(
                                                        id="food_problem_text",
                                                        value='',
                                                        style={'width': '100%', 'height': 300},
                                                    ),
                                                ]),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Label("Komentarze do zamówienia:")),
                                                dbc.Col(dcc.Textarea(
                                                    id='order_description',
                                                    value='',
                                                    style={'width': '100%', 'height': 300},
                                                ),
                                                ),
                                            ]
                                        ),

                                    html.Div(
                                        [
                                            dbc.Label("Ocena zamówienia:"),
                                            dcc.Slider(0, 10, step=1, value=5, id="order_rating"),
                                        ]
                                    ),
                                    ], id="comments", style={"width": "-webkit-fill-available"}),
                                    dbc.Col(
                                        dbc.Button("Submit", color="primary", id="order_submit_btn"), width="auto"
                                    ),
                                ]
                            )
                        ],
                        className='card_body'
                    ),
                ],
            ),
        ],
        id='new_order',
        className='content'
    )


layout = create_new_order_layout()
