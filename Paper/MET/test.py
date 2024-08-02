import ROOT
from array import array
ROOT.gROOT.SetBatch(True)

# Binning array
varbins = [0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.]

# Create canvas
canvas = ROOT.TCanvas("canvas", "TGraph Errors Example", 800, 600)
canvas.SetFillColor(0)
canvas.SetFrameFillColor(0)

# Create empty list to store TGraphs
graphs = []

# Open data file
with open("data.txt", "r") as file:
    lines = file.readlines()

    # Loop over lines in the file
    for i, line in enumerate(lines):
        # Remove leading/trailing whitespaces and split the line into values
        values = line.strip().split("\t")

        # Extract y-value and error from 2nd and 3rd columns
        y_value = float(values[1])
        y_error = float(values[2])

        # Calculate x bin based on index and binning array
        x_bin = i % len(varbins) + 1
        #x_value = (varbins[i % len(varbins)] + varbins[(i % len(varbins)) + 1]) / 2.0
        x_value = i*10+20
        print x_bin, x_value, y_value, 'i---', i, line
        # Create TGraphErrors with a single point for each line
        graph = ROOT.TGraphErrors(1, array("d", [x_value]), array("d", [y_value]), array("d", [0]), array("d", [y_error]))

        # Add the graph to the list
        graphs.append(graph)

# Draw the first graph on the canvas to set the axis
canvas.cd()
graphs[0].Draw("AP")

# Set axis labels
canvas.Update()
axis = graphs[0].GetHistogram().GetXaxis()
axis.Set(len(varbins) - 1, array("d", varbins))

# Draw all graphs on the canvas
for i in range(len(graphs)):
    if i != 0:
        graphs[i].Draw("P")

# Set canvas options
canvas.SetGrid()

# Save canvas to PDF
canvas.Print("output.pdf")

# Close canvas
canvas.Close()



