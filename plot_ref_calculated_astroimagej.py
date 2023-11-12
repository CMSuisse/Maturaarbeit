from matplotlib import pyplot as plt
import numpy as np
from os import path
import pandas as pd

target_files = [
    "36PerseiB",
    "36PerseiV",
    "36PerseiR",
    "alfCepheiB",
    "alfCepheiV",
    "alfCepheiR",
    "alfLacertaeB",
    "alfLacertaeV",
    "alfLacertaeR",
    "etaPerseiB",
    "etaPerseiV",
    "etaPerseiR",
    "gamDraconisB",
    "gamDraconisV",
    "gamDraconisR",
    "tauDraconisB",
    "tauDraconisV",
    "tauDraconisR"
]

MOVING_AVERAGE_WINDOW_SIZE = 20

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

def plot_flux_ligthcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name):
    FLUX_MEDIAN = np.median(FLUX_PER_SECOND)
    # Plot the values as well as median and average values in a scatter plot with connecting lines
    fig, ax = plt.subplots()
    ax.set_title("Background subtracted flux for sequence {}".format(file_name))
    ax.set_xlabel("Julian Date -2400000")
    ax.set_ylabel("ADU/s")

    ax.plot(JULIAN_DATES, FLUX_PER_SECOND, "o")
    ax.axhline(FLUX_MEDIAN, linestyle = "--", color = "green")
    # Also plot the moving average to make the diagram more readable
    ax.invert_yaxis()
    # Safe the figure in the correct folder and with a figure size that doesn't save a potato quality image
    fig.savefig("../Figures/images_results/fluxastroimagej_{}.png".format(file_name), dpi=fig.get_dpi()*5)

def plot_magnitude_lightcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name):
    # For every value, apply the fitted formula to get from flux per second to the conversion coefficient
    COEFFICIENTS = list(map(lambda flux_value: 2150.1*flux_value**-1.485, FLUX_PER_SECOND))
    # Then use the coefficients to get from flux to mag
    MAGS = list(map(lambda flux_value, coeff: flux_value*coeff, FLUX_PER_SECOND, COEFFICIENTS))
    # Then plot the lightcurve
    MAGS_MEDIAN = np.median(MAGS)
    # Plot the values as well as median and average values in a scatter plot with connecting lines
    fig, ax = plt.subplots()
    ax.set_title("Magnitude LC for sequence {}".format(file_name))
    ax.set_xlabel("Julian Date -2400000")
    ax.set_ylabel("mag")

    ax.plot(JULIAN_DATES, MAGS, "o")
    ax.axhline(MAGS_MEDIAN, linestyle = "--", color = "green")
    ax.invert_yaxis()
    # Safe the figure in the correct folder and with a figure size that doesn't save a potato quality image
    fig.savefig("../Figures/images_results/magastroimagej_{}.png".format(file_name), dpi=fig.get_dpi()*5)
    return MAGS

def print_stats(MAGS):
    print("========== MAG stats ==========")
    print("Max value: {}mag".format(max(MAGS)))
    print("Min value: {}mag".format(min(MAGS)))

def main():
    # Let the user decide which file to plot
    for file_name in target_files:

        try:
            # Check if file exists
            assert path.isfile("lightcurves/ref_stars/astroimagej/{}.tbl".format(file_name))
            JULIAN_DATES, FLUX_PER_SECOND = calculate_flux(file_name)
            plot_flux_ligthcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name)
            MAGS = plot_magnitude_lightcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name)
            print_stats(MAGS)

            plt.show()
        
        except AssertionError as e:
            print("File doesn't exist.")

if __name__ == "__main__":
    main()