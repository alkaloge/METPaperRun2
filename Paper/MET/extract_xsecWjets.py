import ROOT

# Open the text file
year='2018'
file_path = "samples_{0:s}_gjets.dat".format(year)

file_path = "samples_{0:s}_v2.dat".format(year)
file_path = "samples_{0:s}_2l.dat".format(year)
file_path = "samples_{0:s}_2l2nu.dat".format(year)
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

yD = year
if year == '2016postVFP' : yD = "2016"
for key, value in data_dict.iteritems():

    filemc='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/Gjets_out/{0:s}_{1:s}/{0:s}_{1:s}_Gjets.root'.format(key, yD)
    filemc='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/{0:s}_{1:s}/{0:s}_{1:s}_weights.root'.format(key, yD)
    filemc='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/HZZ2L2Nu/{0:s}_{1:s}/{0:s}_{1:s}_weights.root'.format(key, yD)
    #filemc='/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/2Lep/{0:s}_{1:s}/{0:s}_{1:s}_weights.root'.format(key, yD)
    fmc = ROOT.TFile(filemc, "READ")
    try : 
        hW = fmc.Get("hWeights")
        if 'WJetsToLNu' in key and 'nlo' not in key.lower() and 'ht' not in key.lower() : hW = fmc.Get("W0genWeights")
        weight_dict[key] = hW.GetSumOfWeights()
        #print filemc, key, 1000* lumis[year]*value/hW.GetSumOfWeights(), hW.GetSumOfWeights()
    except AttributeError : continue
    #if 'WJetsToLNu' in key

print("{")
for key, value in weight_dict.iteritems():

    print("    '{}' : {},".format(key, value))
print("}")
