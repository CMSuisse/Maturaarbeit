from matplotlib import pyplot as plt
import numpy as np
from os import path
import pandas as pd

MOVING_AVERAGE_WINDOW_SIZE = 20

def adjust_t1_source_counts(SOURCE_COUNTS_T1, SOURCE_COUNTS_C2):
    ADJUSTED_SOURCE_COUNTS_T1 = [SOURCE_COUNTS_T1[0]]
    median_ref_count = np.median(SOURCE_COUNTS_C2)
    for i in range(len(SOURCE_COUNTS_T1)):
        # Correct the source counts by comparing the target star to the reference and assuming the reference star's brightness is constant
        ref_normalized = (SOURCE_COUNTS_C2[i])/(median_ref_count)
        ADJUSTED_SOURCE_COUNTS_T1.append(SOURCE_COUNTS_T1[i]*(1/ref_normalized))
    return ADJUSTED_SOURCE_COUNTS_T1
        

def calculate_flux(file_name):
    with open("lightcurves/binary_stars/{}.tbl".format(file_name)) as file:
        file_df = pd.read_table(file, delim_whitespace=True)
        
        # Extract the necessary informations from the file
        # The timestamp
        JULIAN_DATES = file_df["J.D.-2400000"].to_list()
        # The total ADU count over all the pixels in the aperture of the target and the reference
        SOURCE_COUNTS_T1 = file_df["Source-Sky_T1"].to_list()
        SOURCE_COUNTS_C2 = file_df["Source-Sky_C2"].to_list()
        SOURCE_COUNTS = adjust_t1_source_counts(SOURCE_COUNTS_T1, SOURCE_COUNTS_C2)
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
    SOURCE_COUNTS_BG_SUBTRACTED_RAW = list(map(lambda raw_value, bg_value: raw_value-bg_value, SOURCE_COUNTS_T1, BACKGROUND_COUNTS))
    # Go through each source count and divide by the exposure time to get the flux in ADU/s
    FLUX_PER_SECOND = list(map(lambda count: count/EXP_TIME, SOURCE_COUNTS_BG_SUBTRACTED))
    FLUX_PER_SECOND_RAW = list(map(lambda count: count/EXP_TIME, SOURCE_COUNTS_BG_SUBTRACTED_RAW))
    return JULIAN_DATES, FLUX_PER_SECOND, FLUX_PER_SECOND_RAW

def plot_magnitude_lightcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name):
    # Then use the coefficients to get from flux to mag
    MAGS = list(map(lambda flux_value: -2.5*np.log10(flux_value/16468819), FLUX_PER_SECOND))
    # Then plot the lightcurve
    fig, ax = plt.subplots()
    ax.set_title("Magnitude LC for sequence {}".format(file_name))
    ax.set_xlabel("Julian Date -2400000")
    ax.set_ylabel("mag")
    ax.ticklabel_format(useOffset=False)
    ax.locator_params(axis="x", tight=True, nbins=6)

    ax.plot(JULIAN_DATES, MAGS, "o")
    # Also plot the moving average to make the diagram more readable
    SMOOTHED_MAGS = moving_average(MAGS)
    print(np.median(SMOOTHED_MAGS))
    ax.plot(JULIAN_DATES, SMOOTHED_MAGS)
    ax.invert_yaxis()
    # Safe the figure in the correct folder and with a figure size that doesn't save a potato quality image
    fig.savefig("../Figures/images_results/magastroimagej_{}.png".format(file_name), dpi=fig.get_dpi()*5)
    return MAGS, SMOOTHED_MAGS

def plot_raw_magnitude_lightcurve(JULIAN_DATES, FLUX_PER_SECOND_RAW, file_name):
    # Then use the coefficients to get from flux to mag
    MAGS = list(map(lambda flux_value: -2.5*np.log10(flux_value/16468819), FLUX_PER_SECOND_RAW))

    # Then plot the lightcurve
    fig, ax = plt.subplots()
    ax.set_title("Raw magnitude LC for sequence {}".format(file_name))
    ax.set_xlabel("Julian Date -2400000")
    ax.set_ylabel("mag")
    ax.ticklabel_format(useOffset=False)
    ax.locator_params(axis="x", tight=True, nbins=6)

    ax.plot(JULIAN_DATES, MAGS, "o")
    # Also plot the moving average to make the diagram more readable
    SMOOTHED_MAGS = moving_average(MAGS)
    ax.plot(JULIAN_DATES, SMOOTHED_MAGS)
    ax.invert_yaxis()
    # Safe the figure in the correct folder and with a figure size that doesn't save a potato quality image
    fig.savefig("../Figures/images_results/magastroimagej_{}.png".format(file_name), dpi=fig.get_dpi()*5)


def print_stats(MAGS, SMOOTHED_MAGS):
    DEVS_FROM_MEAN = MAGS - SMOOTHED_MAGS
    print("========== MAG stats ==========")
    print("Max value: {}mag".format(max(MAGS)))
    print("Min value: {}mag".format(min(MAGS)))
    print("========== SMOOTHED_MAG stats ==========")
    print("Max value: {}mag".format(max(SMOOTHED_MAGS)))
    print("Min value: {}mag".format(min(SMOOTHED_MAGS)))
    print("========== DEVIATION STATS ==========")
    print("Average deviation: {}mag".format(np.average(DEVS_FROM_MEAN)))
    print("Standard deviation: {}mag".format(np.std(DEVS_FROM_MEAN)))

def moving_average(array):
    window = np.ones(int(MOVING_AVERAGE_WINDOW_SIZE))/float(MOVING_AVERAGE_WINDOW_SIZE)
    processed = np.convolve(array, window, 'same')
    # Remove the first few and last few elements of the array as for these values the convolution windows isn't filled
    processed = processed[MOVING_AVERAGE_WINDOW_SIZE//2:len(processed)-MOVING_AVERAGE_WINDOW_SIZE//2]
    # Fill up the list again
    for _ in range(MOVING_AVERAGE_WINDOW_SIZE//2):
        processed = np.insert(processed, 0, processed[0])
        processed = np.insert(processed, len(processed)-1, processed[len(processed)-1])    
    return processed

def main():
    # Let the user decide which file to plot
    file_name = input("Specify the name of the lightcurve to be analyzed (path will be: lightcurves/binary_stars/[INPUT].tbl): ")

    try:
        # Check if file exists
        assert path.isfile("lightcurves/binary_stars/{}.tbl".format(file_name))
        JULIAN_DATES, FLUX_PER_SECOND, FLUX_PER_SECOND_RAW = calculate_flux(file_name)
        MAGS, SMOOTHED_MAGS = plot_magnitude_lightcurve(JULIAN_DATES, FLUX_PER_SECOND, file_name)
        plot_raw_magnitude_lightcurve(JULIAN_DATES, FLUX_PER_SECOND_RAW, file_name)
        print_stats(MAGS, SMOOTHED_MAGS)

        plt.show()
    
    except AssertionError as e:
        print("File doesn't exist.")

if __name__ == "__main__":
    main()