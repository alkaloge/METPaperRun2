import os

# Replace this with the path to your directory containing .sh files
sh_dir = './'

# Replace this with the path to your local directory containing scales_*root files
root_dir = './'

# List all .sh files in the directory
sh_files = [f for f in os.listdir(sh_dir) if f.endswith('.sh')]

# Initialize lists to store missing .sh and .root files along with their source .sh
missing_sh_files = []
missing_root_files = {}
total_root=0
inroot=0
# Iterate through each .sh file
for sh_file in sh_files:
    # Open the .sh file
    with open(os.path.join(sh_dir, sh_file), 'r') as file:
        # Read each line in the .sh file
        for line in file:
            # Check if the line contains a scales_*root file
            if line.strip().startswith('mv') and 'scales_' in line:
                # Extract the target root file from the mv command
                target_file = line.split()[-1]
                #print 'checking for', target_file
                inroot+=1

                # Check if the target root file exists in the local directory
                if not os.path.exists(os.path.join(root_dir, target_file)):
                    missing_root_files[target_file] = sh_file
                else  : total_root+=1

    # Check if the .sh file is missing
    if not os.path.exists(os.path.join(sh_dir, sh_file)):
        missing_sh_files.append(sh_file)

# Print missing .sh files
print("Missing .sh files:")
for missing_sh in missing_sh_files:
    print('  ', missing_sh)

# Print missing .root files and their corresponding .sh files
print("\nMissing .root files:")
for missing_root, source_sh in missing_root_files.items():
    print('  Missing', missing_root, 'from', source_sh)


print 'in total {} root files are present from {}'.format(total_root, inroot)

#for missing_root, source_sh in missing_root_files.items():
#    jdl=source_sh.replace('sh', 'jdl') 
#    print 'condor_submit ', jdl
