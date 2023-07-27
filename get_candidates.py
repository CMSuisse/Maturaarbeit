# Load the .csv file into the program
# Allow the user to define limits on the different criteria
# Discard any entries that have insufficient information
# Display the entries that meet the user defined constraints
# Export the filtered entries as a new .csv file

import pandas as pd

# Define rough filter values
MIN_DECLINATION_VALUE_DEG = -40
MIN_RA_VALUE_H = 0
MAX_RA_VALUE_H = 23
MIN_PERIOD_VALUE = 0.0
MAX_PERIOD_VALUE = 5.0
MIN_BRIGHTNESS = 8.0


def main():
    with open("CATALOGF_edited_final.CSV", encoding="UTF-8-sig") as catalog:
        # Create a pandas dataframe object from the .csv file
        catalog_df = pd.read_csv(catalog)
        # Automatically exclude some entries before the user inputs are filtered
        catalog_df = exclude_insufficient_entries(catalog_df)
        catalog_df = exclude_permanent_invisible(catalog_df)
        catalog_df = filter_dataframe(catalog_df)
        catalog_df.to_csv('candidates.csv', index=False)

# Exclude entries that are missing period informations
def exclude_insufficient_entries(catalog_df):
    for index, row in catalog_df.iterrows():
        # O is the placeholder for an unknown period
        if row["Period [d]"] == 0:
            print("Removing index {} due to invalid period".format(index))
            # Remove this entry from the dataframe
            catalog_df = catalog_df.drop(index=index, axis=0)  
    return catalog_df

# Exclude entries with a declination of -40° or lower, as they won't ever be visible from Glarus
def exclude_permanent_invisible(catalog_df):
    for index, row in catalog_df.iterrows():
        if row["DE-"] == "-" and row["DEd"] >= 40:
            print("Removing index {} due to being permanently invisible".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
    return catalog_df

# Use the filter constraints defined at the start of the file to filter through the dataframe
def filter_dataframe(catalog_df):
    for index, row in catalog_df.iterrows():
        # Check every entry for declination, min_ra, max_ra, min_period, max_period and min_brightness
        # Connect the sign and value for the declination degree value to make comparing it easier
        row_declination_value_deg = int((row["DE-"] + str(row["DEd"])))
        if row_declination_value_deg < MIN_DECLINATION_VALUE_DEG:
            print("Removing index {} due to constraint declination".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
        # Check right ascension
        elif row["RAh"] < MIN_RA_VALUE_H or row["RAh"] > MAX_RA_VALUE_H:
            print("Removing index {} due to constraint right ascension".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
        # Check period
        elif row["Period [d]"] < MIN_PERIOD_VALUE or row["Period [d]"] > MAX_PERIOD_VALUE:
            print("Removing index {} due to constraint period".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
        # Check brightness
        elif row["MinI"] > MIN_BRIGHTNESS or row["MinII"] > MIN_BRIGHTNESS:
            print("Removing index {} due to constraint brightness".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
    return catalog_df
        
if __name__ == "__main__":
    main()