# MET Performance
This repository contains the tools for making scale and resolution plots, and making data/mc comparisons for MET in gamma+jets, Z-> ee and Z->mumu.


About the framework:


    Sample location, cross sections and options for the different samples are stored in samples.dat
    
    The samples are minitrees that have the generated pu, kfactor and prescale weight distributions stored in them. These weights are later applied on an event by event basis in the getTH1F function defined in incude/Sample.py
    
    The cuts are defined in include/CutManager.py, where pretty much just the string of cuts for the leptons and th photon is defined. 
    
    The include/Canvas.py contains everything needed for the plotting. It has two functions defined, save() and saveRatio(), which makes plots without and with a ratio.


How to make data/mc comparisons:
    
    
    In met_distribution.py:
    
    Select if you want to do ee, mumu or gjets with the doDY and doEE booleans. 
    
    Select the variables you want to plot in the doVariables list
    
    For events containing any kind of met, like met, uPara and uPerp, the histograms for the jec and unclustered energy up/down variations is also generated for the error calculations

    Only stat errors are generated for the other variables such as nvert, qT etc.
    
    Run by: python met_distribution.py
    
    Plots end up in plots/


How to make scale plots:
    
    
    Relevant comments inline in met_scale_zjets.py (basically the same as for gjets)
    
    Select if you want to do ee or mumu and background subtraction or not using doEE and doBKGSubtraction
    
    When doing background subtraction, background and data histograms of the uPara are generated in bins of qT and fed to the fitting function constructModel, that subtracts the background from the data and returns the mean and the error post fit, which is filled in a tgraph. 
    
    When doBKGSubtraction = False, histograms are generated in bins of qT for just the signal mc, and fitted in the constructModel function and returns the mean and the error post fit, but this is also done for the jec and unclustered energy up/down variations which are stored with the same name of the tgraph but in different tf1s with the corresponding name of the variations
    
    The fits are stored in plots/XXXjets/scale/fit where XXX is z or gamma
    
    The final results are stored as tgraphs in tf1s, and the plotting is done separately. The reason for this is that it is easier to change the plot style of tgraphs that are already generated instead of regenerating them everytime you plot, since the fits are usually slow. 
    
    The naming convention is: the tf1s name contain the Data if doBKGSubtraction DY if not, Scale if it is Scale, Resolution if not, if doBKGSubtraction= False tehn there are also tf1s with the jec and unclustered energy up/down variations stored separately, and the end of the name specifies if it is ee or mumu. The same naming convention holds for gjets too. Inside these tf1s, the tgraphs names are the same, so the only way to differentiate them is to see what tf1 they are in.
    
    Once you have generated the tgraphs of the three different processes, both doing background subtraction and not, the plotting is done using the runPlotter.C script. In this script the first argument of the function is the name of the tgraph in zjets case, and the second argument is the name of the tgraph in the gjets case. The runPlotter.C script calls the script plotter.C where the names of the tf1s are specified. 
    
    The runPlotter.C script can plot both the scale and the resolution, but these needs to be done separately, since there is a different binning needed for the different cases, which needs to be specified on the beginning of the plotter.C script. This can probably be automated but I'm too lazy to fix this right now. 
    
    Run by .L runPlotter.C++ followed by runPlotWithRatioJES("")
    

How to make resolution plots:
    
    
    Pretty much the same procedure as the scale, but now using met_resolution_zjets.py script. 
    
    Main difference is that now the resolution can be of both the uPara and uPerp and as a function of qT, nvert and sumEt, so this needs to be specified, otherwise same procedure.  

Regarding PF/Puppi comparisons:
    
    
    The PF met Puppi met comparisons are historically done just in the case of Z->mumu, and the resolution is mainly interesting as a function of number of vertices. The script met_resolution_zjetsPuppi.py can do this for you. And it also includes a little section where we correct the scale of the pf and puppi met in the cases where it is not 1. 
    
    The plotting of the PF/Puppi comparisons of the scale and resolution is done with the runPlotterPuppi.C script. The plotting style is a bit different from the three boson comparisons, so I keep a separate script for the PF/Puppi comparison for simplicity.  

































