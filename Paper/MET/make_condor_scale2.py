import os
import errno

proc = "ZToLL"
# Directory containing the input files
input_dir = "/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/Gjets_out_cutBased/"
if proc == "ZToLL" : input_dir = "/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/"

# Output directory for JDL files
output_ = "condor_jdls/"

# Path to the get_scales.py script
get_scales_script = "get_scales2.py"

# Create the output directory if it doesn't exist

# List of dataset names to include

# List of keywords to identify datasets
keywords = ["DYJetsToLLM50_"]#, "SingleMuon", "SingleElectron", "EGamma"]
keywords = ["DYJetsToLLM50_", "SingleMuon", "SingleElectron"]
keywords = ["DYJetsToLLM50_", "SingleMuon", 'EGamma']
keywords = ["SingleMuon", "SingleElectron"]
keywords = ["DYJetsToLLM50_", 'NLO']
#keywords = ["DYJetsToLLM10", "DYJetsToLLM50NLO_", "SingleMuon", "SingleElectron", "EGamma"]
if proc == "ZToLL" : keywords = ["DYJetsToLLM50NLO_", "SingleMuon", "SingleElectron", "EGamma"]

#keywords = ['GJets_HT', 'EGamma', 'SinglePhoton', 'WJetsToLNu_NLO', 'QCD_HT']
#keywords = ['WJetsToLNu_NLO', 'QCD_HT']
#keywords = ['QCD_HT']

isMC = 'ismc'
#ismc MuMu 2018 dy
Channels=['Gjets']
if proc == "ZToLL" : Channels=['MuMu', 'ElEl']

year='2016preVFP'
year='2016'
Njet=['eq0', 'eq1', 'geq1', 'incl']
#Njet=['eq1', 'incl']

filesToRun = 10
for channel in Channels : 
    #try:
    try : 
        output_dir = output_+channel+"_"+year
        os.makedirs(output_dir)
    except OSError as e: print 'dir exists', output_dir
    #if e.errno != errno.EEXIST:
    #    raise
    for dir_name in os.listdir(input_dir):
	if ('2017' in year or '2018' in year or year=='2016')  and year not in dir_name : continue
        if year =="2016" and 'preV' in dir_name : continue
        if year =="2016preVFP" and 'preVFP' not in dir_name : continue

	if ('SingleElectron' in dir_name or 'EGamma' in dir_name) and channel == 'MuMu' : continue
	if ('SingleMuon' in dir_name or 'Photon' in dir_name) and channel == 'ElEl' : continue
	if 'Single' in dir_name or 'EGamma' in dir_name : isMC = 'isdata'
	else : isMC = 'ismc'
        

        if any(keyword in dir_name for keyword in keywords):
            dir_path = os.path.join(input_dir, dir_name)
            file_list = os.listdir(dir_path)
            file_list = [item for item in file_list if 'weight' not in item]
            if 'Electron' in dir_path and channel =='MuMu' : continue
            if 'EGamma' in dir_path and channel =='MuMu' : continue
            if 'Muon' in dir_path and channel =='ElEl' : continue
            if 'Run' not in dir_path : file_list = [item for item in file_list if 'part'  in item]
            if 'Run' in dir_path : file_list = [item for item in file_list if 'all_'  in item]
            if channel == 'MuMu' : file_list = [item for item in file_list if 'Muon'  in item]
            if channel == 'ElEl' : file_list = [item for item in file_list if ('Electron'  in item or 'EGamma' in item)]

            for i in range(0, len(file_list), filesToRun):
                batch_files = file_list[i:i + filesToRun]
                print 'working on', i, batch_files[0], batch_files
                jdl_file = os.path.splitext(batch_files[0])[0] + ".jdl"
                jdl_path = os.path.join(output_dir, jdl_file)

                script_file = os.path.splitext(batch_files[0])[0] + ".sh"
                script_out = os.path.splitext(batch_files[0])[0] + ".root"
                script_path = os.path.join(output_dir, script_file)


                command_string = ""
                for file in batch_files:
                    file_path = os.path.join(dir_path, file)
                    #print 'some info', file_path, dir_path, file
                    #if 'run20' in file_path.lower() or 'Single' in dir_path or 'EGamma' in dir_path:
                    #    isMC = 'isdata'
                    #if 'run' not in file:
                    #    isMC = 'ismc'
                    if 'Electrons' in file and 'MuMu' in channel: continue
                    if 'Muons' in file and 'ElEl' in channel: continue
                    if 'M50' not in dir_path and channel not in file and 'Run20' not in dir_path : continue
		    if file.endswith(".root"):
			command_string += "xrdcp root://cmseos.fnal.gov/{} inFile_{}\n".format(file_path, file)
			command_string += "echo 'Executing get_scales2.py with list.txt'\n"
                        for njet in Njet : 
                            #print 'lets see', njet, isMC, channel, file
			    command_string += "python {} {} {} {} {} {} \n".format(get_scales_script, isMC, channel, year, njet, file)
			    command_string += "mv output_Njet{0:s}.root scales_Njet{0:}_{1:s} \n".format(njet,file)
			#command_string += "python {} {} {} {}\n".format(get_scales_script, isMC, channel, year)
			#command_string += "mv output.root scales_{}_{}\n".format(script_out, file)
			#command_string += "cp scales_Njet{0:}_{1:s} .\n".format(njet,script_out)
			command_string += "rm inFile_{}\n".format(file)

			with open(jdl_path, "w") as f:
			    f.write("executable = {}\n".format(script_file))
			    f.write("output = {}\n".format(os.path.splitext(batch_files[0])[0] + ".out"))
			    f.write("error = {}\n".format(os.path.splitext(batch_files[0])[0] + ".err"))
			    f.write("log = {}\n".format(os.path.splitext(batch_files[0])[0] + ".log"))
			    f.write("transfer_input_files = /uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/Paper/MET/get_scales2.py \n")
			    #f.write("transfer_output_files = scales_{}\n".format(script_out))
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
			    f.write("echo 'Listing .root files on EOS:'\n")
			    f.write(command_string)



	 
			    #f.write("xrdcp root://cmseos.fnal.gov/{} inFile.root\n".format(file_path))
			    #f.write("echo 'Executing get_scales2.py with list.txt'\n")
			    #ismc MuMu 2018 dy
			    #f.write("python {} {} {} {}\n".format(get_scales_script, isMC, channel, year))
			    #f.write("mv output.root scales_{} \n".format(script_out))
			    #f.write("rm inFile.root \n")

			    # Make the shell script executable
		        os.chmod(script_path, 0o755)


    # Print a message with the number of generated JDL files
    num_jdls = len(os.listdir(output_dir))
    print("Generated {} JDL files in {}".format(num_jdls, output_dir))


