# import dash
# import dash_bootstrap_components as dbc
# from dash import Input, Output, State
#
# from dashboard_app.models.models import Deliverers
# from dashboard_app.models.orm_settings import Session
#
#
# @dash.callback(
#     Output('info', 'children'),
#     Input('deliverer_submit_btn', 'n_clicks'),
#     State('deliverer_name_input', 'value'),
# )
# def create_deliverer(n_clicks, deliverer_name):
#     if n_clicks:
#         deliver = Deliverers(name=deliverer_name)
#         Session.add(deliver)
#         Session.commit()
#         print(deliver.id)
#     return dbc.Alert(deliverer_name)
