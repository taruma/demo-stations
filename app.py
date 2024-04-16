"""MAIN APPLICATION"""

import dash
import dash_bootstrap_components as dbc
import plotly.io as pio
import pyfigure, pyfunc, pylayout, pylayoutfunc  # noqa: E401
from dash import Input, Output, State, html, dcc
from pyconfig import appConfig
from pathlib import Path
from pytemplate import fktemplate

pio.templates.default = fktemplate

# DASH APP CONFIG
APP_TITLE = appConfig.DASH_APP.APP_TITLE
UPDATE_TITLE = appConfig.DASH_APP.UPDATE_TITLE
DEBUG = appConfig.DASH_APP.DEBUG

# BOOTSTRAP THEME
THEME = appConfig.TEMPLATE.THEME
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)

# VARS
FOLDER_RAINFALL = Path(appConfig.DATASET.RAINFALL)
FOLDER_COMPLETENESS = Path(appConfig.DATASET.COMPLETENESS)

combined_metadata_rr = pyfunc.read_metadata_csv(FOLDER_RAINFALL)
combined_metadata_comp = pyfunc.read_metadata_csv(FOLDER_COMPLETENESS)

# MAIN APP
app = dash.Dash(
    APP_TITLE,
    external_stylesheets=[getattr(dbc.themes, THEME), DBC_CSS],
    title=APP_TITLE,
    update_title=UPDATE_TITLE,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    suppress_callback_exceptions=True,
)
server = app.server

app.layout = dbc.Container(
    [
        pylayout.HTML_TITLE,
        pylayout.HTML_INFO,
        pylayout.html_map(combined_metadata_rr),
        pylayout.HTML_ROW_INPUT,
        pylayout.HTML_ROW_BUTTON_NEAREST,
        pylayout.HTML_ROW_COORDINATE,
        pylayout.HTML_ROW_BUTTON_GRAPH_COMPLETENESS,
        pylayout.HTML_ROW_COMPLETENESS_RAINFALL,
        pylayout.html_row_rainfall_options(combined_metadata_rr),
        pylayout.HTML_ROW_GRAPH_RAINFALL,
        pylayout.HTML_ROW_BUTTON_DOWNLOAD,
        pylayout.HTML_CREATOR,
        pylayout.HTML_FOOTER,
    ],
    fluid=False,
    className="dbc",
)


@app.callback(
    (
        (Output("input-latitude", "valid"), Output("input-latitude", "invalid")),
        (Output("input-longitude", "valid"), Output("input-longitude", "invalid")),
        (
            Output("input-name-coordinate", "valid"),
            Output("input-name-coordinate", "invalid"),
        ),
    ),
    Input("button-coordinate-validity", "n_clicks"),
    State("input-latitude", "value"),
    State("input-longitude", "value"),
    State("input-name-coordinate", "value"),
    State("input-latitude", "valid"),
    State("input-latitude", "invalid"),
    State("input-longitude", "valid"),
    State("input-longitude", "invalid"),
    State("input-name-coordinate", "valid"),
    State("input-name-coordinate", "invalid"),
    prevent_initial_call=True,
)
def callback_valid_coordinate(
    _,
    latitude: str,
    longitude: str,
    name_coordinate: str,
    input_lat_valid: bool,
    input_lat_invalid: bool,
    input_lon_valid: bool,
    input_lon_invalid: bool,
    input_name_valid: bool,
    input_name_invalid: bool,
):
    """VALIDATION OF COORDINATES (LAT, LON, NAME)"""

    is_lat_valid = pyfunc.validate_single_coordinate(latitude, "lat")
    is_lon_valid = pyfunc.validate_single_coordinate(longitude, "lon")
    is_name_valid = (name_coordinate is not None) and (name_coordinate != "")

    input_lat_valid, input_lat_invalid = (True, None) if is_lat_valid else (None, True)
    input_lon_valid, input_lon_invalid = (True, None) if is_lon_valid else (None, True)
    input_name_valid, input_name_invalid = (
        (True, None) if is_name_valid else (None, True)
    )

    return (
        (input_lat_valid, input_lat_invalid),
        (input_lon_valid, input_lon_invalid),
        (input_name_valid, input_name_invalid),
    )


@app.callback(
    (
        Output("graph-coordinate", "children"),
        Output("table-coordinate", "children"),
        Output("button-graph-completeness", "disabled"),
    ),
    Input("input-latitude", "valid"),
    Input("input-longitude", "valid"),
    Input("input-name-coordinate", "valid"),
    State("input-latitude", "value"),
    State("input-longitude", "value"),
    State("input-name-coordinate", "value"),
    State("input-radius", "value"),
    State("input-n-stations", "value"),
    prevent_initial_call=True,
)
def callback_plot_coordinate(
    input_lat_valid: bool,
    input_lon_valid: bool,
    input_name_valid: bool,
    latitude: str,
    longitude: str,
    name_coordinate: str,
    radius_km: int,
    n_nearest: int,
):
    """CALLBACK PLOT BASED ON COORDINATE"""
    import math

    if input_lat_valid and input_lon_valid and input_name_valid:
        point_coordinate = f"{latitude},{longitude}"

        n_nearest = None if n_nearest < 1 else n_nearest
        radius_km = math.inf if radius_km < 1 else radius_km

        df_combined_with_distance = pyfunc.dataframe_calc_distance(
            point_coordinate, combined_metadata_rr
        )

        df_nearest_stations = (
            df_combined_with_distance.sort_values("distance")
            .round(3)
            .loc[df_combined_with_distance.distance < radius_km]
            .iloc[:n_nearest]
        )

        fig = pyfigure.generate_nearest_stations_map(
            point_coordinate, name_coordinate, df_nearest_stations
        )

        COLS_TABLE = "title distance station_name".split()
        COLS_NAME = "ID,DATASET,DISTANCE,STATION NAME".split(",")

        table = pylayoutfunc.dataframe_as_datatable(
            df_nearest_stations[COLS_TABLE],
            "table-nearest-stations",
            cols_name=COLS_NAME,
            page_size=12,
        )

        return (
            html.Div(pylayoutfunc.graph_map(fig, {"scrollZoom": True})),
            html.Div(table, className="border border-3 border-secondary"),
            False,
        )
    else:
        return (
            pylayoutfunc.graph_as_staticplot(
                pyfigure.generate_empty_figure(text="check your input", size=20, margin_all=50)
            ),
            pylayoutfunc.graph_as_staticplot(
                pyfigure.generate_empty_figure(text="check your input", size=20, margin_all=50)
            ),
            True,
        )


