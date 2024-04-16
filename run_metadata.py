"""Generate metadata for all datasets in the folder"""

from pathlib import Path
import pandas as pd
import pyfunc
from pyconfig import appConfig

# pylint: disable=invalid-name


def generate_metadata(folder: Path, folder_metadata: Path) -> None:
    """
    Generate metadata for files in a given folder and save it to a CSV file.

    Args:
        folder (Path): The folder containing the files
            for which metadata needs to be generated.
        folder_metadata (Path): The folder where the metadata CSV file will be saved.

    Returns:
        None
    """
    folder_name = folder.parts[-1]

    if folder_name.startswith("_"):
        print(f"SKIP: {folder}")
        return None

    metadata_all = []
    print(f"PROCESSING: {folder}")
    for path_file in folder.glob("*.h5"):
        metadata_file = pyfunc.get_metadata_file(path_file)
        metadata_stations = pyfunc.get_metadata_stations(path_file)

        for info, value in metadata_file.items():
            metadata_stations[info] = value

        metadata_stations["rel_folder"] = path_file.parent

        date_start = []
        date_end = []
        for stat_id in metadata_stations.index:
            key = metadata_stations.loc[stat_id, "key"]
            with pd.HDFStore(path_file, mode="r") as read_rr:
                _dataframe = read_rr.get(key)
                _date_start = _dataframe.index[0]
                _date_end = _dataframe.index[-1]
            date_start.append(_date_start)
            date_end.append(_date_end)

        metadata_stations["date_start"] = date_start
        metadata_stations["date_end"] = date_end

        metadata_all.append(metadata_stations)

    metadata_all = pd.concat(metadata_all, axis=0)

    all_metadata_filename = folder_metadata / f"metadata_{folder_name}.csv"

    print(f"WRITING: {all_metadata_filename}")
    metadata_all.to_csv(all_metadata_filename)


def main():
    """Main function to generate metadata for all datasets in the folder"""
    DATASET_CONFIGS = appConfig.DATASET
    FOLDER_METADATA = Path(appConfig.DATASET.METADATA)

    for key, folder_path in DATASET_CONFIGS.items():
        if key == "METADATA":
            print(f"SKIP: {key}")
        else:
            print(f"READING: {key} | FOLDER: {folder_path}")
            folder_path = Path(folder_path)
            generate_metadata(folder_path, FOLDER_METADATA)


if __name__ == "__main__":
    main()
