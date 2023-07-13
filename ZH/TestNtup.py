import ROOT
import argparse

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Define the command-line argument parser
parser = argparse.ArgumentParser(description="Read and print information from a ROOT file")
parser.add_argument("root_file", help="Path to the input ROOT file")

# Parse the command-line arguments
args = parser.parse_args()

# Open the specified ROOT file
file = ROOT.TFile(args.root_file)

# Get the TTree called "Events"
tree = file.Get("Events")

# Define the base branches to scan
base_branches = [
    "u_par_RawMET",
    "u_par_MET_T1",
    "u_par_METCor_T1",
    "u_par_METCorGood_T1",
    "u_par_MET_T1Smear",
    "u_par_METCor_T1Smear",
    "u_par_METCorGood_T1Smear",
    "u_par_PuppiMET",
    "u_par_PuppiMETCor",
    "u_par_PuppiMETCorGood",
]
base_branches = [
    "MET_T1",
    "METCor_T1",
    "METCorGood_T1",
    "MET_T1Smear",
    "METCor_T1Smear",
    "METCorGood_T1Smear",
    "PuppiMET",
    "PuppiMETCor",
    "PuppiMETCorGood",
]



# Define the lists for systematic variations
ptphis = ["pt", "phi"]
systematics = ["", "JES", "JER"]
systematics = ["", "JES", "JER","Unclustered"]
directions = ["Up", "Down"]

# Construct the final list of branches to scan
branches_to_scan = []

branches_to_scan.append("MET_pt")
branches_to_scan.append("MET_phi")
branches_to_scan.append("MET_T1_pt")
branches_to_scan.append("MET_T1_phi")
for base_branch in base_branches:
    branches_to_scan.append(base_branch)

    #for pts in ptphis:
    for systematic in systematics:
	for pts in ptphis:
	    for direction in directions:
                if len(systematic) > 0 : 
		    #branches_to_scan.append("{}{}{}".format(base_branch, systematic, direction))
		    branches_to_scan.append("{}_{}{}{}".format(base_branch, pts,systematic, direction))
                else : 
		    branches_to_scan.append("{}_{}{}".format(base_branch, pts,systematic))
                    continue

# Split branches_to_scan into smaller chunks
chunk_size = 25  # Adjust this value as needed
branch_chunks = list(chunks(branches_to_scan, chunk_size))

# Scan the specified branches in chunks
for i, branch_chunk in enumerate(branch_chunks):
    print branch_chunk
    print("Scanning chunk {} of {}".format(i+1, len(branch_chunks)))
    tree.Scan(":".join(branch_chunk))

# Close the file
file.Close()


