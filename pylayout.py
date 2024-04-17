"""
This module contains the layout components for a Dash application.

The layout includes HTML elements, Bootstrap components, 
    and functions to generate graphs and figures.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfigure
import pylayoutfunc
from pyconfig import appConfig
from pytemplate import mytemplate

pio.templates.default = mytemplate

HTML_TITLE = html.Div(
    [
        html.H1(
            appConfig.DASH_APP.APP_TITLE, className="float fw-bold mt-3 fs-1 fw-bold"
        ),
        html.Span("KAGGLE DATASET VERSION", className="fw-bold"),
        html.Br(),
        html.Span(
            html.A(
                [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
                href="https://github.com/taruma/demo-stations",
                target="_blank",
            ),
            className="text-muted",
        ),
        html.Br(),
    ],
    className="text-center",
)

# ALERT_INFO = dbc.Alert(
#     [
#         "Informasi aplikasi ini dapat dilihat di ",
#         html.A(
#             "GitHub README",
#             href="https://github.com/taruma/demo-stations#readme",
#             target="_blank",
#         ),
#         ".",
#     ],
#     color="info",
#     class_name="text-center fw-bold",
# )

ALERT_DATA = dbc.Alert(
    [
        "The displayed data comes from the KAGGLE DATASET.",
        html.Br(),
        "Information about the Kaggle dataset can be found ",
        html.A(
            "here",
            href="https://www.kaggle.com/datasets/greegtitan/indonesia-climate",
            target="_blank",
        ),
        ". With HDF5 data from ",
        html.A(
            "here",
            href="https://www.kaggle.com/code/tarumainfo/compile-rainfall-dataset-to-hdf5",
            target="_blank",
        ),
        ".",
        # html.Br(),
        # "With this modification, the metadata/rainfall download options are disabled.",
    ],
    color="warning",
    class_name="text-center fw-bold",
)

HTML_INFO = html.Div(
    # [ALERT_INFO, ALERT_DATA],
    [ALERT_DATA],
    className="mt-3",
)


def html_map(combined_metadata_rainfall: pd.DataFrame) -> html.Div:
    """Generate a map of rainfall stations."""
    return html.Div(
        [
            html.H2("Map of Rainfall Stations", className="text-center"),
            pylayoutfunc.graph_map(
                figure=pyfigure.generate_station_map_figure(combined_metadata_rainfall)
            ),
        ],
        className="mt-5",
    )


HTML_ROW_INPUT = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Coordinate Name / Nama Koordinat"),
                        dbc.Input(
                            id="input-name-coordinate",
                            placeholder="type coordinate name...",
                            type="text",
                            value="My Coordinate",
                        ),
                        dbc.FormText("Example: My Coordinate"),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        dbc.Label("Latitude / Lintang Derajat"),
                        dbc.Input(
                            id="input-latitude",
                            placeholder="type valid latitude coordinate...",
                            type="text",
                            value="""6°50'49.9"S""",
                        ),
                        dbc.FormText("""Example: 6°50'49.9"S"""),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        dbc.Label("Longitude / Bujur Derajat"),
                        dbc.Input(
                            id="input-longitude",
                            placeholder="type valid longitude coordinate...",
                            type="text",
                            value="107.525361",
                        ),
                        dbc.FormText("Example: 107.525361"),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        dbc.Label("Radius (km)"),
                        dbc.Input(
                            id="input-radius",
                            placeholder="0 - ♾️",
                            type="number",
                            value=100,
                        ),
                    ],
                    # width=2,
                ),
                dbc.Col(
                    [
                        dbc.Label("Total Stations"),
                        dbc.Input(
                            id="input-n-stations",
                            placeholder="0 - ♾️",
                            type="number",
                            value=5,
                        ),
                    ],
                    # width=2,
                ),
            ],
        )
    ],
    fluid=True,
    class_name="mt-4",
)

HTML_ROW_BUTTON_NEAREST = dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Button(
                "Find Nearest Stations",
                id="button-coordinate-validity",
                size="lg",
            ),
            width="auto",
        ),
        justify="end",
    ),
    class_name="my-3",
    fluid=True,
)

HTML_ROW_COORDINATE = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Map of Nearest Stations"),
                        dcc.Loading(
                            dcc.Graph(
                                figure=pyfigure.generate_empty_figure(margin_all=50),
                                config={"staticPlot": True},
                            ),
                            id="graph-coordinate",
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.H3("Table of Nearest Stations"),
                        dcc.Loading(
                            dcc.Graph(
                                figure=pyfigure.generate_empty_figure(margin_all=50),
                                config={"staticPlot": True},
                            ),
                            id="table-coordinate",
                        ),
                    ],
                    md=6,
                ),
            ],
            justify="start",
        )
    ],
    fluid=True,
)

