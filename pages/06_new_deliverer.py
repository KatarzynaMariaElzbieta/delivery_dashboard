import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from dashboard_app.models.models import Deliverers
from dashboard_app.models.orm_settings import Session

dash.register_page(
    __name__,
)

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader("Dodaj nowego dostawcę"),
                dbc.CardBody(
                    [
                        dbc.FormFloating(
                            [
                                dbc.Input(type="Nazwa", id="deliverer_name_input"),
                                dbc.Label("Nazwa dostawcy"),
                                dbc.Col(dbc.Button("Submit", color="primary", id="deliverer_submit_btn"), width="auto"),
                            ]
                        )
                    ],
                ),
            ]
        ),
        html.Div(id="info"),
    ]
)


@dash.callback(
    Output("info", "children"),
    Input("deliverer_submit_btn", "n_clicks"),
    State("deliverer_name_input", "value"),
)
def create_deliverer(n_clicks, deliverer_name):
    if n_clicks:
        deliver = Deliverers(name=deliverer_name)
        with Session() as session:
            session.add(deliver)
            session.commit()
        return dbc.Alert(f'Dostawca {deliverer_name} został dodany do bazy.')
    return ''
