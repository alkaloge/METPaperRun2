import os

directory = "./"
old_substring = "nbtagl"
new_substring = "nbtagl"

# Get a list of all files in the directory
file_list = os.listdir(directory)

# Iterate through each file
for filename in file_list:
    if old_substring in filename:
        # Create the new filename by replacing the substring
        new_filename = filename.replace(old_substring, new_substring)
        
        # Construct the full paths for the old and new filenames
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_path, new_path)
        print "Renamed: {} -> {}".format(filename, new_filename)


