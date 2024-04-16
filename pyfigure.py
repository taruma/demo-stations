"""MODULE FOR GENERATE FIGURE PLOTLY"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from geopy.point import Point
from pyconfig import appConfig

LOWEST_OPACITY, HIGHEST_OPACITY = 0.4, 1


def generate_watermark(subplot_number: int = 1, watermark_source: str = None) -> dict:
    """
    Generate a watermark dictionary for a subplot.

    Args:
        subplot_number (int, optional): The number of the subplot. Defaults to 1.
        watermark_source (str, optional): The source of the watermark.
            If not provided, it uses the default watermark source from the app configuration.

    Returns:
        dict: A dictionary containing the watermark properties.

    """
    watermark_source = watermark_source or appConfig.TEMPLATE.WATERMARK_SOURCE

    subplot_number = "" if subplot_number == 1 else subplot_number
    return {
        "source": watermark_source,
        "xref": f"x{subplot_number} domain",
        "yref": f"y{subplot_number} domain",
        "x": 0.5,
        "y": 0.5,
        "sizex": 0.5,
        "sizey": 0.5,
        "xanchor": "center",
        "yanchor": "middle",
        "name": "watermark",
        "layer": "below",
        "opacity": 0.2,
    }


def generate_empty_figure(
    text: str = "", size: int = 40, margin_all: int = 0, height: int = 450
) -> go.Figure:
    """
    Generate an empty figure with customizable text annotation.

    Parameters:
    - text (str): The text to be displayed as an annotation in the figure.
        Default is an empty string.
    - size (int): The font size of the text annotation. Default is 40.
    - margin_all (int): The margin size for all sides of the figure. Default is 0.
    - height (int): The height of the figure in pixels. Default is 450.

    Returns:
    - go.Figure: The generated empty figure with the specified properties.
    """

    data = [{"x": [], "y": []}]

    layout = go.Layout(
        title={"text": "", "x": 0.5},
        xaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        margin={"t": margin_all, "l": margin_all, "r": margin_all, "b": margin_all},
        annotations=[
            {
                "name": "text",
                "text": f"<i>{text}</i>",
                "opacity": 0.3,
                "font_size": size,
                "xref": "x domain",
                "yref": "y domain",
                "x": 0.5,
                "y": 0.05,
                "showarrow": False,
            }
        ],
        height=height,
    )

    return go.Figure(data, layout)


def generate_station_map_figure(station_locations: pd.DataFrame) -> go.Figure:
    """
    Generates a scattermapbox figure showing the locations of stations.

    Args:
        station_locations (pd.DataFrame): A DataFrame containing the station locations.

    Returns:
        go.Figure: The scattermapbox figure.

    Note:
        # The coordinate center of the map is the center of Indonesia.
        # Reference: https://qr.ae/psPeSb
        # Coordinate: 2°36'00.1"S 118°00'56.8"E (-2.600029, 118.015776)

    """

    data = []
    for dataset in station_locations["title"].unique():
        metadata_stations = station_locations.loc[station_locations["title"] == dataset]
        _scattermapbox = go.Scattermapbox(
            lat=metadata_stations.latitude,
            lon=metadata_stations.longitude,
            text=metadata_stations.station_name,
            customdata=metadata_stations.index,
            name=dataset,
            marker_size=12,
            marker_opacity=0.8,
        )
        data.append(_scattermapbox)

    layout = go.Layout(
        clickmode="event",
        title=None,
        margin={"t": 0, "l": 0, "b": 0, "r": 0},
        mapbox={
            "center": {
                "lat": -2.600029,
                "lon": 118.015776,
            },
        },
        dragmode=False,
        showlegend=True,
        legend_title="<b>Dataset</b>",
        legend={
            "yanchor": "top",
            "xanchor": "left",
            "x": 0.01,
            "y": 0.99,
            "bgcolor": "rgba(0,0,0,0)",
        },
        images=[
            {
                "source": appConfig.TEMPLATE.WATERMARK_SOURCE,
                "xref": "x domain",
                "yref": "y domain",
                "x": 0.01,
                "y": 0.02,
                "sizex": 0.2,
                "sizey": 0.2,
                "xanchor": "left",
                "yanchor": "bottom",
                "name": "watermark-fiako",
                "layer": "above",
                "opacity": 0.7,
            }
        ],
    )

    return go.Figure(data, layout)


def generate_nearest_stations_map(
    point_coordinate: str,
    name_coordinate: str,
    nearest_stations_df: pd.DataFrame,
) -> go.Figure:
    """
    Generate a scattermapbox figure showing the nearest stations to a given point.

    Args:
        point_coordinate (str): The coordinates of the point of interest.
        name_coordinate (str): The name of the point of interest.
        nearest_stations_df (pd.DataFrame):
            A DataFrame containing information about the nearest stations.

    Returns:
        go.Figure: A scattermapbox figure showing the nearest stations and the point of interest.
    """

    point_coordinate = Point(point_coordinate)

    # ref: https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    def normalize(data: pd.Series, lower: float, upper: float):
        return lower + (upper - lower) * (
            (data - data.min()) / (data.max() - data.min())
        )

    opacity_stations = (
        normalize(nearest_stations_df.distance, LOWEST_OPACITY, HIGHEST_OPACITY)[::-1]
        if len(nearest_stations_df) > 1
        else [HIGHEST_OPACITY]
    )

    data = [
        go.Scattermapbox(
            lat=nearest_stations_df.latitude,
            lon=nearest_stations_df.longitude,
            text=nearest_stations_df.station_name,
            textposition="bottom right",
            texttemplate="%{customdata[0]}<br>%{text}<br>%{customdata[1]:.3f} km",
            customdata=np.stack(
                [
                    nearest_stations_df.index,
                    nearest_stations_df.distance,
                ],
                axis=-1,
            ),
            hovertemplate="%{customdata[0]} - %{text}<br>(%{lat:.5f}, %{lon:.5f})<br>"
            "<b>%{customdata[1]:.3f} km</b><extra></extra>",
            name="Nearest Stations",
            marker_size=12,  # df_with_distance.distance,
            # marker_sizemin=5,
            # marker_sizeref=sizeref,
            marker_color="MidnightBlue",
            marker_opacity=opacity_stations,
            mode="markers+text",
        ),
        go.Scattermapbox(
            lat=[point_coordinate.latitude],
            lon=[point_coordinate.longitude],
            text=[name_coordinate],
            name=name_coordinate,
            textposition="bottom center",
            marker_size=15,
            marker_color="red",
            marker_opacity=1,
            mode="markers+text",
            hovertemplate="%{text}<br>(%{lat:.5f}, %{lon:.5f})<extra></extra>",
        ),
    ]

    layout = go.Layout(
        clickmode="event",
        title=None,
        margin={"t": 0, "l": 0, "b": 0, "r": 0},
        mapbox_center_lat=point_coordinate.latitude,
        mapbox_center_lon=point_coordinate.longitude,
        dragmode=False,
        showlegend=True,
        mapbox={"zoom": 9.5},
        images=[
            {
                "source": appConfig.TEMPLATE.WATERMARK_SOURCE,
                "xref": "x domain",
                "yref": "y domain",
                "x": 0.5,
                "y": 0.02,
                "sizex": 0.3,
                "sizey": 0.3,
                "xanchor": "center",
                "yanchor": "bottom",
                "name": "watermark-fiako",
                "layer": "above",
                "opacity": 0.6,
            }
        ],
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0.01,
            "bgcolor": "rgba(0,0,0,0)",
            "itemsizing": "constant",
        },
    )

    return go.Figure(data, layout)


def generate_completeness_heatmap(
    dataframe: pd.DataFrame, station_locations: pd.DataFrame = None
) -> go.Figure:
    """
    Generate a heatmap figure showing the completeness of data for all stations.

    Args:
        dataframe (pd.DataFrame): The input dataframe containing the completeness data.
        station_locations (pd.DataFrame, optional):
            The dataframe containing station locations information. Defaults to None.

    Returns:
        go.Figure: The generated heatmap figure.

    """

    table_percent = dataframe.T.iloc[::-1]
    table_percent_date = table_percent.copy()
    table_percent_date = table_percent_date.astype(str)
    table_percent_date[:] = table_percent_date.columns.strftime("%B %Y")

    if station_locations is not None:
        y_label = [
            f"{stat_id} - {station_locations.loc[stat_id, 'station_name']}"
            for stat_id in table_percent.index
        ]
    else:
        y_label = table_percent.index

    data = go.Heatmap(
        z=table_percent.to_numpy(),
        x=table_percent.columns,
        y=y_label,
        zmin=0,
        zmax=100,
        customdata=table_percent_date.to_numpy(),
        # colorbar_title_text='Percentage'
        hovertemplate="%{y}<br>%{customdata}<br><b>%{z}%</b><extra></extra>",
    )

    layout = go.Layout(
        xaxis_title_text="<b>Date</b>",
        xaxis_showspikes=True,
        yaxis_title_text="<b>Station ID</b>",
        # yaxis_tickangle=-90,
        yaxis_fixedrange=True,
        yaxis={"tickvals": y_label, "ticktext": table_percent.index},
        margin=dict(t=45, l=0, r=0, b=0),
        dragmode="zoom",
        height=max(450, 45 * len(table_percent)),
        showlegend=True,
    )

    return go.Figure(data, layout)


def generate_completeness_bar(
    series: pd.Series, station_locations: pd.DataFrame
) -> go.Figure:
    """
    Generate a bar chart showing the completeness of data for a single station.

    Args:
        series (pd.Series): The series containing the completeness data.
        station_locations (pd.DataFrame): The dataframe containing station locations.

    Returns:
        go.Figure: The generated bar chart figure.
    """

    border = 100 - series

    station_name = station_locations.loc[series.name, "station_name"]

    data = []
    _bar = go.Bar(
        x=series.index.strftime("%b %Y"),
        y=series,
        name=f"{station_name}",
        marker_line_width=0,
        hovertemplate=f"{series.name} - {station_name}<br>%{{x}}<br><b>%{{y}}%</b><extra></extra>",
    )
    data.append(_bar)
    _border = go.Bar(
        x=series.index.strftime("%b %Y"),
        y=border,
        name="<i>(border)</i>",
        hoverinfo="skip",
        marker_line_width=0,
        legendrank=500,
        visible="legendonly",
        marker_color="DarkGray",
    )
    data.append(_border)

    layout = go.Layout(
        barmode="stack",
        hovermode="x",
        bargap=0,
        dragmode="zoom",
        showlegend=True,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0.01,
        },
        xaxis_title="<b>Date</b>",
        yaxis={
            "fixedrange": True,
            "title": "<b>Percentage (%)</b>",
            "range": [0, 100],
        },
        margin={"t": 45, "l": 0, "r": 0, "b": 0},
    )

    return go.Figure(data, layout)


def figure_scatter(
    dataframe: pd.DataFrame, combined_metadata_rr: pd.DataFrame
) -> go.Figure:
    """FIGURE LINE/SCATTER STATIONS"""

    data = [
        go.Scatter(
            x=series.index,
            y=series,
            mode="lines",
            name=f"{stat_id} - {combined_metadata_rr.loc[stat_id, 'station_name']}",
        )
        for stat_id, series in dataframe.items()
    ]
    layout = go.Layout(
        hovermode="closest",
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>Rainfall (mm)</b>",
        legend_title="<b>Stations</b>",
        margin=dict(t=25, l=0, r=0, b=0),
    )

    return go.Figure(data, layout)
