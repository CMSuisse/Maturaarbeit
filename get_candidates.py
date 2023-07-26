# Load the .csv file into the program
# Allow the user to define limits on the different criteria
# Discard any entries that have insufficient information
# Display the entries that meet the user defined constraints
# Export the filtered entries as a new .csv file

import pandas as pd

def main():
    with open("CATALOGF_edited_final.CSV", encoding="UTF-8-sig") as catalog:
        reader = pd.read_csv(catalog)
        print(reader.line_num)
        #exclude_permanent_invisible(reader)

if __name__ == "__main__":
    main()