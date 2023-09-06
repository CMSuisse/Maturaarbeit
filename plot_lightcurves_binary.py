from matplotlib import pyplot as plt
import numpy as np
from os import path
import csv

JULIAN_DATE_PREFIX = 0
MOVING_AVERAGE_WINDOW_SIZE = 20

def plot_lightcurves(file_path):
    with open("lightcurves/binary_stars/{}".format(file_path), encoding="UTF-8-sig") as file:
        file_reader = csv.reader(file)
        # Extract the values from the .csv files
        JULIAN_DATES = []
        RELMAGS = []
        MAGS = []
        for i, entry in enumerate(file_reader):
            # Determine the julian date prefix with the first entry
            if i == 0:
                JULIAN_DATE_PREFIX = int(entry[0].split(".")[0])
            # Subtract the julian date prefix from every julian date as this prefix is the same for every value in the csv
            JULIAN_DATES.append(float(entry[0]) - JULIAN_DATE_PREFIX)
            RELMAGS.append(float(entry[1]))
        
        file.close()

    # First, plot the lightcurve with the relative magnitude as the y-axis
    fig, ax = plt.subplots()
    ax.set_title("relMag lightcurve for sequence {}".format(file_path))
    ax.set_xlabel("Julian Date ({}+)".format(JULIAN_DATE_PREFIX))
    ax.set_ylabel("Relative magnitude")
    ax.invert_yaxis()
    ax.plot(JULIAN_DATES, RELMAGS, "o")
    # To smooth out the values, plot a moving average
    SMOOTHED_RELMAGS = moving_average(RELMAGS, MOVING_AVERAGE_WINDOW_SIZE)
    ax.plot(JULIAN_DATES, SMOOTHED_RELMAGS, linewidth=3)
    # Safe the figure in the correct folder and with a figure size that doesn't save a potato quality image
    fig.savefig("../Figures/images_results/relMag_{}.png".format(file_path), dpi=fig.get_dpi()*5)

    # Adjust each relMag value.
    for relmag in RELMAGS:
        # Calculate the conversion coefficient that has to be applied to get from relMag to mag
        conversion_coeff = -0.1595*relmag - 3.047
        MAGS.append(relmag*conversion_coeff)

    # Plot the adjusted light curve
    fig, ax = plt.subplots()
    ax.set_title("Mag lightcurve for sequence {}".format(file_path))
    ax.set_xlabel("Julian Date ({}+)".format(JULIAN_DATE_PREFIX))
    ax.set_ylabel("Magnitude")
    ax.invert_yaxis()
    ax.plot(JULIAN_DATES, MAGS, "o")
    # To smooth out the values, plot a moving average
    SMOOTHED_MAGS = moving_average(MAGS, MOVING_AVERAGE_WINDOW_SIZE)
    ax.plot(JULIAN_DATES, SMOOTHED_MAGS, linewidth=3)
    # Safe the figure in the correct folder and with a figure size that doesn't save a potato quality image
    fig.savefig("../Figures/images_results/Mag_{}.png".format(file_path), dpi=fig.get_dpi()*5)

    return MAGS, SMOOTHED_MAGS

def moving_average(array, window_size):
    window = np.ones(int(window_size))/float(window_size)
    processed = np.convolve(array, window, 'same')
    # Remove the first few and last few elements of the array as for these values the convolution windows wasn't filled
    processed = processed[window_size//2:len(processed)-window_size//2]
    # Fill up the list again
    for i in range(window_size//2):
        processed = np.insert(processed, 0, processed[0])
        processed = np.insert(processed, len(processed)-1, processed[len(processed)-1])    
    return processed

def print_stats(MAGS, SMOOTHED_MAGS):
    print("========== MAG stats ==========")
    print("Max value: {}mag".format(max(MAGS)))
    print("Min value: {}mag".format(min(MAGS)))
    print("========== SMOOTHED_MAG stats ==========")
    print("Max value: {}mag".format(max(SMOOTHED_MAGS)))
    print("Min value: {}mag".format(min(SMOOTHED_MAGS)))

def main():
    # Let the user decide which file to plot
    file_path = input("Specify the name of the lightcurve to be analyzed (path will be: lightcurves/binary_stars/[INPUT]): ")

    try:
        # Check if file exists
        assert path.isfile("lightcurves/binary_stars/{}".format(file_path))
        MAGS, SMOOTHED_MAGS = plot_lightcurves(file_path)
        print_stats(MAGS, SMOOTHED_MAGS)

        plt.show()
    
    except AssertionError as e:
        print("File doesn't exist.")

if __name__ == "__main__":
    main()