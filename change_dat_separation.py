import os
import pandas

# The .dat files created by Siril are delimited using spaces
# The plot_lightcurves requires a comma separated file
# This script goes over all the .dat files in the lightcurves directory and changes their delimiter from a space to a comma

TARGET_FILES = []

def get_target_files():
    for file in os.listdir("lightcurves/auto_aperture"):
        if file.endswith(".dat"):
            TARGET_FILES.append("lightcurves/auto_aperture/{}".format(file))

def change_delimiter(file):
    with open(file) as file_obj:
        file_df = pandas.read_csv(file_obj, sep=" ", header=None)
        # Remove header line
        file_df = file_df.drop(index=0, axis=0)
        file_df.to_csv(file+".csv", index=False, sep=",", header=False)

def main():
    get_target_files()
    for file in TARGET_FILES:
        change_delimiter(file)

if __name__ == "__main__":
    main()