HTML_ROW_BUTTON_GRAPH_COMPLETENESS = dbc.Container(
    dbc.Row(
        dbc.Col(
            dbc.Button(
                "Plot Rainfall Data Completeness",
                id="button-graph-completeness",
                color="warning",
                disabled=True,
                size="lg",
                # class_name="float-end",
            ),
            width="auto",
        ),
        justify="center",
    ),
    fluid=True,
    class_name="my-3",
)

HTML_ROW_COMPLETENESS_RAINFALL = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Rainfall Data Completeness"),
                dcc.Loading(
                    dcc.Graph(
                        figure=pyfigure.generate_empty_figure(margin_all=50),
                        config={"staticPlot": True},
                    ),
                    id="graph-completeness-rainfall",
                ),
            ],
            justify="start",
        )
    ],
    fluid=True,
    class_name="my-3",
)


def _options_stations(combined_metadata_rr: pd.DataFrame) -> list[dict]:
    return [
        {"label": f"{stat_id} - {series.station_name}", "value": stat_id}
        for stat_id, series in combined_metadata_rr.iterrows()
    ]


def html_row_rainfall_options(combined_metadata_rr: pd.DataFrame) -> dbc.Container:
    """Generate a row of rainfall data options."""
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Rainfall Data Options"),
                            dbc.Card(
                                [
                                    dbc.Label("Select Stations"),
                                    dcc.Dropdown(
                                        id="dropdown-stations",
                                        options=_options_stations(combined_metadata_rr),
                                        clearable=True,
                                        multi=True,
                                        value=[
                                            "kg_96783",
                                            "kg_96751",
                                            "kg_96791",
                                            "kg_96753",
                                            "kg_96747",
                                        ],
                                    ),
                                    html.Br(),
                                    dbc.Label("Select Years"),
                                    dcc.Loading(
                                        html.P(
                                            "Pick Stations First",
                                            className="text-muted text-center",
                                        ),
                                        id="row-rangeslider-years",
                                    ),
                                    html.Br(),
                                    dbc.Checklist(
                                        options=[
                                            {
                                                "label": "Clean Unmeasured Data (8888 & 9999)",
                                                "value": "clean-data",
                                            }
                                        ],
                                        value=["clean-data"],
                                        id="switches-clean-data",
                                        switch=True,
                                    ),
                                ],
                                body=True,
                            ),
                        ],
                    ),
                ],
                justify="start",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                "Plot Rainfall Data",
                                id="button-graph-rainfall",
                                color="danger",
                                size="lg",
                                disabled=True,
                            ),
                        ],
                        width="auto",
                    ),
                ],
                class_name="my-4",
                justify="center",
            ),
        ],
        fluid=True,
        class_name="my-3",
    )


HTML_ROW_GRAPH_RAINFALL = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Rainfall Data"),
                dcc.Loading(
                    dcc.Graph(
                        figure=pyfigure.generate_empty_figure(margin_all=50),
                        config={"staticPlot": True},
                    ),
                    id="graph-rainfall-data",
                ),
            ],
            justify="start",
        )
    ],
    fluid=True,
    class_name="my-3",
)

HTML_ROW_BUTTON_DOWNLOAD = dbc.Container(
    dbc.Row(
        dbc.Col(
            [
                dbc.Button(
                    "Download Metadata Stations",
                    id="button-download-metadata-stations",
                    size="lg",
                    color="info",
                    class_name="mx-3",
                    disabled=False,
                ),
                dcc.Download(id="download-metadata-stations"),
                dbc.Button(
                    "Download Rainfall Data",
                    id="button-download-rainfall",
                    size="lg",
                    disabled=True,
                    color="primary",
                    class_name="mx-3",
                ),
                dcc.Download(id="download-rainfall"),
            ],
            width="auto",
        ),
        justify="center",
    ),
    fluid=True,
    class_name="my-3",
)


_HTML_TROUBLESHOOTER = html.Div(id="row-troubleshooter")

HTML_CREATOR = html.P(
    [
        html.Hr(),
        "created by ",
        html.A("taruma", href="https://taruma.my.id"),
        # ". Sponsored by ",
        # html.A("FIAKO Engineering", href="https://fiako.engineering"),
    ],
    className="text-muted text-center mt-5 mb-1",
)


HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2024 ",
            html.A(
                "Taruma Sakti Megariansyah",
                href="https://dev.taruma.info",
                target="_blank",
            ),
            ".",
        ],
        className="text-center mb-3",
    ),
)
