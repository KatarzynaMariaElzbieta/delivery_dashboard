import dash
import dash_bootstrap_components as dbc
import folium
from dash import Input, Output, State, html, dcc

from dashboard_app.controler.geo_location import get_coordinates, get_address, coordinates_to_point
from dashboard_app.models.dictionaries import restaurant_types
from dashboard_app.models.models import Restaurants
from dashboard_app.models.orm_settings import Session

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader("Dodaj nową restaurację"),
                dbc.CardBody(
                    [
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Nazwa restauracji")),
                                        dbc.Col(dbc.Input(type="name", id="restaurant_name_input")),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Typ restauracji")),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                options=[
                                                    {"label": value, "value": key}
                                                    for key, value in restaurant_types.items()
                                                ],
                                                id="restaurant_type"
                                            )
                                        ),
                                    ]
                                ),
                                dbc.Row([dbc.Col(dbc.Label("Adres:")), dbc.Col(dbc.Input(id="address_input"))]),
                                html.Div(id="map"),
                                dbc.Col(
                                    dbc.Button("Submit", color="primary", id="restaurant_submit_btn"), width="auto"
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
        html.Div(id="restaurants_info"),
    ]
)

dash.register_page(
    __name__,
)


@dash.callback(
    [
        Output("map", "children"),
        Output("address_input", "n_blur_timestamp")
    ],
    Input("address_input", "n_blur_timestamp"),
    State("address_input", "value"))
def create_map(blur, address):
    if blur and address:
        coordinates = get_coordinates(address)
        m = folium.Map(location=coordinates, zoom_start=21)
        folium.Marker(coordinates).add_to(m)
        return (html.Div(html.Iframe(
            srcDoc=m.get_root().render(), style={"height": "30rem", "width": "100%"}
        )), 0)
    return "", None


@dash.callback(
    Output("restaurants_info", "children"),
    Input("restaurant_submit_btn", "n_clicks"),
    [
        State("restaurant_name_input", "value"),
        State("address_input", "value"),
        State("restaurant_type", "value")
    ],
)
def create_deliverer(n_clicks, restaurant_name, restaurant_address, restaurant_type):
    if n_clicks:
        latitude, longitude = get_coordinates(restaurant_address)
        restaurant = Restaurants()
        restaurant.name = restaurant_name
        restaurant.address = get_address(restaurant_address)
        restaurant.type_id = restaurant_type
        restaurant.location = coordinates_to_point(latitude, longitude)
        with Session() as session:
            session.add(restaurant)
            session.commit()
        return dbc.Alert(f'Restauracja {restaurant_name} została dodana do bazy.')
    return ''
