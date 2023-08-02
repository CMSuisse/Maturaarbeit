# Load the .csv file into the program
# Allow the user to define limits on the different criteria
# Discard any entries that have insufficient information
# Display the entries that meet the user defined constraints
# Export the filtered entries as a new .csv file

import pandas as pd

# Define rough filter values
MIN_DECLINATION_VALUE_DEG = -40
# Representing RA values using base 10 is (of course) a sin, BUT determining if one is bigger than the other is still possible
MIN_RA_VALUE = 000000.0
MAX_RA_VALUE = 235959.9
MAX_PERIOD_VALUE = 5.0
MIN_BRIGHTNESS = 8.0


def main():
    with open("CATALOGF_edited_final.CSV", encoding="UTF-8-sig") as catalog:
        # Create a pandas dataframe object from the .csv file
        catalog_df = pd.read_csv(catalog)
        # Automatically exclude some entries before the user inputs are filtered
        catalog_df = exclude_insufficient_entries(catalog_df)
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

# Use the filter constraints defined at the start of the file to filter through the dataframe
def filter_dataframe(catalog_df):
    for index, row in catalog_df.iterrows():
        # Check every entry for declination, min_ra, max_ra, min_period, max_period and min_brightness
        # Connect the sign and value for the declination degree value to make comparing it easier
        row_declination_value_deg = int(row["DE-"] + str(row["DEd"]))
        # Convert the RA values of the row into one value that can be compared with the RA_VALUES defined at the top of the file
        row_ra_value = row["RAh"]*10000 + row["RAm"]*100 + row["RAs"]
        print(row_ra_value)
        if row_declination_value_deg < MIN_DECLINATION_VALUE_DEG:
            print("Removing index {} due to constraint declination".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
        # Check right ascension
        elif row_ra_value < MIN_RA_VALUE or row_ra_value > MAX_RA_VALUE:
            print("Removing index {} due to constraint right ascension".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0) 
        # Check period
        elif row["Period [d]"] > MAX_PERIOD_VALUE:
            print("Removing index {} due to constraint period".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
        # Check brightness
        elif row["MinI"] > MIN_BRIGHTNESS or row["MinII"] > MIN_BRIGHTNESS:
            print("Removing index {} due to constraint brightness".format(index))
            catalog_df = catalog_df.drop(index=index, axis=0)
    return catalog_df
        
if __name__ == "__main__":
    main()