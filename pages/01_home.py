import dash
from dash import html

dash.register_page(__name__, name="Główna", path="/")

layout = html.Div("HOME")
