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
    var = "METCorGood_T1_pt"
    background_samples =['dy', 'qcd', 'top', 'ew', 'ewknlo61']
    processes=[]
    processes=['fsignal']
    for bkg in background_samples : 
        hist = 'histo_{0:s}_{1:s}'.format(bkg, var)
        processes.append(hist)
    #processes.append('data_obs')

    with open(output_file, 'w') as f:
        f.write('imax 1\n')
        f.write('jmax *\n')
        f.write('kmax *\n')
        f.write('---------------\n')
        f.write('shapes * wjets wjets.root wjets/$PROCESS wjets/$PROCESS_$SYSTEMATIC')
        f.write('---------------\n')
        f.write('bin wjets\n')
        f.write('observation {0}\n'.format(int(histograms_nominal['data'].Integral() if histograms_nominal['data'] else 0)))
        f.write('------------------------------\n')

        f.write('bin\t\t{}\n'.format('\t\t'.join(['wjets']*len(processes))))  # Repeated 'wjets' for each process
        f.write('process\t\t{}\n'.format('\t\t'.join(processes)))  # Processes from the list
        f.write('process\t\t{}\n'.format('\t\t'.join(['-1'] + [str(i) for i in range(1, len(processes) )])))  # -1 for 'fsignal', then increasing numbers for other processes
        #f.write('rate\t\t{}\n'.format('\t\t'.join([str(histograms_nominal[process].Integral() if histograms_nominal[process] else 0) for process in processes])))  # Integral values for each process

        #rate_values = ['0' if histograms_nominal[processes] is None else str(histograms_nominal[process].Integral()) for process in processes]
        #f.write('rate\t\t{}\n'.format('\t\t'.join(rate_values)))


        #f.write('bin\t\twjets\t\twjets\t\twjets\t\twjets\t\twjets\t\twjets\t\twjets\n')
        #f.write('process\t\tfsignal\t\thisto_dy_METCorGood_T1_pt\t\thisto_qcd_METCorGood_T1_pt\t\thisto_top_METCorGood_T1_pt\t\thisto_ew_METCorGood_T1_pt\t\thisto_ewknlo61_METCorGood_T1_pt\t\tdata\n')
        #f.write('process\t\t-1\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\n')
        f.write('rate\t\t{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\t\n'.format(
            histograms_nominal['fsignal'].Integral() if histograms_nominal['fsignal'] else 0,
            histograms_nominal['dy'].Integral() if histograms_nominal['dy'] else 0,
            histograms_nominal['qcd'].Integral() if histograms_nominal['qcd'] else 0,
            histograms_nominal['top'].Integral() if histograms_nominal['top'] else 0,
            histograms_nominal['ew'].Integral() if histograms_nominal['ew'] else 0,
            histograms_nominal['ewknlo61'].Integral() if histograms_nominal['ewknlo61'] else 0))
            #histograms_nominal['data'].Integral() if histograms_nominal['data'] else 0))


        f.write('------------------------------\n')
        f.write('# Systematic variations\n')

        f.write('------------------------------\n')
        f.write('# Systematic variations\n')
        f.write('norm_bkgs\tlnN\t-\t1.05\t1.1\t1.05\t1.05\t1.05\n')
        f.write('lumi\tlnN\t-\t1.016\t1.016\t1.016\t1.016\t1.016\n')
        f.write('trigger\tlnN\t-\t1.02\t1.02\t1.02\t1.02\t1.02\n')
        f.write('id\tlnN\t-\t1.02\t1.02\t1.02\t1.02\t1.02\n')
        f.write('JES\tshape\t-\t1\t1\t1\t1\t1\n')
        f.write('Unclustered\tshape\t-\t1\t1\t1\t1\t1\n')
        f.write('ID\tshape\t-\t1\t1\t1\t1\t1\n')
        f.write('PU\tshape\t-\t1\t1\t1\t1\t1\n')
        f.write('* autoMCStats 0\n')




if __name__ == "__main__":
    # Define the ROOT file and histogram names
    ROOT.gROOT.SetBatch(True)  # Prevents ROOT from trying to open a GUI
    root_file = "./Root_Wjets/plotS_Run2_njetsgt0_nbtagl_cutbased_varbins_vetolept_isolt0p15_mtmassgt80_hitslt1_METCorGood_T1_pt_ElNu.root"
    background_samples = ['tx', 'ew', 'ewknlo', 'qcdmg', 'gjets']
    background_samples =['dy', 'qcd', 'top', 'ew', 'ewknlo61']
    histograms_nominal = {}

    f = TFile.Open(root_file, "read")
    f1 = TFile.Open("wjets.root", "recreate")
    f1.cd()
    f1.mkdir("wjets")
    f1.cd("wjets")
    hd = f.Get("histo_data")
    histograms_nominal['data'] = hd
    hd.SetName("data_obs")
    signal_hist = f.Get("histo_data")
    signal_hist.Reset()
    signal_hist.SetBinContent(1,1)
    signal_hist.SetName("fsignal")
    signal_hist.SetTitle("fsignal")
    histograms_nominal['fsignal'] = signal_hist
    f1.cd("wjets")
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
                f1.cd("wjets")
                hh.Write()
            '''
        else:
            print("Warning: Histogram for sample", sample, "was not found.")
        f1.cd("wjets")
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
            f1.cd("wjets")
	    hist.Write()

    # Make dummy signal template
    f1.Close()

    # Write datacard
    output_file = "wjets_fit.txt"
    print histograms_nominal
    write_datacard(output_file, histograms_nominal, histograms_systematics)

    print("Datacard written to:", output_file)



