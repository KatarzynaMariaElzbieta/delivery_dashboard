import dash
from dash import dcc, html


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
                        className='menu-container'
                    ),
                ],
                id="sidebar",
                className="bar side-bar",
            ),
            page_container,
        ],
        id="main",
        className="main",
    )