from matplotlib import pyplot as plt
import numpy as np
from os import path
import csv

JULIAN_DATE_PREFIX = 0

def plot_lightcurve(file_name):
    global JULIAN_DATE_PREFIX
    with open("lightcurves/ref_stars/auto_aperture/{}".format(file_name), encoding="UTF-8-sig") as file:
        file_reader = csv.reader(file)
        # Extract the values from the .csv files
        JULIAN_DATES = []
        RELMAGS = []
        for i, entry in enumerate(file_reader):
            # Determine the julian date prefix with the first entry
            if i == 0:
                JULIAN_DATE_PREFIX = int(entry[0].split(".")[0])
            # Subtract the julian date prefix from every julian date as this prefix is the same for every value in the csv
            JULIAN_DATES.append(float(entry[0]) - JULIAN_DATE_PREFIX)
            RELMAGS.append(float(entry[1]))
        
        file.close()

    # Calculate the median and average
    RELMAG_MEDIAN = np.median(RELMAGS)
    RELMAG_AVERAGE = np.average(RELMAGS)
    print("Median is: {}".format(RELMAG_MEDIAN))
    print("Average and median are off by {} magnitudes".format(abs(RELMAG_AVERAGE - RELMAG_MEDIAN)))

    # Plot the values as well as median and average values in a scatter plot with connecting lines
    fig, ax = plt.subplots()
    ax.set_title("Unadjusted lightcurve for sequence {}".format(file_name))
    ax.set_xlabel("Julian Date ({}+)".format(JULIAN_DATE_PREFIX))
    ax.set_ylabel("Relative magnitude")

    ax.plot(JULIAN_DATES, RELMAGS, "o")
    ax.axhline(RELMAG_MEDIAN, linestyle = "--", color = "green")
    ax.axhline(RELMAG_AVERAGE, linestyle = ":", color = "green")

    # Coefficient calculations are done only on the median, hence the average is not returned
    return JULIAN_DATES, RELMAGS, RELMAG_MEDIAN
    
def plot_adjusted_lightcurve(truemag, RELMAG_MEDIAN, JULIAN_DATES, RELMAGS, file_name):
    # Convert all the relative magnitudes to apparent magnitudes
    COEFF = truemag/RELMAG_MEDIAN
    MAGS = list(map(lambda x: COEFF*x, RELMAGS))

    # Plot the values again, this time only show the median
    fig, ax = plt.subplots()
    ax.set_title("Adjusted lightcurve for sequence {}".format(file_name))

    ax.set_xlabel("Julian Date ({}+)".format(JULIAN_DATE_PREFIX))
    ax.set_ylabel("Apparent magnitude")

    ax.plot(JULIAN_DATES, MAGS, "o")
    ax.axhline(np.median(MAGS), linestyle = "--", color = "green")
    print("Conversion coefficient was {}".format(COEFF))
    

def main():
    # Let the user decide which file to plot
    file_name = input("Specify the name of the lightcurve to be analyzed (path will be: lightcurves/ref_stars/auto_aperture/[INPUT]): ")
    # Allow the user to enter the actual magnitude of the star to calculate the conversion coefficient
    truemag = input("Magnitude the star actually has: ")
    truemag = float(truemag)

    try:
        # Check if file exists
        assert path.isfile("lightcurves/ref_stars/auto_aperture/{}".format(file_name))
        JULIAN_DATES, RELMAGS, RELMAG_MEDIAN = plot_lightcurve(file_name)
        plot_adjusted_lightcurve(truemag, RELMAG_MEDIAN, JULIAN_DATES, RELMAGS, file_name)

        plt.show()
    
    except AssertionError as e:
        print("File doesn't exist.")

if __name__ == "__main__":
    main()