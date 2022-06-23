"""MODULE FUNCTION ONLY"""
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd


def get_metadata_stations(path_file: Path) -> pd.DataFrame:
    """GET KEY /metadata/stations (stations information) AS DATAFRAME"""
    with pd.HDFStore(path_file, mode="r") as store:
        return store.get("/metadata/stations")


def get_metadata_file(path_file: Path) -> pd.Series:
    """GET KEY /metadata/file (file information) AS DATAFRAME"""
    with pd.HDFStore(path_file, mode="r") as store:
        return store.get("/metadata/file")


def read_metadata_csv(path_file: Path) -> pd.DataFrame:
    """READ METADATA RAINFALL & COMPLETENESS FILE/FOLDER"""
    from pyconfig import appConfig

    path_file = Path(path_file)

    if path_file.is_file():
        return pd.read_csv(
            path_file, index_col=0, parse_dates=["date_start", "date_end"]
        )
    if path_file.is_dir():
        filename = f"metadata_{path_file.parts[-1]}.csv"
        folder_metadata = Path(appConfig.DATASET.METADATA)
        path_file = folder_metadata / filename
        return pd.read_csv(
            path_file, index_col=0, parse_dates=["date_start", "date_end"]
        )


# FUNCTIONS
def replace_unmeasured_data(
    dataframe: pd.DataFrame, replace_vals: List[int] = None, replace_with=None
) -> None:
    """Replace 8888 and 9999 values to np.nan"""

    replace_vals = [8888, 9999] if replace_vals is None else replace_vals
    replace_with = np.nan if replace_with is None else replace_with

    for val in replace_vals:
        dataframe[dataframe == val] = replace_with


def validate_single_coordinate(single_coordinate: str, angle: str = "lat"):
    """Validate single coordinate on angle [lat]itude/[lon]itude"""
    from geopy.point import Point

    try:
        if angle == "lat":
            checkcoord = f"{single_coordinate},0"
        elif angle == "lon":
            checkcoord = f"0,{single_coordinate}"
        else:
            return False
        Point(checkcoord)
        return True
    except Exception as e:
        print(e)
        return False


def dataframe_calc_distance(
    point_coordinate: str, metadata_stations: pd.DataFrame = None
) -> pd.DataFrame:
    """ADD ADITIONAL COLUMN DISTANCE FROM POINT COORDINATE"""
    from geopy.point import Point
    from geopy import distance

    point_coord = Point(point_coordinate)

    metadata_stations["geopypoint"] = metadata_stations.apply(
        lambda row: Point(row.latitude, row.longitude), axis=1
    )
    metadata_stations["distance"] = metadata_stations.apply(
        lambda row: distance.geodesic(row.geopypoint, point_coord).km, axis=1
    )

    return metadata_stations.drop("geopypoint", axis=1)


def transform_to_dataframe(dashtable):
    return pd.DataFrame(dashtable)


def get_dataframe_from_folder(
    stat_ids: pd.Index, combined_metadata: pd.DataFrame, folder_dataset: Path
) -> pd.DataFrame:
    """RETRIEVE ALL DATA FROM IDS"""

    dataframe_collection = []
    for stat_id in stat_ids:
        filename = combined_metadata.loc[stat_id, "filename"]
        key = combined_metadata.loc[stat_id, "key"]
        path_file = folder_dataset / filename
        with pd.HDFStore(path_file, mode="r") as store:
            _dataframe = store.get(key)
            _dataframe.columns = [stat_id]
            dataframe_collection.append(_dataframe.rename_axis("date"))

    return pd.concat(dataframe_collection, axis=1)