@app.callback(
    Output("graph-completeness-rainfall", "children"),
    Input("button-graph-completeness", "n_clicks"),
    State("table-nearest-stations", "derived_virtual_data"),
    State("table-nearest-stations", "derived_virtual_selected_rows"),
    prevent_initial_call=True,
)
def callback_graph_completeness(_, table_nearest_stations, selected_rows_index):
    """CALLBACK PLOT GRAPH COMPLETENESS"""
    df_nearest_stations = pyfunc.transform_to_dataframe(
        table_nearest_stations
    ).set_index("id")

    if selected_rows_index:
        stat_ids = df_nearest_stations.index[selected_rows_index]
    else:
        stat_ids = df_nearest_stations.index

    dataframe_comp = pyfunc.get_dataframe_from_folder(
        stat_ids, combined_metadata_comp, FOLDER_COMPLETENESS
    )

    fig_hm = pyfigure.figure_comp_heatmap(dataframe_comp, combined_metadata_comp)
    graph_hm = [pylayoutfunc.graph(fig_hm)]
    graph_bars = []
    bar_names = []
    hm_names = ["Heatmap"]

    for stat_id in stat_ids:
        _series = dataframe_comp[stat_id].dropna()
        _bar = pyfigure.figure_comp_bar_single(_series, combined_metadata_comp)
        _name = combined_metadata_comp.loc[stat_id, "station_name"]
        graph_bars.append(pylayoutfunc.graph(_bar))
        bar_names.append(f"{stat_id} - {_name}")

    graphs = graph_hm + graph_bars
    names = hm_names + bar_names
    tab_ids = ["heatmap"] + stat_ids.to_list()

    tabs = pylayoutfunc.create_tabcard_graph_comp(graphs, names, tab_ids)

    return tabs


@app.callback(
    Output("row-rangeslider-years", "children"),
    Output("button-graph-rainfall", "disabled"),
    Output("button-download-rainfall", "disabled"),
    Input("dropdown-stations", "value"),
)
def callback_update_years(stations):
    """CALLBACK GENERATE SLIDER BASED ON RANGE OF DATASET"""
    return (
        pylayoutfunc.create_rangeslider(stations, combined_metadata_rr),
        False if stations else True,
        True,
    )


@app.callback(
    Output("graph-rainfall-data", "children"),
    Input("button-graph-rainfall", "n_clicks"),
    State("rangeslider-years", "value"),
    State("dropdown-stations", "value"),
    State("switches-clean-data", "value"),
    prevent_initial_call=True,
)
def callback_plot_rainfall(_, years, stations, switch_clean_data):
    """CALLBACK PLOT RAINFALL STATIONS"""

    dataframe_rainfall = pyfunc.get_dataframe_from_folder(
        stations, combined_metadata_rr, FOLDER_RAINFALL
    )

    dataframe_sliced = dataframe_rainfall.loc[f"{years[0]}":f"{years[1]}"].copy()

    if "clean-data" in switch_clean_data:
        pyfunc.replace_unmeasured_data(dataframe_sliced)

    fig = pyfigure.figure_scatter(dataframe_sliced, combined_metadata_rr)

    return pylayoutfunc.graph(fig)


@app.callback(
    Output("download-metadata-stations", "data"),
    Input("button-download-metadata-stations", "n_clicks"),
    prevent_initial_call=True,
)
def callback_download_metadata(_):
    """CALLBACK DOWNLOAD METADATA ALL STATIONS"""
    return dcc.send_data_frame(combined_metadata_rr.to_csv, "metadata_stations.csv")


@app.callback(
    Output("download-rainfall", "data"),
    Input("button-download-rainfall", "n_clicks"),
    State("rangeslider-years", "value"),
    State("dropdown-stations", "value"),
    State("switches-clean-data", "value"),
    prevent_initial_call=True,
)
def callback_download_rainfall(_, years, stations, switch_clean_data):
    """CALLBACK DOWNLOAD RAINFALL DATA (SLICED)"""
    dataframe_rainfall = pyfunc.get_dataframe_from_folder(
        stations, combined_metadata_rr, FOLDER_RAINFALL
    )

    dataframe_sliced = dataframe_rainfall.loc[f"{years[0]}":f"{years[1]}"].copy()

    if "clean-data" in switch_clean_data:
        pyfunc.replace_unmeasured_data(dataframe_sliced)

    fn_years = f"{years[0]}_{years[1]}"
    fn_stations = "_".join(map(str, stations))

    return dcc.send_data_frame(
        dataframe_sliced.to_csv, f"rainfall_{fn_years}_{fn_stations}.csv"
    )


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
