import ROOT

def add_histograms():
    file1 = ROOT.TFile("scales_EGamma_Run2018_Gjets_Njetincl.root")
    file2 = ROOT.TFile("1.root")

    hist1 = file1.Get("Folder_3_vspt_PtGt60Lt80/h_scale_puppi_vspt_3")
    hist2 = file2.Get("Folder_3_vspt_PtGt60Lt80/h_scale_puppi_vspt_3")

    print 'hists' , hist1.GetSumOfWeights(), hist2.GetSumOfWeights()
    print 'hists' , hist1.Integral(), hist2.Integral()
    if hist1 and hist2:
        hist1.Add(hist2)
        outputFile = ROOT.TFile("output.root", "RECREATE")
        hist1.Write()
        outputFile.Close()
    else:
        print("Failed to retrieve histograms from files.")


    outputFile = ROOT.TFile("output.root", "RECREATE")
    hist1.Write()
    outputFile.Close()

if __name__ == "__main__":
    add_histograms()


