import dash
import dash_bootstrap_components as dbc

from dashboard_app.views.main_layout import create_main_layout

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = create_main_layout(dash.page_registry, dash.page_container)

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
