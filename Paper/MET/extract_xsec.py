import ROOT

# Open the text file
year='2016preVFP'
file_path = "samples_{0:s}_gjets.dat".format(year)
file = open(file_path, "r")

# Create an empty dictionary
data_dict = {}
weight_dict = {}

# Loop through each line in the file
for line in file:
    # Remove leading/trailing whitespaces and split the line into columns
    columns = line.strip().split()
    # Check if the line is empty or does not have enough columns
    if len(columns) < 6 or line.startswith("#"): continue

    # Get the values from the third and sixth columns
    value1 = columns[2]
    value2 = float(columns[5])

    # Add the values to the dictionary
    data_dict[value1] = value2

# Close the file
file.close()

# Print the resulting dictionary
lumis={'2016':35.93, '2017':41.48, '2018':59.83}
print("{")
for key, value in data_dict.iteritems():

    print("    '{}' : {},".format(key, value))
print("}")

for key, value in data_dict.iteritems():

    filemc='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/Gjets_out/{0:s}_{1:s}/{0:s}_{1:s}_Gjets.root'.format(key, year)
    fmc = ROOT.TFile(filemc, "READ")
    try : 
        hW = fmc.Get("hWeights")
        weight_dict[key] = hW.GetSumOfWeights()
        #print filemc, key, 1000* lumis[year]*value/hW.GetSumOfWeights(), hW.GetSumOfWeights()
    except AttributeError : continue

print("{")
for key, value in weight_dict.iteritems():

    print("    '{}' : {},".format(key, value))
print("}")
