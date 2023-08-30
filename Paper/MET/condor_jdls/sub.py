import os

channels=['MuMu', 'ElEl']
channels=['ElEl']
years=['2016', '2016pre', '2017', '2018']
years=['2018']

for channel in channels:
    for year in years : 
	dir_name =channel+"_"+year
	#for dir_name in os.listdir('.'):
	if os.path.isdir(dir_name):
	    os.chdir(dir_name)  # Enter the directorya
            print 'I am in dir ...', dir_name
	    for jdl_file in os.listdir('.'):
		if jdl_file.endswith('.jdl'):
		    root_file = jdl_file.replace("jdl", "root")
		    root_file = "scales_Njeteq0_" + root_file
		    subm_file = jdl_file + ".submitted"
		    if not os.path.isfile(root_file) and not os.path.isfile(subm_file):
			os.system('condor_submit {}'.format(jdl_file))
			os.system('touch {}.submitted'.format(jdl_file))
			print('condor_submit {}'.format(jdl_file))
	    os.chdir('..')  # Go back to the parent directory




