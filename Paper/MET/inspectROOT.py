import sys
import ROOT
from tabulate import tabulate

def printTable(histograms):
    # Dictionary to store the process names and their corresponding systematic histograms
    process_systematics = {}

    # Loop over the histograms and extract the process names
    for histogram in histograms:
        # Split the histogram name by underscores
        name_parts = histogram.GetName().split("_")

        # Extract the process name and the systematic type
        process = name_parts[1]
        systematic = name_parts[2] if len(name_parts) > 2 else "Nominal"

        # Check if the process is data
        if "data" in process.lower():
            process = "Data"

        # Check if the process is one of the specified processes
        if process.lower() not in ["dy", "dynlo", "top", "ew", "ewk"]:
            continue

        # Check if the systematic is one of the specified variations
        if systematic.lower() not in ["jesup", "jesdown", "jerup", "jerdown", "unclusteredup", "unclustereddown"]:
            continue

        # Check if the process already exists in the dictionary
        if process in process_systematics:
            # Add the systematic histogram to the existing process entry
            process_systematics[process][systematic] = histogram
        else:
            # Create a new entry for the process and add the systematic histogram
            process_systematics[process] = {systematic: histogram}

    # Create a list of systematic types
    systematic_types = ["JES", "JER", "Unclustered"]

    # Create the table header
    header = ["Process", "Nominal"]
    for systematic in systematic_types:
        header.extend([f"{systematic} Up", f"{systematic} Down"])

    # Create the table rows
    rows = []
    for process, systematics in process_systematics.items():
        row = [process]

        # Check if the nominal systematic is present
        if "Nominal" in systematics:
            nominal_histogram = systematics["Nominal"]
        else:
            # Use the first available systematic as the nominal value
            nominal_histogram = next(iter(systematics.values()))

        nominal_value = nominal_histogram.GetSumOfWeights()
        row.append(nominal_value)

        # Loop over the systematic types
        for systematic in systematic_types:
            systematic_up_histogram = systematics.get(systematic + "Up")
            systematic_down_histogram = systematics.get(systematic + "Down")

            if systematic_up_histogram and systematic_down_histogram:
                systematic_up_value = systematic_up_histogram.GetSumOfWeights()
                systematic_down_value = systematic_down_histogram.GetSumOfWeights()
                row.extend([systematic_up_value, systematic_down_value])
            else:
                row.extend(["-", "-"])

        rows.append(row)

    # Print the table
    print(tabulate(rows, headers=header))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a ROOT file.")
        sys.exit(1)

    # Load the ROOT library
    ROOT.gROOT.SetBatch(True)

    # Open the ROOT file
    file = ROOT.TFile.Open(sys.argv[1])
    if not file or file.IsZombie():
        print("Failed to open the ROOT file.")
        sys.exit(1)

    # List to store the TH1 histograms
    histograms = []

    # Loop over all objects in the ROOT file
    key_list = file.GetListOfKeys()
    for key in key_list:
        obj = key.ReadObj()

        # Check if the object is a TH1 histogram
        if isinstance(obj, ROOT.TH1):
            histograms.append(obj)

    # Print the table
    printTable(histograms)



