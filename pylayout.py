import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfigure, pylayoutfunc, pyfunc  # noqa
from dash import html, dcc
from pyconfig import appConfig
from pytemplate import fktemplate

pio.templates.default = fktemplate

HTML_TITLE = html.Div(
    [
        html.H1(
            appConfig.DASH_APP.APP_TITLE, className="float fw-bold mt-3 fs-1 fw-bold"
        ),
        html.Span("DEMO/OPEN-SOURCE VERSION", className="fw-bold"),
        html.Br(),
        html.Span(
            [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
            className="text-muted",
        ),
        html.Br(),
    ],
    className="text-center",
)

ALERT_INFO = dbc.Alert(
    [
        "Informasi aplikasi ini dapat dilihat di ",
        html.A(
            "GitHub README",
            href="https://github.com/fiakoenjiniring/demo-stations#readme",
            target="_blank",
        ),
        ".",
    ],
    color="info",
    class_name="text-center fw-bold",
)

ALERT_DATA = dbc.Alert(
    [
        "Data yang ditampilkan berasal dari DATASET KAGGLE.",
        html.Br(),
        "Informasi dataset Kaggle bisa dilihat di ",
        html.A(
            "greegtitan/indonesia-climate",
            href="https://www.kaggle.com/datasets/greegtitan/indonesia-climate",
            target="_blank",
        ),
        ". Dengan data HDF5 dari ",
        html.A(
            "sini",
            href="https://www.kaggle.com/code/tarumainfo/compile-rainfall-dataset-to-hdf5",
            target="_blank",
        ),
        ".",
        html.Br(),
        "Dengan perubahan ini, maka opsi download metadata/rainfall dimatikan."
    ],
    color="warning",
    class_name="text-center fw-bold",
)

HTML_INFO = html.Div(
    [ALERT_INFO, ALERT_DATA],
    className="mt-3",
)


def html_map(combined_metadata_rainfall: pd.DataFrame) -> html.Div:
    return html.Div(
        [
            html.H2("Rainfall Stations", className="text-center"),
            pylayoutfunc.graph_map(
                figure=pyfigure.figure_map_all_stations(combined_metadata_rainfall)
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
                "Show Completeness Rainfall Data",
                id="button-graph-completeness",
                color="warning",
                disabled=True,
                # class_name="float-end",
            ),
            width="auto",
        ),
        justify="end",
    ),
    fluid=True,
    class_name="my-3",
)

HTML_ROW_COMPLETENESS_RAINFALL = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Completeness Rainfall Data"),
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
                                        value=[],
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
                                disabled=True,
                            ),
                        ],
                        width="auto",
                    ),
                ],
                class_name="my-4",
                justify="end",
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
                    disabled=True,
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
        ". Sponsored by ",
        html.A("FIAKO Engineering", href="https://fiako.engineering"),
    ],
    className="text-muted text-center mt-5 mb-1",
)


HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022 ",
            html.A(
                "PT. FIAKO Enjiniring Indonesia",
                href="https://fiako.engineering",
            ),
            ".",
        ],
        className="text-center",
    ),
)
