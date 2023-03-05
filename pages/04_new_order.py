from datetime import datetime as dt

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from dashboard_app.models.dictionaries import (delivery_method,
                                               delivery_problems,
                                               food_problems)
from dashboard_app.models.models import Deliverers, Orders, Restaurants
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
                                                            id="order_deliverer_transport",
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
            html.Div(id='order_info'),
        ],
        id='new_order',
        className='content'
    )


layout = create_new_order_layout


@dash.callback(
    Output("order_info", "children"),
    Input("order_submit_btn", "n_clicks"),
    [
        State("order_start_time", "value"),
        State("order_stop_time", "value"),
        State("restaurant_name", "value"),
        State("order_cost", "value"),
        State("order_deliverer", "value"),
        State("order_deliverer_transport", "value"),
        State("delivery_cost", "value"),
        State("deliverer_problems_dropdown", "value"),
        State("food_problems_dropdown", "value"),
        State("order_description", "value"),
        State("order_rating", "value"),
    ],
)
def create_order(n_clicks,
                 order_start_time,
                 order_stop_time,
                 restaurant_name,
                 order_cost,
                 order_deliverer,
                 order_deliverer_transport,
                 delivery_cost,
                 deliverer_problems_dropdown,
                 food_problems_dropdown,
                 order_description,
                 order_rating):
    if n_clicks:
        order = Orders(order_create_date=order_start_time,
                       delivery_datetime=order_stop_time,
                       costs_of_food=order_cost,
                       cost_of_delivery=delivery_cost,
                       means_of_transport=order_deliverer_transport,
                       delivery_problems=list(deliverer_problems_dropdown),
                       food_problems=list(food_problems_dropdown),
                       description=order_description,
                       rating=order_rating
                       )

        with Session() as session:
            order.restaurant = session.query(Restaurants).filter(Restaurants.id == restaurant_name).one()
            order.deliverer = session.query(Deliverers).filter(Deliverers.id == order_deliverer).one()
            print(restaurant_name)
            print(order.restaurant.name)
            session.add(order)
            session.commit()
        return dbc.Alert(f"Zamówienie zostało dodane do bazy.")
    return ""
