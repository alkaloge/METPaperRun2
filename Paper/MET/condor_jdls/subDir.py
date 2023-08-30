import os
import sys
search_string = "_"
current_dir = os.getcwd()

for filename in os.listdir(current_dir):
    if filename.endswith(".jdl") and search_string in open(filename).read():
        froot = filename+".submitted"
        if not os.path.isfile(froot) :
	    os.system("condor_submit %s" % filename)
	    os.system("touch  %s.submitted" % filename)


