import sys
import ROOT

# Check if the input file is given
if len(sys.argv) < 2:
    print "Please provide the input file name as an argument."
    sys.exit(1)

# Open the ROOT file
try:
    input_file = ROOT.TFile(sys.argv[1])
except Exception as ex:
    print "Failed to open file:", ex
    sys.exit(1)

processes = ["ew", "dy", "dynlo", "top", "data"]
systematics = ["JES", "JER", "Unclustered"]

# Create a dictionary to store the results
results = {}
for proc in processes:
    results[proc] = {"Main": 0.0}
    for syst in systematics:
        results[proc]["{}_up".format(syst)] = 0.0
        results[proc]["{}_down".format(syst)] = 0.0

hist = input_file.Get("histo_data")
results['data']["Main"] = hist.GetSumOfWeights()

# Loop over all histograms in the ROOT file
for proc in processes:
    if "data" in proc.lower():
        # Only central value for data
        results[proc]["Main"] = input_file.Get("histo_data").GetSumOfWeights()
    else:
        # Get central value for the process
        main = input_file.Get("histo_{}_METCorGood_T1Smear_pt".format(proc)).GetSumOfWeights()
        results[proc]["Main"] = main
        # Get systematics up/down values for the process
        for syst in systematics:
            hist_up = input_file.Get("histo_{}_METCorGood_T1Smear_pt{}Up".format(proc, syst))
            hist_down = input_file.Get("histo_{}_METCorGood_T1Smear_pt{}Down".format(proc, syst))
            if hist_up and hist_down:
                up = hist_up.GetSumOfWeights()
                down = hist_down.GetSumOfWeights()
                results[proc]["{}_up".format(syst)] = up 
                results[proc]["{}_down".format(syst)] = down 

print("Process\tMain\tJES_up\tJES_down\tJER_up\tJER_down\tUnclustered_up\tUnclustered_down")
for proc in processes:
    values = [round(results[proc]["Main"], 2)]
    for syst in systematics:
        values.append(round(results[proc]["{}_up".format(syst)], 2))
        values.append(round(results[proc]["{}_down".format(syst)], 2))
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(proc, *values))




