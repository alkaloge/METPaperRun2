import sys
from ROOT import TFile, TH1F, TIter

# Open the ROOT file
root_file = TFile.Open(sys.argv[1])

# Get the list of keys in the top-level directory
key_list = root_file.GetListOfKeys()

# Loop over the keys
for key in TIter(key_list):
    obj = key.ReadObj()
    if isinstance(obj, TH1F):
        name = obj.GetName()
        sum_of_weights = obj.GetSumOfWeights()
        
        # Print name and sum of weights
        print("Name: {0}, Sum of Weights: {1}".format(name, sum_of_weights))
        
        # Set the histogram color to red if sum of weights is less than 1

# Close the ROOT file
root_file.Close()


