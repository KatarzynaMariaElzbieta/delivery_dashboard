import dash_bootstrap_components as dbc
from dash import dcc, html

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]


def create_main_layout(page_registry, page_container):
    return html.Div(
        [
            html.Div(
                [
                    html.H1("Delivers dashboard", className="title"),
                    html.H2("Menu", className="menu"),
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(f"{page['name']}", href=page["relative_path"], className="link"),
                                className="btn-menu",
                            )
                            for page in page_registry.values()
                        ],
                    ),
                ],
                id="sidebar",
                className="sidebar",
            ),
            page_container,
        ],
        id="main",
        className="main",
    )
