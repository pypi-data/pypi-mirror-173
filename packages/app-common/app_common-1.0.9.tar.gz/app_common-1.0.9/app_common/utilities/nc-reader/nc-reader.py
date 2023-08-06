import os
import netCDF4 as nc
import pandas as pd

# Directory for raw .nc files
directory = "C:/Development/dal/app_common/utilities/nc-reader/"

# Where the new extracted csv files are going to live
if not os.path.exists("extracted"):
    os.mkdir("extracted")

directory_list = os.listdir(directory)
for file in directory_list:
    if file.endswith(".nc"):
        raw_data = {}
        path_of_file = os.path.join(directory, file)
        raw_df = nc.Dataset(path_of_file)
        for index, value in raw_df.variables.items():
            raw_data[index] = value[:]
        # Specific example of a variable that is longer than all the other variables in the table so we need to get rid of it
        del raw_data["castExtremeIndex"]
        df = pd.DataFrame(data=raw_data)
        file_name = file.strip(".nc")
        df.to_csv(os.path.join("extracted/", file_name + ".csv"))
