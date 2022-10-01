import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc

from dashboard_app.models.dictionaries import restaurant_types
from dashboard_app.models.models import Deliverers
from dashboard_app.models.orm_settings import Session

import geopy.geocoders
# import geocode

from geopy.geocoders import Nominatim

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader("Dodaj nową restaurację"),
                dbc.CardBody(
                    [
                        dbc.Form(
                            [
                                dbc.Row([
                                    dbc.Col(dbc.Label("Nazwa restauracji")),
                                    dbc.Col(dbc.Input(type="name", id="restaurants_name_input")),
                                ]),
                                dbc.Row([
                                    dbc.Col(dbc.Label("Typ restauracji")),
                                    dbc.Col(dcc.Dropdown(
                                        options=[{'label': value, 'value': key} for key, value in
                                                 restaurant_types.items()],
                                        multi=True
                                    ))]),
                                dbc.Row(
                                    [dbc.Col(dbc.Label('Adres:')),
                                     dbc.Col(dbc.Input(id='address_input'))]
                                ),
                                html.Div(id='map'),
                                dbc.Col(dbc.Button("Submit", color="primary", id="restaurants_submit_btn"),
                                        width="auto"),
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
    Output('map', 'children'),
    Input('address_input', 'value')
)
def create_map(address):
    if address:
        print(address)
        geopy.geocoders.options.default_user_agent = '1'
        geopy.geocoders.options.default_timeout = 7
        geolocator = Nominatim()
        print(geolocator.headers)
        {'User-Agent': 'my_app/1'}
        print(geolocator.timeout)
        coordinates = geolocator.geocode(query=address)
        print(coordinates.latitude)
        print(coordinates.longitude)
    return ''
# @dash.callback(
#     Output("info", "children"),
#     Input("deliverer_submit_btn", "n_clicks"),
#     State("deliverer_name_input", "value"),
# )
# def create_deliverer(n_clicks, deliverer_name):
#     if n_clicks:
#         deliver = Deliverers(name=deliverer_name)
#         with Session() as session:
#             session.add(deliver)
#             session.commit()
#         return dbc.Alert(f'Dostawca {deliverer_name} został dodany do bazy.')
#     return ''
