import ROOT
from ROOT import TFile
def read_histogram(root_file, histogram_name):
    """
    Read a histogram from a ROOT file.
    """
    f = TFile.Open(root_file, "read")
    hist = f.Get(str(histogram_name))
    if hist:
        hist.SetName(histogram_name)
        hist2 = hist.Clone(str(histogram_name))
        hist2.SetName(histogram_name)
        print 'hist ->', hist.Integral(),  histogram_name, hist.GetName(), 'hist2', hist2.GetName(), hist2.Integral()
        #f2 = TFile.Open("dummy.root", "update")
        #f2.cd()
        #hist2.Write()
        #f2.Close()
    f.Close()
    return hist2

def write_datacard(output_file, histograms_nominal, histograms_systematics):
    """
    Write histograms into a datacard.
    """
    with open(output_file, 'w') as f:
        f.write('imax 1\n')
        f.write('jmax *\n')
        f.write('kmax *\n')
        f.write('---------------\n')
        f.write('bin 1\n')
        f.write('observation {0}\n'.format(int(histograms_nominal['data'].Integral() if histograms_nominal['data'] else 0)))
        f.write('------------------------------\n')
        f.write('bin\t\t1\t\t1\t\t1\t\t1\t\t1\t\t1\n')
        f.write('process\t\tfsignal\t\ttx\t\tew\t\tewknlo\t\tqcdmg\t\tgjets\t\tdata\n')
        f.write('process\t\t0\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\n')
        f.write('rate\t\t{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\t\t{6}\n'.format(
            histograms_nominal['fsignal'].Integral() if histograms_nominal['fsignal'] else 0,
            histograms_nominal['tx'].Integral() if histograms_nominal['tx'] else 0,
            histograms_nominal['ew'].Integral() if histograms_nominal['ew'] else 0,
            histograms_nominal['ewknlo'].Integral() if histograms_nominal['ewknlo'] else 0,
            histograms_nominal['qcdmg'].Integral() if histograms_nominal['qcdmg'] else 0,
            histograms_nominal['gjets'].Integral() if histograms_nominal['gjets'] else 0,
            histograms_nominal['data'].Integral() if histograms_nominal['data'] else 0))
        f.write('------------------------------\n')
        f.write('# Systematic variations\n')
        for sample in histograms_systematics:
            if sample != 'data':
                for variation in histograms_systematics[sample]:
                    f.write('{0}\tshape\t1\t{1}\n'.format(sample, variation))
        f.write('* autoMCStats 0\n')
        f.write('------------------------------\n')
        f.write('# Uncertainties\n')
        f.write('# List your systematics here\n')



if __name__ == "__main__":
    # Define the ROOT file and histogram names
    ROOT.gROOT.SetBatch(True)  # Prevents ROOT from trying to open a GUI
    root_file = "your_file.root"
    background_samples = ['tx', 'ew', 'ewknlo', 'qcdmg', 'gjets']
    histograms_nominal = {}

    f = TFile.Open(root_file, "read")
    f1 = TFile.Open("test.root", "recreate")
    f1.cd()
    f1.mkdir("Gjets")
    f1.cd("Gjets")
    hd = f.Get("histo_data")
    histograms_nominal['data'] = hd
    hd.SetName("data_obs")
    signal_hist = f.Get("histo_data")
    signal_hist.Reset()
    signal_hist.SetBinContent(1,1)
    signal_hist.SetName("fsignal")
    signal_hist.SetTitle("fsignal")
    histograms_nominal['fsignal'] = signal_hist
    f1.cd("Gjets")
    hd.Write()
    signal_hist.Write()
    #signal_hist.Write()
    print histograms_nominal, histograms_nominal['fsignal'].Integral(), signal_hist.Integral()

    # Read nominal histograms for each background sample
    for sample in background_samples:
        histogram_name = 'histo_' + sample + '_METCorGood_T1_pt'
	hist = f.Get(str(histogram_name))
	if hist:
	    hist.SetName(histogram_name)
            histograms_nominal[sample] = hist
            '''
            if 'gjets' in sample:
                hh = hist.Clone()
                hh.Reset()
                hh.SetBinContent(1,1)
                hh.SetName('s')
                f1.cd("Gjets")
                hh.Write()
            '''
        else:
            print("Warning: Histogram for sample", sample, "was not found.")
        f1.cd("Gjets")
        hist.Write()

    # Read systematic variation histograms for each background sample
    histograms_systematics = {}
    for sample in background_samples:
        histograms_systematics[sample] = {}
        #for variation in ['JERUp', 'JERDown', 'JESUp', 'JESDown']:
        for variation in ['UnclusteredUp','UnclusteredDown', 'JESUp', 'JESDown', 'IDUp', 'IDDown', 'PUUp', 'PUDown']:
            histogram_name = 'histo_' + sample + '_METCorGood_T1_pt' + variation
            histogram_namee = 'histo_' + sample + '_METCorGood_T1_pt' + '_'+variation
            #hist = read_histogram(root_file, histogram_name)
	    hist = f.Get(str(histogram_name))
            hist.SetName(str(histogram_namee))
            if hist:
                histograms_systematics[sample][variation] = hist
            else:
                print("Warning: Histogram for sample", sample, "with variation", variation, "was not found.")
            f1.cd("Gjets")
	    hist.Write()

    # Make dummy signal template
    f1.Close()

    # Write datacard
    output_file = "output_datacard.txt"
    print histograms_nominal
    write_datacard(output_file, histograms_nominal, histograms_systematics)

    print("Datacard written to:", output_file)



