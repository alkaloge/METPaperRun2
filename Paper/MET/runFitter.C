#include "TString.h"
#include "TSystem.h"
#include "fitter.C"
void runFitter(TString channel){
gSystem->CompileMacro("fitter.C", channel);


    //fitter("met_uPara_over_zll_pt", "met_uPara_over_qt", "q_{T} [GeV]");
    fitter("met_metx_over_nVert", "met_mety_over_nVert", "# vertices");
    //testRatioEEMuMuGJetsComparison("met_mety_over_nVert", "met_mety_over_nVert", "q_{T} [GeV]");



}

