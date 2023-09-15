import ROOT
from ROOT import TFile, TTree, TCut, TCanvas, TGraph

# Open the ROOT files
dataFile = TFile.Open('/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/SingleMuon_Run2017E/SingleMuon_Run2017E_2017.root')
DY_MCFile = TFile.Open('/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/DYJetsToLLM50_2017/DYJetsToLLM50_2017_MuMu.root')  # Drell-Yan MC root file

# Get the TTrees from the files
dataTree = dataFile.Get('Events')  # Replace 'tree' with the name of your TTree
DY_MCTree = DY_MCFile.Get('Events')  # Replace 'tree' with the name of your TTree

# Define the cuts
cut_data = TCut(" (nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15  && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2     && fabs(q_2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]>0   && nbtagL[0]==0.0 && cat==2 )"

cut_mc = TCut(" ((nMuon[0]==2 && Flag_BadPFMuonDzFilter[0]==1 && fabs(d0_1[0])<0.045 && fabs(dZ_1[0])<0.2 && fabs(q_1[0])==1 && iso_1[0] <= .15  && fabs(d0_2[0])<0.045 && fabs(dZ_2[0])<0.2     && fabs(q_    2[0])==1 && iso_2[0] <= .15 && nPVndof[0]>4 && fabs(PVz[0])<26 && (PVy[0]*PVy[0] + PVx[0]*PVx[0])<3 && nPV[0]>2 && njets[0]>0   && nbtagL[0]==0.0 && cat==2 ) * ( weight[0]  )* fabs( weightPUtrue[0]  )* ( L1PreFiringWeight_Nom[0]  )* ( IDSF  )* ( TrigSF )* ( IsoSF  ) ) "


# Define the bins for the boson pT
bins = [0, 20, 40, 60, 80, 100]  # Adjust these values as necessary

# Prepare to fill the TGraphs
graphs_data = []

# List of MET types
met_types = ["RawMET", "MET_T1", "PuppiMET"]

# List of MC to be subtracted
#mc_subtraction_files = ['mc1.root', 'mc2.root', 'mc3.root']  # Replace with your MC file names
mc_subtraction_files = ['/eos/uscms/store/user/lpcsusyhiggs/ntuples/nAODv9/2Lep/TTTo2L2Nu_2017/TTTo2L2Nu_2017_MuMu.root"']  # Replace with your MC file names
mc_subtraction_trees = [TFile.Open(mc_file).Get('Events') for mc_file in mc_subtraction_files] 

# Loop over the bins
for i in range(len(bins)-1):
    pt_low = bins[i]
    pt_high = bins[i+1]
    cut_pt = TCut("boson_pt > %f && boson_pt <= %f" % (pt_low, pt_high))
    
    # Loop over MET types
    for met_type in met_types:
        u_par_var = met_type + "_u_par"  # Adjust these names according to your TTree structure

        # Prepare the TGraphs
        graph_data = TGraph()
        graph_mc = TGraph()
        graph_DY_mc = TGraph()  # TGraph for DY MC

        # Subtracting MC from data
        for mc_tree in mc_subtraction_trees:
            for j, event in enumerate(mc_tree):
                if cut_mc and cut_pt:
                    graph_mc.SetPoint(j, getattr(event, 'boson_pt'), getattr(event, u_par_var))
                
        # Loop over the DY MC events
        for j, event in enumerate(DY_MCTree):
            if cut_mc and cut_pt:
                graph_DY_mc.SetPoint(j, getattr(event, 'boson_pt'), getattr(event, u_par_var))

        # Loop over the data events
        for j, event in enumerate(dataTree):
            if cut_data and cut_pt:
                graph_data.SetPoint(j, getattr(event, 'boson_pt'), getattr(event, u_par_var))

        # Subtract the MC graph from the data graph
        graph_data_minus_mc = graph_data.Clone()
        graph_data_minus_mc.GetXaxis().SetTitle("Boson pT")
        graph_data_minus_mc.GetYaxis().SetTitle("{} u_par".format(met_type))
        graph_data_minus_mc.SetName("{}_{}-{}".format(met_type, pt_low, pt_high))

        for j in range(graph_mc.GetN()):
            x_mc, y_mc = ROOT.Double(0), ROOT.Double(0)
            graph_mc.GetPoint(j, x_mc, y_mc)
            for i in range(graph_data_minus_mc.GetN()):
                x_data, y_data = ROOT.Double(0), ROOT.Double(0)
                graph_data_minus_mc.GetPoint(i, x_data, y_data)
                if x_data == x_mc:
                    graph_data_minus_mc.SetPoint(i, x_data, y_data - y_mc)
        
        # Add the DY MC entries to the final TGraph
        for j in range(graph_DY_mc.GetN()):
            x_DY, y_DY = ROOT.Double(0), ROOT.Double(0)
            graph_DY_mc.GetPoint(j, x_DY, y_DY)
            graph_data_minus_mc.SetPoint(graph_data_minus_mc.GetN(), x_DY, y_DY)
        
        # Append the TGraph to the list
        graphs_data.append(graph_data_minus_mc)

# Now you can draw your TGraphs as needed
#c = TCanvas()
# Now you can save your TGraphs as needed
for i, graph in enumerate(graphs_data):
    c = TCanvas()
    graph.Draw("APL")
    if i == 0:
        c.SaveAs("my_output.pdf[")
    elif i == len(graphs_data) - 1:
        c.SaveAs("my_output.pdf]")
    else:
        c.SaveAs("my_output.pdf")




