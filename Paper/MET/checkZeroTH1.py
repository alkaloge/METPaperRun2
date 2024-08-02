
import os
import ROOT

def find_empty_histograms(directory):
    empty_histograms = []
    error_files = []

    # Loop over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".root") and '2016pre' in filename:
            filepath = os.path.join(directory, filename)
            try:
                root_file = ROOT.TFile.Open(filepath)

                if root_file and root_file.IsOpen():
                    # Loop over all keys in the file
                    for key in root_file.GetListOfKeys():
                        obj = key.ReadObj()
                        # Check if the object is a TH1 (1D, 2D, or 3D histograms)
                        if isinstance(obj, ROOT.TH1):
                            if obj.Integral() == 0:
                                empty_histograms.append((filepath, obj.GetName()))
                    root_file.Close()
                else:
                    error_files.append((filepath, "Failed to open or read the file"))
            except Exception as e:
                error_files.append((filepath, str(e)))

    return empty_histograms, error_files

# Directory containing .root files
directory = "/path/to/your/root/files"
directory = "Jobs_wjets_cutbased/"

empty_histograms, error_files = find_empty_histograms(directory)

# Print out the empty histograms
for filepath, hist_name in empty_histograms:
    #print("File: {}, Histogram: {}".format(filepath, hist_name))
    print("rm  {}".format(filepath))

# Write the error files and rm commands to a text file
#os.system("rm error_files.sh")
with open("error_files.sh", "w") as error_file:
    for filepath, error_msg in error_files:
        #error_file.write("Error with file: {}, Error: {}\n".format(filepath, error_msg))
        error_file.write("rm {}\n".format(filepath))

print("Error log written to error_files.sh")



