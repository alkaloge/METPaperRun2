
import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    defDS = '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM '
    parser.add_argument("--dataSet",default=defDS,help="Data set name.") 
    parser.add_argument("--nickName",default='MCpileup',help="Data set nick name.") 
    parser.add_argument("-m","--mode",default='anaXRD',help="Mode (script to run).")
    parser.add_argument("-y","--year",default=2017,type=str,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-c","--concatenate",default=5,type=int,help="On how many files to run on each job")
    parser.add_argument("-s","--selection",default='ZH',type=str,help="select ZH or AZH")
    parser.add_argument("-j","--doSystematics",default='yes',type=str,help="do JME systematics")
    parser.add_argument("-l","--islocal",default='no',type=str,help="get list from /eos/ not DAS")
    parser.add_argument("-w","--weights",default='no',type=str,help="get list from /eos/ not DAS")
    return parser.parse_args()

def beginBatchScript(baseFileName, Systematics) :
    outLines = ['#!/bin/bash\n']
    outLines.append("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
    outLines.append("export SCRAM_ARCH=slc7_amd64_gcc820\n")
    outLines.append("eval `scramv1 project CMSSW CMSSW_10_6_5`\n")
    outLines.append("cd CMSSW_10_6_5/src\n")
    outLines.append("eval `scramv1 runtime -sh`\n")
    outLines.append("cmsenv\n")
    outLines.append("git clone --recursive https://github.com/cms-nanoAOD/correctionlib.git\n")
    outLines.append("cd correctionlib;make PYTHON=python;make install\n")
    outLines.append("cd ${_CONDOR_SCRATCH_DIR}/CMSSW_10_6_5/src/\n")
    #outLines.append("git clone https://github.com/cms-tau-pog/TauIDSFs TauPOG/TauIDSFs\n")
    #outLines.append("tar -zxvf ${_CONDOR_SCRATCH_DIR}/taupog.tar.gz\n")
    outLines.append("scram b -j 4\n")
    #if Systematics :
    #if str(args.islocal.lower()=='yes') : 
    #    outLines.append("git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools\n")
    #    outLines.append("cp ${_CONDOR_SCRATCH_DIR}/branchselection.py PhysicsTools/NanoAODTools/python/postprocessing/framework/.\n")
    #    outLines.append("cp ${_CONDOR_SCRATCH_DIR}/keep_and_drop.txt PhysicsTools/NanoAODTools/python/postprocessing/framework/.\n") 
    #    outLines.append("cd PhysicsTools/NanoAODTools\n")
    #    outLines.append("scram b -j 4\n")
    outLines.append("echo ${_CONDOR_SCRATCH_DIR}\n")
    outLines.append("cd ${_CONDOR_SCRATCH_DIR}/CMSSW_10_6_5/src/\n")
    outLines.append("cp ${_CONDOR_SCRATCH_DIR}/* .\n")
    outLines.append("ls -altrh\n")
    outLines.append("echo 'this is the working dir' ${_CONDOR_SCRATCH_DIR}\n")
    return outLines

def getFileName(line) :
    tmp = line.split()[0].strip(',')
    fileName = tmp.strip()
    return fileName


args = getArgs()
era = str(args.year)
doJME  = args.doSystematics.lower() == 'true' or args.doSystematics.lower() == 'yes' or args.doSystematics == '1'

doWeights = args.weights.lower() =='yes' or args.weights.lower()=='1' or  args.weights.lower() == 'true'

period="B"
if 'Run2016' in args.dataSet or 'Run2017' in args.dataSet or 'Run2018' in args.dataSet: 
    poss = args.dataSet.find("Run")
    period = args.dataSet[int(poss)+7:int(poss)+8]
    print 'will set up', poss, period

  

# sample query 
# dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8*/*/NANOAOD*" --limit=0   


query = '"file dataset={0:s}"'.format(args.dataSet)
if "USER" in str(args.dataSet) : query = '"file dataset={0:s}"'.format(args.dataSet+" instance=prod/phys03")
command = "dasgoclient --query={0:s} --limit=0  > fileList.txt".format(query)


#if str(args.islocal.lower())=='yes' : command ='ls  /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv7/ZH_JECs_{0:s}/CRAB_PrivateMC/{1:s}_{0:s}/*/*/*root   > fileList.txt'.format(str(args.year), args.nickName) 

whate = str(args.year)
getNt = args.nickName
if 'pre' in whate:
    whate='2016'
    getNt=args.nickName+"_preVFP"
if str(args.islocal.lower())=='yes' : command ='ls  /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/{0:s}/{1:s}/*root   > fileList.txt'.format(str(whate), getNt) 
#if str(args.islocal.lower())=='yes' or str(args.islocal.lower())=='1': command ='ls  /eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv7/JEC_{0:s}/*/{1:s}_{0:s}/*/*/*root   > fileList.txt'.format(str(args.year), args.nickName)

print("Running in {0:s} mode.  Command={1:s}".format(args.mode,command))
os.system(command)
    
files = open('fileList.txt','r').readlines()
if len(files) < 1 :
    print("***In makeCondor.py: Empty fileList.txt")
    exit()

scriptList = [] 
file=[]
dataset=[]

mjobs=args.concatenate


for nFiles, file in enumerate(files) :
     
    fileName=getFileName(file)
    if str(args.islocal.lower())=='yes' : fileName = fileName.replace('/eos/uscms','')
    if '#' not in fileName :  dataset.append(fileName)


counter=0

executable = str(args.selection)
executable=executable.replace("_T1","")
if 'ZH' in str(args.selection) : executable='ZH'

runLocal = str(args.islocal.lower())=='yes'

mjobs = 1
if runLocal : mjobs = args.concatenate
for nFile in range(0, len(dataset),mjobs) :
    #print("nFile={0:d} file[:80]={1:s}".format(nFile,file[:80]))
    fileName = getFileName(file)
    print dataset[nFile]
    #numb = dataset[nFile].split("/",11)[11]
    #numb = numb.replace(".root","")
    scriptName = "{0:s}_{1:03d}_{2:s}.sh".format(args.nickName,nFile+1, args.year)

    #scriptName = "{0:s}_{1:s}.sh".format(numb, args.year)

    print("scriptName is ={0:s}".format(scriptName))
    outLines = beginBatchScript(scriptName,doJME)

    #outLines.append("tar -zxvf SFs.tar.gz\n")
    #outLines.append("cp MCsamples_*csv MCsamples.csv\n")
    outLines.append("cp cuts_{0:s}_{1:s}.yaml cuts.yaml\n".format(args.selection, args.year))


    maxx = mjobs
    if counter+mjobs > len(dataset) : 
	#print 'should include', nFile, -nFile-mjobs + len(dataset)+1, 'from ', len(dataset), counter
	maxx = len(dataset)-counter
	#for j in range(0,mjobs) :
    for j in range(0,maxx) :
	#print 'shoud see', nFile+maxx, maxx, len(dataset)
	fileloop=dataset[nFile:nFile+maxx][j]
	#query = '"file={0:s} | grep file.nevents"'.format(fileloop)
	#command = "dasgoclient --query={0:s} ".format(query)
	#print("============>.  Command={0:s}".format(command))
	#nevts=os.system(command)
	#print 'check', os.system(command)
	#output = subprocess.check_output(os.system(command), shell=True)
	#print 'for ', fileloop, 'we have', nevts, nevts/20000

	#if 'lpcsusyhiggs' not in fileName : outLines.append("xrdcp root://cms-xrd-global.cern.ch/{0:s} inFile.root\n".format(fileloop)) 
	#else : 
	infile = "inFile.root"
        if 'Electrons' in fileloop : infile="inFileElectrons.root"
        if 'Muons' in fileloop : infile="inFileMuons.root"

        outLines.append("xrdcp root://cmsxrootd.fnal.gov/{0:s} {1:s}\n".format(fileloop, infile)) 

	outFileName = "{0:s}_{1:03d}.root".format(args.nickName,nFile+j+1)


	#if doJME : 

        weightSwitch=0
        fend = fileloop.split("all_",1)[1] 
        if 'part_1of' in fileloop and 'Electrons' not in fileloop: weightSwitch=1
	#if str(args.islocal.lower())=='yes' :  
	#    outLines.append("python {6:s}.py -f {4:s} -o {0:s} --nickName {1:s} -y {2:s} -s {3:s} -w 0 -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable))

	if doWeights and not runLocal: 
	    outLines.append("python SystWeights.py -f {4:s}  -o {0:s} --nickName {1:s} -y {2:s} -s {3:s} -w 1 -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable, str(weightSwitch)))

	if not runLocal or 'part_1of' not in fileloop: outLines.append("python {6:s}.py -f {4:s} -o {0:s} --nickName {1:s} -y {2:s} -s {3:s} -w 0 -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable, str(weightSwitch)))
	else : outLines.append("python {6:s}.py -f {4:s} -o {0:s} --nickName {1:s} -y {2:s} -s {3:s} -w  {7:s} -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable, str(weightSwitch)))
	#else : 
	#    outLines.append("python {6:s}.py -f {4:s} -o {0:s} --nickName {1:s} -y {2:s} -s {3:s} -w 0 -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable))
    
	outLines.append("rm inFile*.root\n")

        ntupfile = outFileName.replace(".root", ".ntup")
        weightsfile = outFileName.replace(".root", ".weights")
	#if doWeights or weightSwitch in fend:
	if doWeights or weightSwitch:
	    #oautLines.append("hadd -f -k all_{0:s}_{1:03d}.root {2:s} {3:s}\n".format(args.nickName,nFile+j+1, ntupfile, weightsfile))
	    #outLines.append("mv all_{0:s}_{1:03d}.root {0:s}_{1:03d}.root\n".format(args.nickName,nFile+j+1, ntupfile, weightsfile))
	    outLines.append("xrdcp {4:s} root://cmseos.fnal.gov//store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/{0:s}_{3:s}/{4:s}\n".format(args.nickName, nFile+1, executable, args.year, weightsfile))
	    outLines.append("\n")
 
	#if str(args.islocal.lower())=='no' : outLines.append("hadd -f -k all_{0:s}_{1:03d}.root *ntup *\n".format(args.nickName,nFile+1))
	#else : outLines.append("hadd -f -k all_{0:s}_{1:03d}.root *ntup \n".format(args.nickName,nFile))
	outLines.append("xrdcp {5:s} root://cmseos.fnal.gov//store/group/lpcsusyhiggs/ntuples/nAODv9/Wjets_T1/{0:s}_{3:s}/{4:s}\n".format(args.nickName, nFile+1+j, executable, args.year, fend, ntupfile))
	outLines.append("\n")

    outLines.append("rm  *root *.ntup  *.so\nrm *.pcm\nrm *cc.d\n")
    outLines.append("cd ../.. ; rm -fr CMSSW_10_6_5\n")
    #outLines.append("cp  all*root  ${_CONDOR_SCRATCH_DIR}/.\n")
    #outLines.append("cp * ${_CONDOR_SCRATCH_DIR}/.\n")
    fend = fend.replace(".root","")
    scriptName = "all_{0:s}.sh".format(fend)

    print("Writing out file = {0:s}".format(scriptName))
    open(scriptName,'w').writelines(outLines)
    scriptList.append(scriptName)
    counter += mjobs

'''

if str(args.islocal.lower())=='no': 

    mjobs = len(dataset) * (len(ptBins)-1)
    mjobs=5
    print '--------------------------=============================', 
    if len(ptBins) > 1 : mjobs = 1

    for nFile in range(0, len(dataset),mjobs) :

	for ipT in range(len(ptBins)-1):

	    pt = ptBins[ipT]
	    ptN = ptBins[ipT+1]
	    if ipT >0 : doWeights=0

	    
	    #print("nFile={0:d} file[:80]={1:s}".format(nFile,file[:80]))
	    scriptName = "{0:s}_{1:03d}_{2:s}of{3:s}.sh".format(args.nickName,nFile+1, str(ipT+1), str(len(ptBins)-1))
	    print("scriptName={0:s}".format(scriptName))
	    outLines = beginBatchScript(scriptName,doJME)

	    #outLines.append("tar -zxvf SFs.tar.gz\n")
	    outLines.append("cp MCsamples_*csv MCsamples.csv\n")
	    outLines.append("cp cuts_{0:s}.yaml cuts.yaml\n".format(args.selection))

	    fileName = getFileName(file)
	    maxx = mjobs
	    if counter+mjobs > len(dataset) : 
		#print 'should include', nFile, -nFile-mjobs + len(dataset)+1, 'from ', len(dataset), counter, maxx
		maxx = len(dataset)-counter
		#for j in range(0,mjobs) :
	    #for j in range(0,mjobs) :
            for j in range(0,maxx) :
		#print 'shoud see', nFile+maxx, maxx, len(dataset)
		#if len(dataset) == 1 :  fileloop=dataset[nFile:nFile+1][0]
		#else :  fileloop=dataset[nFile:nFile+maxx][j-1]a
                fileloop=dataset[nFile:nFile+maxx][j]
		#fileloop=dataset[nFile:nFile+maxx][j]
		if 'lpcsusyhiggs' not in fileName : outLines.append("xrdcp root://cms-xrd-global.cern.ch/{0:s} inFile.root\n".format(fileloop)) 
		else : outLines.append("xrdcp root://cmsxrootd.fnal.gov/{0:s} inFile.root\n".format(fileloop)) 

		outFileName = "{0:s}_{1:03d}.root".format(args.nickName,nFile+j)
		infile = "inFile.root"

		
		if doJME : 

		    outLines.append("sed -i 's/MIN/{0:s}/g' make_jme.py  \n".format(str(pt)))
		    outLines.append("sed -i 's/MAX/{0:s}/g'  make_jme.py \n".format(str(ptN)))


		    if ipT== 0 : outLines.append("python {6:s}.py -f {4:s} -o {0:s}_{8:s}of{9:s} --nickName {1:s} -y {2:s} -s {3:s} -w {7:s} -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable, str(doWeights),str(ipT+1), str(len(ptBins)-1)))

		    if 'Run2016' in fileloop or 'Run2017' in fileloop or 'Run2018' in fileloop : 
			outLines.append("python make_jme.py False {0:s} {1:s}\n".format(str(args.year), str(period)))
		    else : 
			outLines.append("python make_jme.py True {0:s} {1:s}\n".format(str(args.year), str(period)))

		    infile = "inFile_Skim.root"

		    outLines.append("python {6:s}.py -f {4:s} -o {0:s}_{7:s}of{8:s} --nickName {1:s} -y {2:s} -s {3:s} -w 0 -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable, str(ipT+1), str(len(ptBins)-1)))


		else : 
		    outLines.append("python {6:s}.py -f {4:s} -o {0:s} --nickName {1:s} -y {2:s} -s {3:s} -w 1 -j {5:s}\n".format(outFileName,args.nickName, args.year, args.selection,infile, args.doSystematics, executable))
	    
		outLines.append("rm inFile*.root\n")


	    outLines.append("hadd -f -k all_{0:s}_{1:03d}_{2:s}of{3:s}.root *ntup* **\n".format(args.nickName,nFile+j,str(ipT+1), str(len(ptBins)-1)))
	    outLines.append("rm *.pyc\nrm *.so\nrm *.pcm\nrm *cc.d\n")
	    #outLines.append("rm *.ntup *. *.so\nrm *.pcm\nrm *cc.d\n")
	    outLines.append("rm *ntup* *.so\nrm *.pcm\nrm *cc.d\n")
	    outLines.append("cp  all*root ${_CONDOR_SCRATCH_DIR}/.\n")
	    outLines.append("cp  ** ${_CONDOR_SCRATCH_DIR}/.\n")
	    print("Writing out file = {0:s}".format(scriptName))
	    open(scriptName,'w').writelines(outLines)
	    scriptList.append(scriptName)
	counter += mjobs
		
'''

# now that .sh files have been generated make a list of corresponding .jdl files

#dir = '/uscms_data/d3/alkaloge/ZH/CMSSW_10_2_9/src/MC/'
'''
dir = os.getenv("CMSSW_BASE")+"/src/ZH_Run2/MC/"
dirData = os.getenv("CMSSW_BASE")+"/src/ZH_Run2/data/"
funcsDir = os.getenv("CMSSW_BASE")+"/src/ZH_Run2/funcs/"
SVFitDir = os.getenv("CMSSW_BASE")+"/src/ZH_Run2/SVFit/"

dirMC = os.getcwd()+"/../../../../MC/"
dirZH = os.getcwd()+"/../../../../ZH/"
dirData = os.getcwd()+"/../../../../data/"
funcsDir = os.getcwd()+"/../../../../funcs/"
SVFitDir = os.getcwd()+"/../../../../SVFit/"
toolsDir = os.getcwd()+"/../../../../tools/"
'''

wdir='/uscms_data/d3/alkaloge/MetStudies/nAOD/CMSSW_10_6_5/src/'

dirMC = wdir+"/MC/"
dirZH = wdir+"/ZH/"
dirData = wdir+"/data/"
funcsDir = wdir+"/funcs/"
SVFitDir = wdir+"/SVFitDir/"
toolsDir = wdir+"/tools/"
pileupDir = wdir+"/pileup/"

print("dir={0:s}".format(dir))

for file in scriptList :
    base = file[:-3] 
    outLines = ['universe = vanilla\n']
    outLines.append('Executable = {0:s}\n'.format(file))
    outLines.append('Output = {0:s}.out\n'.format(base))
    outLines.append('Error = {0:s}.err\n'.format(base))
    outLines.append('Log = {0:s}.log\n'.format(base))
    #outLines.append('transfer_input_files = {0:s}ZH.py, {0:s}MC_{1:s}.root, {0:s}data_pileup_{1:s}.root, {0:s}MCsamples_{1:s}.csv, {0:s}ScaleFactor.py, {0:s}SFs.tar.gz, {0:s}cuts_{2:s}.yaml, '.format(dir,args.year, args.selection))
    outLines.append('transfer_input_files = {0:s}{1:s}.py, {0:s}SystWeights.py,'.format(dirZH,executable))
    outLines.append('{0:s}pileup_{1:s}UL_MC.root, {0:s}pileup_{1:s}UL_data.root, {0:s}cuts_{2:s}_{1:s}.yaml, '.format(dirMC,args.year, args.selection, executable))
    #outLines.append('{0:s}*txt, '.format(dirData))
    outLines.append('{0:s}tauFun2.py, {0:s}generalFunctions.py, {0:s}outTupleW.py, {0:s}outTuple2Lep.py, {0:s}Weights.py, '.format(funcsDir))
    outLines.append('{0:s}muon_Z_{1:s}.json.gz, {0:s}electron_{1:s}.json.gz\n'.format(toolsDir, args.year))
    #outLines.append('{0:s}make_jme.py, {0:s}branchselection.py, {0:s}keep_and_drop.txt, {0:s}taupog.tar.gz\n'.format(toolsDir))
    outLines.append('priority = 2\n')
    outLines.append('should_transfer_files = YES\n')
    outLines.append('when_to_transfer_output = ON_EXIT\n')
    outLines.append('x509userproxy = $ENV(X509_USER_PROXY)\n')
    outLines.append('Queue 1\n')
    open('{0:s}.jdl'.format(base),'w').writelines(outLines)


    
    
