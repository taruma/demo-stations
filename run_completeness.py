"""SCRIPT TO GENERATE COMPLETENESS TABLE"""

from pathlib import Path
import pandas as pd
import pyfunc
from pyconfig import appConfig

# pylint: disable=invalid-name


def flatten_multiindex_monthly(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten the multi-index of a DataFrame by
        renaming the index levels and converting it to a single-level index
        with a date range as the index values.

    Args:
        dataframe (pd.DataFrame): The DataFrame with a multi-index to be flattened.

    Returns:
        pd.DataFrame: The DataFrame with a flattened index, where the index values are a date range.

    """
    table = dataframe.copy()
    table.index = table.index.rename(["tahun", "bulan"])
    flat_index = table.index.to_flat_index()
    index_first, index_last = flat_index[0], flat_index[-1]
    date_start = f"{index_first[0]}-{index_first[1]}"
    date_end = f"{index_last[0]}-{index_last[1]}"
    dt_date_start = pd.to_datetime(date_start, format="%Y-%m")
    dt_date_end = pd.to_datetime(date_end, format="%Y-%m")
    index_date = pd.date_range(dt_date_start, dt_date_end, freq="MS")
    table = table.reset_index(drop=True)
    table.index = index_date
    return table


def calculate_monthly_completeness(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the monthly completeness of a given dataframe.

    Parameters:
    dataframe (pd.DataFrame): The input dataframe.

    Returns:
    pd.DataFrame: A dataframe containing the monthly completeness percentages.
    """
    table = dataframe.copy()
    monthly_count = table.groupby(by=[table.index.year, table.index.month]).count()
    monthly_len = (
        table.groupby(by=[table.index.year, table.index.month]).size().to_frame()
    )
    monthly_count = flatten_multiindex_monthly(monthly_count)
    monthly_percent = monthly_count.div(monthly_len.values, axis="columns")
    return monthly_percent.rename_axis("date")


def main():
    """Main function to generate the completeness table."""
    FOLDER_RAINFALL = Path(appConfig.DATASET.RAINFALL)
    FOLDER_COMPLETENESS = Path(appConfig.DATASET.COMPLETENESS)

    for file_rainfall in FOLDER_RAINFALL.glob("*.h5"):
        print(f"PROCESSING: {file_rainfall}")
        metadata_file = pyfunc.get_metadata_file(file_rainfall)
        metadata_stations = pyfunc.get_metadata_stations(file_rainfall)
        filename, title = metadata_file.filename, metadata_file.title

        FILENAME_COMP = f"comp_{filename}"
        PATH_COMP = FOLDER_COMPLETENESS / FILENAME_COMP
        _info_file = {"filename": FILENAME_COMP, "title": title}
        info_file = pd.Series(_info_file)

        with pd.HDFStore(PATH_COMP, mode="w", complevel=1) as store_comp, pd.HDFStore(
            file_rainfall, mode="r"
        ) as read_rr:
            print(f"WRITING: {PATH_COMP}")
            store_comp.put("/metadata/file", value=info_file)
            store_comp.put("/metadata/stations", value=metadata_stations)

            for stat_id in metadata_stations.index:
                key = metadata_stations.loc[stat_id, "key"]
                _df_rainfall = read_rr.get(key)
                pyfunc.replace_unmeasured_data(_df_rainfall)
                _df_completeness = calculate_monthly_completeness(_df_rainfall)
                _df_completeness = _df_completeness.round(3) * 100
                store_comp.put(key, value=_df_completeness)


if __name__ == "__main__":
    main()
