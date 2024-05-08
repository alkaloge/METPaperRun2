import os
import subprocess
import re


def extract_paths_from_sh(file_path):
    root_files = []
    eos_paths = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("xrdcp") and 'part_' in line:
                parts = line.split()
                if len(parts) >= 3:
                    root_file = parts[1]
                    eos_path = parts[2].replace("root://cmseos.fnal.gov/", "/eos/uscms")

                    if 'part_' in root_file :
                        root_files.append(root_file)
                        eos_paths.append(eos_path)
    return root_files, eos_paths

# Main function to traverse directories and check missing files


def check_missing_files(root_dir, lookat):
    missing_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        if lookat not in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(".sh"):
                sh_file_path = os.path.join(dirpath, filename)
                root_files, eos_paths = extract_paths_from_sh(sh_file_path)
                for root_file, eos_path in zip(root_files, eos_paths):
                    if ("Electrons.root" in root_file or "Muons.root" in root_file):
                        for i in range(1, 4):
                            #print('root_file:', root_file, 'eos_path:', eos_path)
                            if not os.path.isfile(eos_path.replace("1of3", "{}of3".format(i))):
                                sh_file_path = sh_file_path.replace("1of3", "{}of3".format(i)) 
                                #print 'found one....' , eos_path.replace("1of3", "{}of3".format(i))
                                missing_files.append((root_file, eos_path.replace("1of3", "{}of3".format(i)), sh_file_path))
                                #print (root_file, eos_path.replace("1of3", "{}of3".format(i)), sh_file_path )
    #print missing_files
    return missing_files





# Main script
if __name__ == "__main__":
    current_dir = os.getcwd()
    #lookdir="DYJetsToLL_PtZ-50To100"
    lookdir="20"
    missing_files = check_missing_files(current_dir, lookdir)
    #parint 'missing files....', missing_files
    missing_files = list(set(missing_files))
    unique_entries = {}
    for root_file, eos_path, sh_file_path in missing_files:
	file_part = root_file.split("_")[3]  # Assuming "fileXXX" is the fourth part of the filename
	unique_entries[file_part] = (root_file, eos_path, sh_file_path)

    # Extract the unique entries from the dictionary
    missing_files = list(unique_entries.values())
    if missing_files:
        with open("submit_missing_jobs.sh", "w") as submit_file:
            submit_file.write("#!/bin/bash\n")
            for missing_file in missing_files:
                submit_file.write("cd {}\n".format(os.path.dirname(missing_file[2])))
                submit_file.write("condor_submit {}.jdl\n".format(os.path.splitext(os.path.basename(missing_file[2]))[0]))
                submit_file.write("cd ../\n")
        print("Commands to submit missing jobs are written to submit_missing_jobs.sh")
    else:
        print "No missing files found."

    # Summary
    print("\nSummary of .root files in .sh vs .root files on EOS:")
    for dirpath, _, filenames in os.walk(current_dir):
        if lookdir not in dirpath : continue
	sh_files = [filename for filename in filenames if filename.endswith(".sh")]
	year = os.path.basename(dirpath).split("_")[-1]  # Extract year from the current directory
	eos_folder = dirpath.replace(current_dir, "/eos/uscms/store/group/lpcsusyhiggs/ntuples/nAODv9/{}/".format(year))
        eos_folder = eos_folder.replace("_{}".format(year),"")
	eos_files = []
	if os.path.exists(eos_folder):
	    eos_files = [filename for filename in os.listdir(eos_folder) if filename.endswith(".root")]
	#print("Folder:", dirpath)
	print("  .sh files:", dirpath, len(sh_files))*2, "  .root files on EOS:", len(eos_files)
	#print("  EOS folder:", eos_folder)










