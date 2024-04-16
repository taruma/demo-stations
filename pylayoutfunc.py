"""FUNCTION FOR GENERATE LAYOUT"""

from textwrap import wrap
from typing import List
from dash import dcc, dash_table, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from pytemplate import mytemplate


def graph_as_staticplot(figure: go.Figure, config: dict = None) -> dcc.Graph:
    """Return a dcc.Graph object with a static plot configuration."""
    config = {"staticPlot": True} if config is None else config
    return dcc.Graph(figure=figure, config=config)


def graph_map(
    figure: go.Figure, config: dict = None, border_width: int = 3
) -> dcc.Graph:
    """Return a dcc.Graph object with a map configuration."""
    config = {"scrollZoom": True} if config is None else config
    return dcc.Graph(
        figure=figure,
        config=config,
        className=f"border border-{border_width} border-primary",
    )


def graph(figure: go.Figure) -> dcc.Graph:
    """Return a dcc.Graph object with a default configuration."""
    return dcc.Graph(figure=figure)


def dataframe_as_datatable(
    dataframe: pd.DataFrame,
    idtable: str,
    cols_name: list = None,
    editable: bool = False,
    deletable: bool = False,
    renamable: bool = False,
    page_size: int = 10,
    index_is_date: bool = False,
):
    """
    Convert a pandas DataFrame into a Dash DataTable.

    Args:
        dataframe (pd.DataFrame): The pandas DataFrame to convert.
        idtable (str): The ID of the DataTable component.
        cols_name (list, optional): A list of column names to display in the DataTable.
            If None, all columns will be displayed. Defaults to None.
        editable (bool, optional): Whether the DataTable cells are editable.
            Defaults to False.
        deletable (bool, optional): Whether the DataTable columns are deletable.
            Defaults to False.
        renamable (bool, optional): Whether the DataTable columns are renamable.
            Defaults to False.
        page_size (int, optional): The number of rows to display per page.
            Defaults to 10.
        index_is_date (bool, optional): Whether the DataFrame index represents dates.
            If True, the index will be renamed to "date" and converted to date format.
            Defaults to False.

    Returns:
        dash_table.DataTable: The converted Dash DataTable component.
    """

    if index_is_date:
        dataframe = dataframe.rename_axis("date")
        dataframe = dataframe.reset_index()
        dataframe["date"] = dataframe["date"].dt.date
    else:
        dataframe = dataframe.reset_index()
    cols_name = dataframe.columns if cols_name is None else cols_name

    return dash_table.DataTable(
        id=idtable,
        columns=[
            {
                "name": f"{col_name}",
                "id": f"{col_id}",
                "deletable": deletable,
                "renamable": renamable,
            }
            for col_id, col_name in zip(dataframe.columns, cols_name)
        ],
        data=dataframe.to_dict("records"),
        page_size=page_size,
        editable=editable,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        row_selectable="multi",
        style_table={"overflowX": "auto", "overflowY": "auto", "height": "450px"},
        style_as_list_view=False,
        style_cell={"font-family": mytemplate.layout.font.family},
        style_data={"textAlign": "left"},
        style_header={"font-size": 20, "textAlign": "center", "font-weight": "bold"},
    )


def create_tabcard_graph_comp(
    graphs: List[dcc.Graph], tab_names: List, tab_ids: List, active_tab: str = None
):
    """
    Create a tabbed card graph component.

    Args:
        graphs (List[dcc.Graph]):
            A list of dcc.Graph objects representing the graphs to be displayed in each tab.
        tab_names (List): A list of tab names.
        tab_ids (List): A list of tab IDs.
        active_tab (str, optional): The ID of the active tab. Defaults to None.

    Returns:
        dbc.Tabs: A Dash Bootstrap Components Tabs component with the specified graphs and tabs.

    """

    def wrap_names(text, width=30):
        if len(wrap(text, width=width)) > 1:
            return wrap(text, width=width)[0] + "..."
        return text

    tab_names_wrapped = [wrap_names(name) for name in tab_names]

    tabs = []
    for each_graph, label, tab_id in zip(graphs, tab_names_wrapped, tab_ids):
        _tab = dbc.Tab(
            dbc.Card(dbc.CardBody([each_graph]), class_name="my-2"),
            label=label,
            tab_id=tab_id,
        )
        tabs.append(_tab)

    active_tab = tab_ids[0] if active_tab is None else active_tab

    return dbc.Tabs(tabs, active_tab=active_tab)


def create_rangeslider(stat_ids: List, combined_metadata_rainfall: pd.DataFrame):
    """
    Create a RangeSlider component based on the given station IDs and
        combined metadata rainfall DataFrame.

    Args:
        stat_ids (List): A list of station IDs.
        combined_metadata_rainfall (pd.DataFrame):
            A DataFrame containing combined metadata rainfall information.

    Returns:
        dcc.RangeSlider or html.P: A RangeSlider component if `stat_ids` is not empty,
            otherwise a paragraph element with a message.

    """
    if stat_ids:
        date_start = combined_metadata_rainfall.loc[stat_ids, "date_start"]
        date_end = combined_metadata_rainfall.loc[stat_ids, "date_end"]
        year_start = date_start.min().year
        year_end = date_end.max().year
        val_start = 2001 if year_start <= 2012 else year_start
        val_end = 2010 if year_end >= 2018 else year_end
        return dcc.RangeSlider(
            id="rangeslider-years",
            min=year_start,
            max=year_end,
            tooltip={"placement": "bottom", "always_visible": True},
            step=1,
            marks={year_start: f"{year_start}", year_end: f"{year_end}"},
            value=[val_start, val_end],
        )

    return html.P(
        "Pick Stations First",
        className="text-muted text-center",
    )
