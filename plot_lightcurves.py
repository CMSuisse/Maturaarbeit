from matplotlib import pyplot as plt
import numpy as np
from os import path
import csv

def plot_lightcurve(file_path):
    with open("lightcurves/{}.csv".format(file_path), encoding="UTF-8-sig") as file:
        file_reader = csv.reader(file)
        # Extract the values from the .csv files
        JULIAN_DATES = []
        RELMAGS = []
        for julian_date, relmag in file_reader:
            # Subtract 2460180 from every julian date as this prefix is the same for every value
            JULIAN_DATES.append(float(julian_date) - 2460180)
            RELMAGS.append(float(relmag))
        
        file.close()

    # Calculate the median and average
    RELMAG_MEDIAN = np.median(RELMAGS)
    RELMAG_AVERAGE = np.average(RELMAGS)
    print("Median is: {}".format(RELMAG_MEDIAN))
    print("Average and median are off by {} magnitudes".format(abs(RELMAG_AVERAGE - RELMAG_MEDIAN)))

    # Plot the values as well as median and average values in a scatter plot with connecting lines
    fig, ax = plt.subplots()
    ax.set_title("Unadjusted lightcurve of file {}".format(file_path))

    ax.set_xlabel("Julian Date (2460180+)")
    ax.set_ylabel("Relative magnitude")

    ax.plot(JULIAN_DATES, RELMAGS, ":o")
    ax.axhline(RELMAG_MEDIAN, linestyle = "--", color = "green")
    ax.axhline(RELMAG_AVERAGE, linestyle = ":", color = "green")

    # Coefficient calculations are done only on the median, hence the average is not returned
    return JULIAN_DATES, RELMAGS, RELMAG_MEDIAN
    
def plot_adjusted_lightcurve(truemag, RELMAG_MEDIAN, JULIAN_DATES, RELMAGS, file_path):
    # Convert all the relative magnitudes to apparent magnitudes
    COEFF = truemag/RELMAG_MEDIAN
    MAGS = list(map(lambda x: COEFF*x, RELMAGS))

    # Plot the values again, this time only show the median
    fig, ax = plt.subplots()
    ax.set_title("Adjusted lightcurve of file {}".format(file_path))

    ax.set_xlabel("Julian Date (2460180+)")
    ax.set_ylabel("Apparent magnitude")

    ax.plot(JULIAN_DATES, MAGS, ":o")
    ax.axhline(np.median(MAGS), linestyle = "--", color = "green")
    print("Conversion coefficient was {}.".format(COEFF))
    

def main():
    # Let the user decide which file to plot
    file_path = input("Specify the name of the lightcurve to be analyzed (path will be: lightcurves/[INPUT].csv): ")
    # Allow the user to enter the actual magnitude of the star if it is a refernce star
    truemag = input("Magnitude the star actually has (press ENTER if not reference star): ")
    if not truemag == "":
        truemag = float(truemag)

    try:
        # Check if file exists
        assert path.isfile("lightcurves/{}.csv".format(file_path))
        JULIAN_DATES, RELMAGS, RELMAG_MEDIAN = plot_lightcurve(file_path)
        if not truemag == "":
            plot_adjusted_lightcurve(truemag, RELMAG_MEDIAN, JULIAN_DATES, RELMAGS, file_path)

        plt.show()
    
    except AssertionError as e:
        print("File doesn't exist.")

if __name__ == "__main__":
    main()