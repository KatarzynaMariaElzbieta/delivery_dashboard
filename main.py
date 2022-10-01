import dash
import dash_bootstrap_components as dbc

from dashboard_app.views.main_layout import create_main_layout

# leafled_css = {
#     'href': "https://unpkg.com/leaflet@1.9.1/dist/leaflet.css",
#     'rel': 'stylesheet',
#     'integrity': "sha256-sA+zWATbFveLLNqWO2gtiw3HL/lh1giY/Inf1BJ0z14=",
#     'crossorigin': ""
# }
# leaflet_js = {
#     'src': "https://unpkg.com/leaflet@1.9.1/dist/leaflet.js",
#     'integrity': "sha256-NDI0K41gVbWqfkkaHj15IzU7PtMoelkzyKp8TOaFQ3s=",
#     'crossorigin': ""
# }

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = create_main_layout(dash.page_registry, dash.page_container)

if __name__ == "__main__":
    app.run_server(debug=True)
