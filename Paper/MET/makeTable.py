import ROOT
import random

# Define input histograms for each process
hist1 = ROOT.TH1F("hist1", "Process 1", 10, 0, 10)
hist2 = ROOT.TH1F("hist2", "Process 2", 10, 0, 10)
hist3 = ROOT.TH1F("hist3", "Process 3", 10, 0, 10)

# Fill histograms with random values
for i in range(100):
    hist1.Fill(random.randint(0, 9))
    hist2.Fill(random.randint(0, 9))
    hist3.Fill(random.randint(0, 9))

# Define input THStack histogram
stack_hist = ROOT.THStack("stack", "Stacked Histogram")
stack_hist.Add(hist1)
stack_hist.Add(hist2)
stack_hist.Add(hist3)

# Create a list of the input histogram/process names
hist_names = ["hist1", "hist2", "hist3"]
process_names = ["process1", "process2", "process3"]

# Create a list of cut names
cuts = [2, 4, 6, 8]

# Create a dictionary to store the cutflow for each histogram/process
cutflow_dict = {}
for hist_name in hist_names:
    cutflow_dict[hist_name] = {}
    for process_name in process_names:
        cutflow_dict[hist_name][process_name] = [0]*len(cuts)

# Loop over the input histogram/processes
for i, hist_name in enumerate(hist_names):
    hist = stack_hist.GetStack().At(i).Clone(hist_name)
    for j, process_name in enumerate(process_names):
        # Get the contribution for each cut
        for k, cut in enumerate(cuts):
            cutflow_dict[hist_name][process_name][k] = hist.Integral(0, hist.FindBin(float(cut)))

# Print the cutflow table for each histogram/process
for hist_name in hist_names:
    print("Histogram: ", hist_name)
    print("Process\t\tCut1\t\tCut2\t\tCut3\t\tCut4")
    for process_name in process_names:
        cutflow_row = "\t".join([str(int(x)) for x in cutflow_dict[hist_name][process_name]])
        print(process_name + ":\t" + cutflow_row)
    print("")


