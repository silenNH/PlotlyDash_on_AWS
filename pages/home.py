
from dash import  html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
#import plotly.express as px
import dash

dash.register_page(__name__, path="/")

layout = dbc.Container([
    
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="./assets/Tree.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("ATool", className="card-title"),
                            html.P(
                                "This tool is designed to optimize the usage of our given ressources. For any further information please contact Max Mustermann.",
                                className="card-text",
                            ),
                            dcc.Link("Go to ATool", href=dash.page_registry['pages.ATool']['path']),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
    )
        ]),
        dbc.Col([
            dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="./assets/Search.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(".....Next Tool", className="card-title"),
                            html.P(
                                "We are looking for new solutions to be published in our Analytics Platform",
                                className="card-text",
                            ),
                            #dcc.Link("Go to ATool", href=dash.page_registry['pages.ATool']['path']),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
    )
        ]),
    ]),
    

    

])
#dcc.Link("Got To", href=dash.page_registry['pages.ATool']['path']),



