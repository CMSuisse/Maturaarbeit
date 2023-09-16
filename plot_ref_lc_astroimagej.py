from matplotlib import pyplot as plt
import numpy as np
from os import path
import pandas as pd

def calculate_flux(file_name):
    with open("lightcurves/ref_stars/astroimagej/{}.tbl".format(file_name)) as file:
        file_df = pd.read_table(file, delim_whitespace=True)
        
        # Extract the necessary informations from the file
        # The timestamp
        JULIAN_DATES = file_df["J.D.-2400000"].to_list()
        # The total ADU count over all the pixels in the aperture
        SOURCE_COUNTS = file_df["Source-Sky_T1"].to_list()
        # The amount of ADUs per pixel which is background
        BACKGROUND_PER_PIXEL_VALUES = file_df["Sky/Pixel_T1"].to_list()
        # The amount of pixels inside the aperture (useful to calculate total background counts)
        N_SKY_PIXELS = file_df["N_Sky_Pixels_T1"].to_list()
        # The exposure time used for the frames
        EXP_TIME = file_df["EXPTIME"].iloc[0]
        file.close()
    
    # Calculate the total background counts for each frame
    BACKGROUND_COUNTS = list(map(lambda pixel_value, num_pixels: pixel_value*num_pixels, BACKGROUND_PER_PIXEL_VALUES, N_SKY_PIXELS))
    # Then subtract the background value from every counts value
    SOURCE_COUNTS_BG_SUBTRACTED = list(map(lambda raw_value, bg_value: raw_value-bg_value, SOURCE_COUNTS, BACKGROUND_COUNTS))
    # Go through each source count and divide by the exposure time to get the flux in ADU/s
    FLUX_PER_SECOND = list(map(lambda count: count/EXP_TIME, SOURCE_COUNTS_BG_SUBTRACTED))
    return JULIAN_DATES, FLUX_PER_SECOND

def plot_ligthcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name):
    FLUX_MEDIAN = np.median(FLUX_PER_SECOND)
    # Plot the values as well as median and average values in a scatter plot with connecting lines
    fig, ax = plt.subplots()
    ax.set_title("Background subtracted flux for sequence {}".format(file_name))
    ax.set_xlabel("Julian Date -2400000")
    ax.set_ylabel("ADU/s")

    ax.plot(JULIAN_DATES, FLUX_PER_SECOND, "o")
    ax.axhline(FLUX_MEDIAN, linestyle = "--", color = "green")
    return FLUX_MEDIAN

def plot_adjusted_ligthcuve(JULIAN_DATES, FLUX_PER_SECOND, FLUX_MEDIAN, file_name, truemag):
    # Calculate what the coefficient should be to convert from flux values to magnitude values
    COEFF = truemag/FLUX_MEDIAN
    # And then apply the coefficient to every flux value
    MAGS = list(map(lambda flux: COEFF*flux, FLUX_PER_SECOND))

    # Plot the values again, this time only show the median
    fig, ax = plt.subplots()
    ax.set_title("Adjusted lightcurve for sequence {}".format(file_name))

    ax.set_xlabel("Julian Date -2400000")
    ax.set_ylabel("Apparent magnitude")

    ax.plot(JULIAN_DATES, MAGS, "o")
    ax.axhline(np.median(MAGS), linestyle = "--", color = "green")
    print("Conversion coefficient was {}".format(COEFF))
    print("FLUX_MEDIAN was {}".format(FLUX_MEDIAN))

def main():
    # Let the user decide which file to plot
    file_name = input("Specify the name of the file to be analyzed (path will be: lightcurves/ref_stars/astroimagej/[INPUT].tbl): ")
    # Allow the user to enter the actual magnitude of the star to calculate the conversion coefficient
    truemag = float(input("Magnitude the star actually has: "))

    try:
        # Check if file exists
        assert path.isfile("lightcurves/ref_stars/astroimagej/{}.tbl".format(file_name))
        JULIAN_DATES, FLUX_PER_SECOND = calculate_flux(file_name)
        FLUX_MEDIAN = plot_ligthcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name)
        plot_adjusted_ligthcuve(JULIAN_DATES, FLUX_PER_SECOND, FLUX_MEDIAN, file_name, truemag)

        plt.show()
    
    except AssertionError as e:
        print("File doesn't exist.")

if __name__ == "__main__":
    main()