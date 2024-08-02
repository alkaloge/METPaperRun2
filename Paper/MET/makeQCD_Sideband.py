import os
import ROOT

# Function to check if a file name contains the specified substrings
def contains_substrings(filename, substrings):
    for substring in substrings:
        if substring in filename:
            return True
    return False

# Function to rename TH1 histograms
def rename_histogram(histogram, suffix):
    # Extract the original histogram name
    original_name = histogram.GetName()
    
    # Append the suffix to the original name
    new_name = original_name + suffix
    
    # Set the new name for the histogram
    histogram.SetName(new_name)

# Directory where the ROOT files are located
input_dir = "Jobs_gjets"
input_dir = "./"

# List of substrings to check for in file names
substrings_to_check = ["sidebandb", "sidebandc", "sidebandd"]

samples=['tx', 'ew', 'ewknlo',  'qcdmg', 'gjets' ]
samples=['ew_']

dirs = ['Up', 'Down']
systs =['JES', 'Unclustered', 'JER']
systs =['nom', 'JES', 'Unclustered', 'JER', 'ID', 'PU']
varbs=['METCorGood_T1_pt']
sidebands=['sidebandb', 'sidebandc', 'sidebandd']

njets=['njetsgt0_','njetsgeq0_']

#plotS_2018_ew_njetsgt0_nbtagl_cutbased_varbins_sidebandc_hitslt1_METCorGood_T1_ptIDUp_Gjets.roo
year='2018'
for njet in njets:
    for side in sidebands : 
	for var in varbs :
	    for proc in samples : 
		for dirr in dirs : 
		    for syst in systs : 
		   
			sys=syst+dirr

			if 'nom' in syst  : sys=''
			if 'nom' in syst  and 'Down' in dirr: continue # to ensure that you run syst only once
			root_Name="plotS_{0:s}_{1:s}{2:s}nbtagl_cutbased_varbins_{3:s}_hitslt1_{4:s}{5:s}_Gjets.root".format(year, proc, njet, side, var, sys)

			print 'will check', root_Name, os.path.isfile(root_Name)
			if os.path.isfile(root_Name):
			    print 'will work for syst', syst, sys
				
			    new_histogram_name = ''
			    histogram_name = ''
				
			    root_file = ROOT.TFile(root_Name, "UPDATE")

			    if 'data' in proc :
				histogram_name = 'histo_data'
			    else :
			    
				histogram_name = ("histo_"+proc+var+sys)
			     
			    histo = root_file.Get('{}'.format(histogram_name))

			    print 'read out histo', histo.GetName(), histo.Integral(), histogram_name

			    new_histogram_name = histogram_name + "_"+side
                            h1 = root_file.Get(new_histogram_name)                           
                            try : hs = h1.Integral() 
		            except  AttributeError:
				if 'data' not in proc and histo.Integral()>0: histo.Scale(-1)
				histo.Write(new_histogram_name)
			    # Close the ROOT file
			    root_file.Close()


