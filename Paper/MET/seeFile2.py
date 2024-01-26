import ROOT
import sys

# Define the samples, systematics, and variations
samples = ['data', 'dy', 'qcd', 'top', 'ew', 'ewknlo61', 'ewknlo', 'ewkincl', 'ewkht', 'ewk']

systs = ['JES', 'Unclustered', 'JER', 'ID', 'PU']
variations = ['Up', 'Down']

# Get the ROOT file
#root_file = ROOT.TFile(sys.argv[1])

vars=["METCorGood_T1_phi", "PuppiMETCorGood_phi", "METCorGoodboson_phi", "PuppiMETCorGoodboson_phi", "METCorGood_T1Smear_phi", "RawMET_phi", "RawPuppiMET_phi" , "RawMET_phi", "RawPuppiMET_phi", "RawMET_pt", "RawPuppiMET_pt", 'u_parboson_RawMET', 'u_parboson_RawPuppiMET', 'u_perp_RawMET', "u_parboson_RawMET", "u_parboson_RawPuppiMET", "u_perp_RawMET", "u_perp_RawPuppiMET", "u_parboson_METCorGood_T1Smear", "u_parboson_METCorGood_T1", "u_perp_METCorGood_T1Smear", "u_perp_METCorGood_T1", "u_parboson_PuppiMETCorGood", "u_perp_PuppiMETCorGood",   "METCorGood_T1_pt", "PuppiMETCorGood_pt", "METCorGoodboson_pt", "PuppiMETCorGoodboson_pt", "METCorGood_T1Smear_pt","METCorGoodboson_m", "PuppiMETCorGoodboson_m", "METCorGoodboson_transm", "PuppiMETCorGoodboson_transm","MET_T1_pt", "MET_T1_phi", "PuppiMET_pt", "PuppiMET_phi"]

#vars=["METCorGood_T1_phi"]
channel='MuNu'
report=[]
year='2017'
for var in vars:
    #root_file = ROOT.TFile("plotS_"+sys.argv[1]+"_njetsgt0_nbtagl_cutbased_varbins_vetolept_isolt0p15_mtmassgt80_hitslt1_"+sys.argv[2]+"_"+sys.argv[3]+".root")
    root_file = ROOT.TFile("plotS_"+year+"_njetsgt0_nbtagl_cutbased_varbins_vetolept_isolt0p15_mtmassgt80_hitslt1_"+var+"_"+channel+".root")

    # Create a table to store the results
    table = []
    # Iterate over the samples
    for sample in samples:

	# Create a row for the table
	row = [sample]
	
	# Get the nominal histogram
	#sname = "histo_" + sample + "_"+str(sys.argv[2])#PuppiMETCorGoodboson_pt"
	sname = "histo_" + sample + "_"+str(var)#PuppiMETCorGoodboson_pt"
	#sname = "histo_" + sample + "_u_perp_PuppiMETCorGood"
	#sname = "histo_" + sample + "_u_parboson_METCorGood_T1"
	nominal_hist = root_file.Get(str(sname))
	if nominal_hist : 
	    print nominal_hist.GetName(), nominal_hist.GetSumOfWeights(), sname
	    # Add the nominal SumOfWeight to the row
	    row.append(round(nominal_hist.GetSumOfWeights(),2))

	    # Iterate over the systematics and variations
	    for syst in systs:
		for variation in variations:

		    # Get the systematic histogram
		    svar = sname +syst + variation
		    syst_hist = root_file.Get(str(svar))
		    print 'trying to get ', svar
		       
		    if syst_hist and syst_hist.GetSumOfWeights() : # Add the systematic SumOfWeight to the row
			row.append(round(nominal_hist.GetSumOfWeights()/syst_hist.GetSumOfWeights(),2))
		    else : 
                        row.append("-")
                        bug=str(year+"_"+svar)
                        if not ('Raw' in var and ('Up' in variation or 'Down' in variation)) : 
                            report.append(bug)

	    # Add the row to the table
	    table.append(row)

    # Print the table
    print("sample/var\t nom\t" + "\t".join([syst + variation for syst in systs for variation in variations]))
    for row in table:
	print("\t   ".join([str(x) for x in row]))

print report
