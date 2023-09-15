import os
import errno

# Directory containing the input files
input_dir = "/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/"
input_dir = "/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets_out/"

# Output directory for JDL files
output_ = "condor_jdls/"

# Path to the get_scales.py script
get_scales_script = "get_scales2.py"

# Create the output directory if it doesn't exist

# List of dataset names to include
datasets = ["DYJets"]

# List of keywords to identify datasets
keywords = ["DYJetsToLL", "SingleMuon", "SingleElectron", "EGamma" ]
keywords = ["EGamma", "GJets_HT"]

isMC = 'ismc'
#ismc MuMu 2018 dy
Channels=['MuMu', 'ElEl']
Channels=['MuMu']
year='2018'
Njet=['eq0', 'eq1', 'geq1', 'incl']

for channel in Channels : 
    #try:
    try : 
        output_dir = output_+channel+"_"+year
        os.makedirs(output_dir)
    except OSError as e: print 'dir exists', output_dir
    #if e.errno != errno.EEXIST:
    #    raise
    for dir_name in os.listdir(input_dir):
        print dir_name
	if ('2017' in year or '2018' in year or year=='2016')  and year not in dir_name : continue
        if year =="2016" and 'preV' in dir_name : continue
	if ('SingleElectron' in dir_name or 'EGamma' in dir_name) and channel == 'MuMu' : continue
	if ('SingleMuon' in dir_name ) and channel == 'ElEl' : continue
	if ('EGamma' in dir_name ) and channel == 'MuMu' : continue
	if ('SingleElectron' in dir_name ) and channel == 'MuMu' : continue
	if any(keyword in dir_name for keyword in keywords):
	    dir_path = os.path.join(input_dir, dir_name)
	    
	    # Loop over the files in the directory
	    for file in os.listdir(dir_path):
		#if 'all_' in file or 'Muons' in file or 'Electrons' in file: continue
		if 'Electrons' in file and 'MuMu' in channel: continue
		if 'Muons' in file and 'ElEl' in channel: continue
		#if 'Run20' not in dir_path and channel not in file : continue
		if 'M50' not in dir_path and channel not in file and 'Run20' not in dir_path : continue
		if file.endswith(".root"):
		    file_path = os.path.join(dir_path, file)
		    if 'run20' in file_path.lower() : isMC ='isdata'
		    if 'DY' in file : isMC ='ismc'
		    # Prepare the JDL file name based on the input file name
		    jdl_file = os.path.splitext(file)[0] + ".jdl"
		    jdl_path = os.path.join(output_dir, jdl_file)
		    
		    # Prepare the shell script name based on the input file name
		    script_file = os.path.splitext(file)[0] + ".sh"
		    script_out = os.path.splitext(file)[0] + ".root"
		    script_path = os.path.join(output_dir, script_file)
		    
		    # Write the JDL content
		    with open(jdl_path, "w") as f:
			f.write("executable = {}\n".format(script_file))
			f.write("output = {}\n".format(os.path.splitext(file)[0] + ".out"))
			f.write("error = {}\n".format(os.path.splitext(file)[0] + ".err"))
			f.write("log = {}\n".format(os.path.splitext(file)[0] + ".log"))
			f.write("transfer_input_files = /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET/get_scales2.py \n")
			f.write("transfer_output_files = scales_{}\n".format(script_out))
			f.write("when_to_transfer_output = ON_EXIT\n")
			f.write("priority = 10\n")
			f.write("queue\n")
		    
     
		    with open(script_path, "w") as f:
			f.write("#!/bin/bash\n")
			f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
			f.write("export SCRAM_ARCH=slc7_amd64_gcc820\n")
			f.write("eval `scramv1 project CMSSW CMSSW_10_6_5`\n")
			f.write("cd CMSSW_10_6_5/src\n")
			f.write("eval `scramv1 runtime -sh`\n")
			f.write("cmsenv\n")
			f.write("cd ${_CONDOR_SCRATCH_DIR}/CMSSW_10_6_5/src/\n")
			f.write("scram b -j 4\n")
			f.write("echo ${_CONDOR_SCRATCH_DIR}\n")
			f.write("cd ${_CONDOR_SCRATCH_DIR}\n")
			#f.write("cp ${_CONDOR_SCRATCH_DIR}/* .\n")
			f.write("echo 'Listing .root files on EOS:'\n")
			f.write("xrdcp root://cmseos.fnal.gov/{} inFile.root\n".format(file_path))
			f.write("echo 'Executing get_scales2.py with list.txt'\n")
			#ismc MuMu 2018 dy
                        for njet in Njet : 
			    f.write("python {} {} {} {} {}\n".format(get_scales_script, isMC, channel, year, njet))
			    f.write("mv output_Njet{0:s}.root scales_Njet{0:}{1:s}} \n".format(njet,script_out))
			f.write("rm inFile.root \n")

		    # Make the shell script executable
		    os.chmod(script_path, 0o755)


    # Print a message with the number of generated JDL files
    num_jdls = len(os.listdir(output_dir))
    print("Generated {} JDL files in {}".format(num_jdls, output_dir))


