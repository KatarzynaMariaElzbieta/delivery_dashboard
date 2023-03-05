import datetime

import dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import html, Output, Input, dcc
from dash_iconify import DashIconify

from dashboard_app.models.dictionaries import restaurant_types
from dashboard_app.models.models import Orders, Restaurants
from dashboard_app.models.orm_settings import Session, engine
from sqlalchemy import func

dash.register_page(__name__, name="Główna", path="/")


def create_boxes():
    with Session() as session:
        avg_price = session.query(func.avg(Orders.costs_of_food + Orders.cost_of_delivery)).one()
        avg_price = str(round(avg_price[0], 2)) if avg_price[0] else 0

        avg_time = session.query(func.avg(Orders.delivery_datetime - Orders.order_create_date)).one()
        avg_time = str((avg_time[0].seconds % 3600) // 60.) if avg_time[0] else 0

        sum_price = session.query(func.sum(Orders.costs_of_food + Orders.cost_of_delivery)).filter(
            func.date_trunc('day', Orders.order_create_date).between(datetime.date.today().replace(day=1),
                                                                     datetime.date.today())).one()
        sum_price = str(round(sum_price[0], 2)) if sum_price[0] else 0

    return html.Div(
        [
            html.Div(
                [html.Span(["Średnia kwota zamówienia",
                            (
                                DashIconify(icon="ic:baseline-receipt-long", color='#fa572d',
                                            className="box-icon")
                            )]),
                 html.P(f"{avg_price} zł", id="avg_order_price")
                 ],
                id="avg_price_box",
                className="box orange-box"
            ),
            html.Div(
                [html.Span(["Średni czas oczekiwania",
                            (
                                DashIconify(icon="ic:baseline-receipt-long", color='#fa572d',
                                            className="box-icon")
                            )]),
                 html.P(f"{avg_time} min", id="avg_order_time")
                 ],
                id="avg_time_box",
                className="box blue-box"
            ),
            html.Div(
                [html.Span(["Suma bieżącego miesiąca",
                            (
                                DashIconify(icon="ic:baseline-receipt-long", color='#fa572d',
                                            className="box-icon")
                            )]),
                 html.P(f"{sum_price} zł", id="sum_price")
                 ],
                id="sum_price_box",
                className="box green-box"
            ),
            html.Div(
                [html.Span(["Średnia częstotliwość",
                            (
                                DashIconify(icon="ic:baseline-receipt-long", color='#fa572d',
                                            className="box-icon")
                            )]),
                 html.P("3 x msc", id="avg_period")
                 ],
                id="avg_period_box",
                className="box purple-box"
            ),
        ],
        id="top-bar",
        className="bar top-bar"
    )


def create_home_layout():
    return html.Div([
        create_boxes(),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Najczęściej zamawiane"),
                        dcc.DatePickerRange(id="food_type_range",
                                            start_date=datetime.date.today().replace(day=1),
                                            end_date=datetime.date.today()),
                        html.Div(id="food_type_plot"),
                    ],
                    className="plotbox"
                ),
                html.Div([
                    html.H3("Wydatki"),
                    dcc.DatePickerRange(id="costs_range",
                                        start_date=datetime.date.today().replace(day=1),
                                        end_date=datetime.date.today()),
                    html.Div(id="costs_plot"),

                ],
                    id="sum_price_plot", className="plotbox size2"),
                html.Div(id="delivery_time_plot"),
                html.Div(id="delivers_plot"),
                html.Div(id="period_plot"),
            ],
            className="view_context"
        )

    ])


layout = create_home_layout


@dash.callback(
    Output('food_type_plot', 'children'),
    Input('food_type_range', 'start_date'),
    Input('food_type_range', 'end_date')
)
def create_food_type_plot(start_date, end_date):
    with Session() as session:
        food_type_query = session.query(Restaurants.type_id, func.count(Orders.id)).join(Restaurants).filter(
            func.date_trunc('day', Orders.order_create_date).between(start_date, end_date)).group_by(
            Restaurants.type_id)
        food_type = pd.read_sql(food_type_query.statement, engine)
        food_type["type_id"] = food_type["type_id"].map(restaurant_types)
    fig = px.pie(food_type, names='type_id', values="count_1")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        font=dict(
            family='Montserrat',
            size=12,
            color="#9C9C9C"
        ),
    ))
    return dcc.Graph(figure=fig)


@dash.callback(
    Output('costs_plot', 'children'),
    Input('costs_range', 'start_date'),
    Input('costs_range', 'end_date')
)
def create_costs_plot(start_date, end_date):
    with Session() as session:
        costs_query = session.query(func.date_trunc('day', Orders.order_create_date).label('dzień'),
                                    func.sum(Orders.costs_of_food).label('Koszt jedzenia'),
                                    func.sum(Orders.cost_of_delivery).label('Koszt dostawy')
                                    ).filter(
            func.date_trunc('day', Orders.order_create_date).between(start_date, end_date)
        ).group_by(func.date_trunc('day', Orders.order_create_date))
        costs = pd.read_sql(costs_query.statement, engine)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=costs['dzień'], y=costs['Koszt jedzenia'] + costs['Koszt dostawy'],
                             mode='lines',
                             name='Koszt ogólny',
                             fill='tozeroy',
                             fillcolor='rgba(253, 121,179, 0.66)',
                             line_color='white', ))
    fig.add_trace(go.Scatter(x=costs['dzień'], y=costs['Koszt jedzenia'],
                             mode='lines',
                             name='Koszt jedzenia',
                             fill='tozeroy',
                             fillcolor='rgba(132, 64, 238, 0.7)',
                             line_color='violet', ))
    fig.add_trace(go.Scatter(x=costs['dzień'], y=costs['Koszt dostawy'],
                             mode='lines',
                             name='Koszt dostawy',
                             line_color='violet', ))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        font=dict(
            family='Montserrat',
            size=12,
            color="white"
        ),
    ),
        font_color='white',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    fig.update_xaxes(
        dtick=24 * 60 * 60 * 1000,
    )
    return dcc.Graph(figure=fig)
