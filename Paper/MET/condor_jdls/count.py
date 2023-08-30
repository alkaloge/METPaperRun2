import ROOT

def print_entries(hist):
    if hist:
        print("Histogram: {}".format(hist.GetName()))
        print("Entries: {}".format(hist.GetEntries()))
        return hist.GetEntries()
    else:
        print("Histogram not found.")
        return 0

def process_directory(directory):
    entries_sum = 0
    
    for key in directory.GetListOfKeys():
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TDirectoryFile):
            print("Entering directory: {}".format(obj.GetName()))
            entries_sum += process_directory(obj)
        elif isinstance(obj, ROOT.TH1):
            hist_name = obj.GetName()
            if hist_name.startswith("h_scale_puppi_vspt_"):
                entries_sum += print_entries(obj)

    return entries_sum

def main():
    file = ROOT.TFile("scales_EGamma_Run2018_Gjets_Njetincl.root")
    file = ROOT.TFile("1.root")
    
    if file.IsOpen():
        entries_sum = 0
        for key in file.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TDirectoryFile):
                print("Processing directory: {}".format(obj.GetName()))
                entries_sum += process_directory(obj)
                
        print("Sum of entries from all histograms: {}".format(entries_sum))
        
        file.Close()
    else:
        print("File not found or could not be opened.")

if __name__ == "__main__":
    main()


