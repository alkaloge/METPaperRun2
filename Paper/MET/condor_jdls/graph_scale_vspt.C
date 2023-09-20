#include "setTDRStyle.h"
#include <iostream>
#include <fstream>
#include <vector>
#include "TH1.h"


void updateHistogram(ifstream& f, TH1* h) {
    double yvalue, yerr, yvalue2, yerr2, yvalue3, yerr3;
    yvalue=yerr= yvalue2= yerr2= yvalue3= yerr3=-0.000001;
    string s;
    f >> s >> yvalue >> yerr >> yvalue2 >> yerr2 >> yvalue3 >> yerr3;
    //s >> yvalue >> yerr >> yvalue2 >> yerr2 >> yvalue3 >> yerr3;  // Read the remaining parts
    int bin = h->GetXaxis()->FindBin(s.c_str());
    h->SetBinContent(bin, yvalue); 
    h->SetBinError(bin, yerr);
}




void updateHistogram2(ifstream& f, TH1* h1, TH1* h2, TH1* h3) {
    double yvalue, yerr, yvalue2, yerr2, yvalue3, yerr3, yvalue4, yerr4;
    yvalue=yerr= yvalue2= yerr2= yvalue3= yerr3= yvalue4 = yerr4=-0.000001;
    string s;
    f >> s >> yvalue >> yerr >> yvalue2 >> yerr2 >> yvalue3 >> yerr3 >> yvalue4 >> yerr4;
    //cout<< " s "<<yvalue<<" "<<yerr<<"  "<<h1->GetName()<<endl;
    int bin1 = h1->GetXaxis()->FindBin(s.c_str());
    int bin2 = h2->GetXaxis()->FindBin(s.c_str());
    int bin3 = h3->GetXaxis()->FindBin(s.c_str());
    h1->SetBinContent(bin1, yvalue); 
    h1->SetBinError(bin1, yerr);
    h2->SetBinContent(bin2, yvalue2); 
    h2->SetBinError(bin2, yerr2);
    h3->SetBinContent(bin3, yvalue3); 
    h3->SetBinError(bin3, yerr3);
    
}


void updateHistogram22(std::ifstream& file, TH1* h1, TH1* h2, TH1* h3) {
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        std::string s;
        double yvalue, yerr, yvalue2, yerr2, yvalue3, yerr3;

        if (ss >> s >> yvalue >> yerr >> yvalue2 >> yerr2 >> yvalue3 >> yerr3) {
            int bin1 = h1->GetXaxis()->FindBin(s.c_str());
            int bin2 = h2->GetXaxis()->FindBin(s.c_str());
            int bin3 = h3->GetXaxis()->FindBin(s.c_str());

            h1->SetBinContent(bin1, yvalue);
            h1->SetBinError(bin1, yerr);
            h2->SetBinContent(bin2, yvalue2);
            h2->SetBinError(bin2, yerr2);
            h3->SetBinContent(bin3, yvalue3);
            h3->SetBinError(bin3, yerr3);
        }
    }
}




void updateHistogrampar(ifstream& f, TH1* h) {
    double yvalue, yerr, yvalue2, yerr2, yvalue3, yerr3;
    string s;
    f >> s >> yvalue >> yerr >> yvalue2 >> yerr2 >> yvalue3 >> yerr3;
    int bin = h->GetXaxis()->FindBin(s.c_str());
    h->SetBinContent(bin, yvalue2); 
    h->SetBinError(bin, yerr2);
}

void updateHistogramperp(ifstream& f, TH1* h) {
    double yvalue, yerr, yvalue2, yerr2, yvalue3, yerr3;
    string s;
    f >> s >> yvalue >> yerr >> yvalue2 >> yerr2 >> yvalue3 >> yerr3;
    int bin = h->GetXaxis()->FindBin(s.c_str());
    h->SetBinContent(bin, yvalue3); 
    h->SetBinError(bin, yerr3);
}

void addCanvasName(TCanvas* canvas) {
    // Create a TPaveText object for the canvas name
    TPaveText* canvasName = new TPaveText(0.3, 0.1, .6, .2, "NDC");
    canvasName->SetBorderSize(0);
    canvasName->SetFillColor(0);
    canvasName->SetTextAlign(22);
    canvasName->SetTextFont(42);
    canvasName->SetTextSize(0.03);
    canvasName->SetFillColorAlpha(0, 0);  // Set fill color to transparent
    TString name = TString(canvas->GetName());
    name.ReplaceAll(".pdf", "");
    canvasName->AddText(name.Data());
    canvasName->Draw();
}



void graph_scale_vspt(const std::string& vs="_vspt_", const std::string& year="2018", const std::string& channelDir="Gjets_mc_sub", const std::string& channel="MuMu", const std::string& mc_="Gjets", const std::string& njet_="eq0"){
  //setTDRStyle();
  gROOT->SetBatch(kTRUE);
  std::string extraTag="_cutbased_isocuttight";
  TCanvas *c1 =new TCanvas("c1", " ", 0, 0, 700, 800);

  c1->Range(0,0,1,1);
  c1->SetFillColor(0);
  c1->SetBorderMode(0);
  c1->SetBorderSize(2);
  c1->SetFrameBorderMode(0);
  c1->Draw();

  TLine *line = new TLine(0, 1., 500, 1.);
  line->SetLineColor(kBlack);
  line->SetLineWidth(1.);
  line->SetLineStyle(3);
  //rawmet_2018_alldata"+vs+"njetsgeq0_MuMu.txt
  //ifstream frawmc, frawpmc, ft1mc, ft1smc, fpuppimc;

  //std::string year = "2018_";
  //std::string vs = "_vspt_"; //_npv_
  //vs = "_npv_"; //_npv_
  std::string common_part = "_alldata"+vs+"njets"+njet_+"_";
  std::string common_partmc = "_"+mc_+vs+"njets"+njet_+"_";

  cout<<" will use "<<common_partmc<<" " <<common_part<<endl;
  //  rawmet_2018_dy"+vs+"njetsgeq0_MuMu.txt
  //"t1_2018_alldata_npv_njetsgeq0_2018.txt
  std::ifstream frawd("txt_"+channelDir+"/rawmet_" + year + common_part + channel + ".txt");
  std::ifstream frawpd("txt_"+channelDir+"/rawpuppi_" + year + common_part + channel + ".txt");
  std::ifstream ft1d("txt_"+channelDir+"/t1_" + year + common_part + channel + ".txt");
  std::ifstream fpuppid("txt_"+channelDir+"/puppi_" + year + common_part + channel + ".txt");

  std::ifstream frawmc("txt_"+channelDir+"/rawmet_" + year+  common_partmc + channel + ".txt");
  std::ifstream frawpmc("txt_"+channelDir+"/rawpuppi_" + year + common_partmc + channel + ".txt");
  std::ifstream ft1mc("txt_"+channelDir+"/t1_" + year+ common_partmc + channel + ".txt");
  std::ifstream ft1smc("txt_"+channelDir+"/t1smear_" + year+  common_partmc + channel + ".txt");
  std::ifstream fpuppimc("txt_"+channelDir+"/puppi_" + year+ common_partmc + channel + ".txt");

  cout <<"working on vspt ..." <<"txt_"+channelDir+"/puppi_" + year + common_part + channel + ".txt"<<endl;
  TString saveName ="scale_"+ year +mc_+"_"+ "njets"+njet_ +vs+channelDir+extraTag+".pdf";
  TString saveNamepar ="res_par_"+ year +mc_+ "_" + "njets"+njet_ +vs+channelDir+extraTag+".pdf";
  TString saveNameperp ="res_perp_"+ year +mc_+ "_" + "njets"+njet_ +vs+channelDir+extraTag+".pdf";

  string s1;
  float yvalue1, yerr1,yvalue2, yerr2,yvalue3,yerr3;
  float yvalue1d, yerr1d,yvalue2d, yerr2d,yvalue3d, yerr3d;
  //Float_t bins[] = { 50, 60, 80, 90, 100, 110, 130, 150, 175, 200, 225, 250, 275, 305, 335, 365, 400, 440, 500, 600 };

  //Float_t bins[] ;//= {0.,20.,40.,60.,80.,100.,120.,160.,200.,300.,500.};
   /*
//std::vector<Float_t> bins;
if (vs == "_vspt_")
  Float_t bins[]  = {0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.};
if (vs == "_npv_")
  Float_t bins[]  = {0., 10., 20., 30., 40., 50., 60., 70.};
*/
//std::vector<Double_t> bins;

 Float_t bins[10]; // Maximum size of the array
//0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500
    if (vs == "_vspt_")
    {
        //Float_t vspt_bins[] = {0., 20., 40., 60., 80., 100., 120., 160., 200., 300., 500.};

        //this is for Gjets, for DY that should start lower
        Float_t vspt_bins[] = {40., 60., 80., 100., 120., 160., 200., 300., 500.};
        std::copy(vspt_bins, vspt_bins + sizeof(vspt_bins) / sizeof(Float_t), bins);
    }
    if (vs == "_npv_")
    {
        Float_t npv_bins[] = {0., 10., 20., 30., 40., 50., 60., 70.};
        std::copy(npv_bins, npv_bins + sizeof(npv_bins) / sizeof(Float_t), bins);
    }




  Int_t  binnum = sizeof(bins)/sizeof(Float_t) -1;
  //Int_t binnum = bins.size() - 1;

  TH1F* hrawd = new TH1F("hrawd", "hrawd", binnum, bins);
  hrawd->GetXaxis()->SetNdivisions(1000 + binnum, kTRUE);  
  cout<<" LOOK "<<binnum<<"  "<<endl;
  //TH1F* hrawd = new TH1F("hrawd","hrawd", binnum, bins);
  TH1F* hrawpd = new TH1F("hrawpd","hrawpd", binnum, bins);
  TH1F* ht1d = new TH1F("ht1d","ht1d", binnum, bins);
  TH1F* hpuppid = new TH1F("hpuppid","hpuppid", binnum, bins);

  TH1F* hrawmc = new TH1F("hrawmc","hrawmc", binnum, bins);
  TH1F* hrawpmc = new TH1F("hrawpmc","hrawpmc", binnum, bins);
  TH1F* ht1mc = new TH1F("ht1mc","ht1mc", binnum, bins);
  TH1F* ht1smc = new TH1F("ht1smc","ht1smc", binnum, bins);
  TH1F* hpuppimc = new TH1F("hpuppimc","hpuppimc", binnum, bins);


  TH1F* hrawdpar =new TH1F("hrawdpar","hrawdpar", binnum, bins);
  TH1F* hrawpdpar =new TH1F("hrawpdpar","hrawpdpar", binnum, bins);
  TH1F* ht1dpar =new TH1F("ht1dpar","ht1dpar", binnum, bins);
  TH1F* hpuppidpar =new TH1F("hpuppidpar","hpuppidpar", binnum, bins);

  TH1F* hrawmcpar =new TH1F("hrawmcpar","hrawmcpar", binnum, bins);
  TH1F* hrawpmcpar =new TH1F("hrawpmcpar","hrawpmcpar", binnum, bins);
  TH1F* ht1mcpar =new TH1F("ht1mcpar","ht1mcpar", binnum, bins);
  TH1F* ht1smcpar =new TH1F("ht1smcpar","ht1smcpar", binnum, bins);
  TH1F* hpuppimcpar =new TH1F("hpuppimcpar","hpuppimcpar", binnum, bins);

  TH1F* hrawdperp =new TH1F("hrawdperp","hrawdperp", binnum, bins);
  TH1F* hrawpdperp =new TH1F("hrawpdperp","hrawpdperp", binnum, bins);
  TH1F* ht1dperp =new TH1F("ht1dperp","ht1dperp", binnum, bins);
  TH1F* hpuppidperp =new TH1F("hpuppidperp","hpuppidperp", binnum, bins);

  TH1F* hrawmcperp =new TH1F("hrawmcperp","hrawmcperp", binnum, bins);
  TH1F* hrawpmcperp =new TH1F("hrawpmcperp","hrawpmcperp", binnum, bins);
  TH1F* ht1mcperp =new TH1F("ht1mcperp","ht1mcperp", binnum, bins);
  TH1F* ht1smcperp =new TH1F("ht1smcperp","ht1smcperp", binnum, bins);
  TH1F* hpuppimcperp =new TH1F("hpuppimcperp","hpuppimcperp", binnum, bins);








for(int i = 0; i < binnum+1; i++){
    updateHistogram2(frawd, hrawd,hrawdpar,hrawdperp);
    updateHistogram2(frawpd, hrawpd,hrawpdpar,hrawpdperp);
    updateHistogram2(ft1d, ht1d,ht1dpar,ht1dperp);
    updateHistogram2(fpuppid, hpuppid,hpuppidpar,hpuppidperp);

    updateHistogram2(frawmc, hrawmc,hrawmcpar,hrawmcperp);
    updateHistogram2(frawpmc, hrawpmc,hrawpmcpar,hrawpmcperp);
    updateHistogram2(ft1mc, ht1mc,ht1mcpar,ht1mcperp);
    updateHistogram2(ft1smc, ht1smc,ht1smcpar,ht1smcperp);
    updateHistogram2(fpuppimc, hpuppimc,hpuppimcpar,hpuppimcperp);

/*
    updateHistogrampar(frawd, hrawdpar);
    updateHistogrampar(frawpd, hrawpdpar);
    updateHistogrampar(ft1d, ht1dpar);
    updateHistogrampar(fpuppid, hpuppidpar);

    updateHistogrampar(frawmc, hrawmcpar);
    updateHistogrampar(frawpmc, hrawpmcpar);
    updateHistogrampar(ft1mc, ht1mcpar);
    updateHistogrampar(ft1smc, ht1smcpar);
    updateHistogrampar(fpuppimc, hpuppimcpar);

    updateHistogramperp(frawd, hrawdperp);
    updateHistogramperp(frawpd, hrawpdperp);
    updateHistogramperp(ft1d, ht1dperp);
    updateHistogramperp(fpuppid, hpuppidperp);

    updateHistogramperp(frawmc, hrawmcperp);
    updateHistogramperp(frawpmc, hrawpmcperp);
    updateHistogramperp(ft1mc, ht1mcperp);
    updateHistogramperp(ft1smc, ht1smcperp);
    updateHistogramperp(fpuppimc, hpuppimcperp);
*/
}
  TGraphErrors* grrawmc = new TGraphErrors(hrawmc);
  TGraphErrors* grrawd = new TGraphErrors(hrawd);

  TGraphErrors* grrawpmc = new TGraphErrors(hrawpmc);
  TGraphErrors* grrawpd = new TGraphErrors(hrawpd);

  TGraphErrors* grt1mc = new TGraphErrors(ht1mc);
  TGraphErrors* grt1d = new TGraphErrors(ht1d);

  TGraphErrors* grpuppimc = new TGraphErrors(hpuppimc);
  TGraphErrors* grpuppid = new TGraphErrors(hpuppid);

  TGraphErrors* grt1smc = new TGraphErrors(ht1smc);

//par
  TGraphErrors* grrawdpar = new TGraphErrors(hrawdpar);
  TGraphErrors* grrawpdpar = new TGraphErrors(hrawpdpar);

  TGraphErrors* grt1dpar = new TGraphErrors(ht1dpar);
  TGraphErrors* grpuppidpar = new TGraphErrors(hpuppidpar);

  TGraphErrors* grrawmcpar = new TGraphErrors(hrawmcpar);
  TGraphErrors* grrawpmcpar = new TGraphErrors(hrawpmcpar);
  TGraphErrors* grt1mcpar = new TGraphErrors(ht1mcpar);
  TGraphErrors* grt1smcpar = new TGraphErrors(ht1smcpar);
  TGraphErrors* grpuppimcpar = new TGraphErrors(hpuppimcpar);
 //perp
  TGraphErrors* grrawdperp = new TGraphErrors(hrawdperp);
  TGraphErrors* grrawpdperp = new TGraphErrors(hrawpdperp);

  TGraphErrors* grt1dperp = new TGraphErrors(ht1dperp);
  TGraphErrors* grpuppidperp = new TGraphErrors(hpuppidperp);

  TGraphErrors* grrawmcperp = new TGraphErrors(hrawmcperp);
  TGraphErrors* grrawpmcperp = new TGraphErrors(hrawpmcperp);
  TGraphErrors* grt1mcperp = new TGraphErrors(ht1mcperp);
  TGraphErrors* grt1smcperp = new TGraphErrors(ht1smcperp);
  TGraphErrors* grpuppimcperp = new TGraphErrors(hpuppimcperp);



  //response
  grrawmc->SetTitle("");
  grrawmc->SetMarkerStyle(8);
  grrawmc->SetMarkerSize(0.8);
  grrawmc->SetMarkerColor(kBlue);
  grrawmc->SetLineColor(kBlue);
  grrawmc->SetLineWidth(2);

  grrawd->SetTitle("");
  grrawd->SetMarkerStyle(9);
  grrawd->SetMarkerSize(0.8);
  grrawd->SetMarkerColor(kBlue);
  grrawd->SetLineColor(kBlue);
  grrawd->SetLineWidth(2);
  grrawd->SetLineStyle(2);

  grrawd->GetXaxis()->SetTitle("q_{T} [GeV]");
  grrawd->GetXaxis()->SetRangeUser(0, 500);
  //if (mc_=="Gjets") { grrawd->GetXaxis()->SetRangeUser(40, 300);}
  if (vs =="_npv_") { 
        grrawd->GetXaxis()->SetRangeUser(0, 70);
        grrawd->GetXaxis()->SetTitle("Nvtx ");
   }
  grrawd->GetXaxis()->SetTitleSize(0.04);

  grrawd->GetYaxis()->SetTitle("- <u_{||}>/<q_{T}>");
  grrawd->GetYaxis()->SetRangeUser(0.0, 1.4);
  grrawd->GetYaxis()->SetTitleSize(0.04);
  grrawd->GetYaxis()->SetTitleOffset(1.2);

  grrawpd->SetTitle("");
  grrawpd->SetMarkerStyle(8);
  grrawpd->SetMarkerSize(0.8);
  grrawpd->SetMarkerColor(kTeal);
  grrawpd->SetLineColor(kTeal);
  grrawpd->SetLineWidth(2);
  grrawpd->SetLineStyle(2);

  grrawpmc->SetTitle("");
  grrawpmc->SetMarkerStyle(8);
  grrawpmc->SetMarkerSize(0.8);
  grrawpmc->SetMarkerColor(kTeal-2);
  grrawpmc->SetLineColor(kTeal-2);
  grrawpmc->SetLineWidth(2);


  grt1mc->SetTitle("");
  grt1mc->SetMarkerStyle(8);
  grt1mc->SetMarkerSize(0.8);
  grt1mc->SetMarkerColor(kRed);
  grt1mc->SetLineColor(kRed);
  grt1mc->SetLineWidth(2);
  grt1smc->SetTitle("");

  grt1smc->SetMarkerStyle(3);
  grt1smc->SetMarkerSize(0.8);
  grt1smc->SetMarkerColor(kRed-2);
  grt1smc->SetLineColor(kRed-2);
  grt1smc->SetLineWidth(1);

  grt1d->SetTitle("");
  grt1d->SetMarkerStyle(9);
  grt1d->SetMarkerSize(0.8);
  grt1d->SetMarkerColor(kRed);
  grt1d->SetLineColor(kRed);
  grt1d->SetLineWidth(2);
  grt1d->SetLineStyle(2);

  grpuppimc->SetTitle("");
  grpuppimc->SetMarkerStyle(8);
  grpuppimc->SetMarkerSize(0.8);
  grpuppimc->SetMarkerColor(kGreen);
  grpuppimc->SetLineColor(kGreen);
  grpuppimc->SetLineWidth(2);

  grpuppid->SetTitle("");
  grpuppid->SetMarkerStyle(9);
  grpuppid->SetMarkerSize(0.8);
  grpuppid->SetMarkerColor(kGreen);
  grpuppid->SetLineColor(kGreen);
  grpuppid->SetLineWidth(2);
  grpuppid->SetLineStyle(2);



  grrawd->Draw("apz");
  grt1mc->Draw("pez same");
  grrawmc->Draw("pez same");
  grrawpmc->Draw("pez same");
  grrawpd->Draw("pez same");
  grt1d->Draw("pez same");
  grt1smc->Draw("pez same");
  grpuppid->Draw("pez same");
  grpuppimc->Draw("pez same");
  //line->Draw("same");


  TLegend *legend1 = new TLegend(0.35, 0.2, 0.85, 0.4);
  legend1->SetTextFont(42);
  legend1->SetLineColor(0);
  legend1->SetTextSize(0.028);
  legend1->SetFillColor(0);
  legend1->SetNColumns(2);

  if (mc_ == "dy" || mc_=="Gjets") {
  legend1->AddEntry(grrawmc, "Raw PF MC", "lp");
  legend1->AddEntry(grrawd, "Raw PF Data", "lp");
  legend1->AddEntry(grrawpmc, "Raw PUPPI MC", "lp");
  legend1->AddEntry(grrawpd, "Raw PUPPI Data", "lp");
  legend1->AddEntry(grt1mc, "PF T1 MC", "lp");
  legend1->AddEntry(grt1d, "PF T1 Data", "lp");
  legend1->AddEntry(grpuppimc, "PUPPI MC", "lp");
  legend1->AddEntry(grpuppid, "PUPPI Data", "lp");
  legend1->AddEntry(grt1smc, "PF T1Smear MC", "lp");
}
/*
  if (mc_ == "dynlo" ) {
  legend1->AddEntry(grrawmc, "Raw MC@nlo", "lp");
  legend1->AddEntry(grt1mc, "T1 MC@nlo", "lp");
  legend1->AddEntry(grt1smc, "T1Smear MC@nlo", "lp");
  legend1->AddEntry(grpuppimc, "Puppi MC@nlo", "lp");
}
*/
  legend1->Draw("same");

  //TLatex *t2a = new TLatex(0.5,0.9," #bf{CMS} #it{Preliminary}          16.97 fb^{-1} (13 TeV, 2016postFVP) ");
  TLatex *t2a ;//
  TLatex *t2b ;//
  if (year =="2018") { t2a= new TLatex(0.7,0.9,"2018 - 59.83 fb^{-1} (13 TeV) ");}
  if (year=="2017") {t2a = new TLatex(0.7,0.9,"2017 - 41.48 fb^{-1} (13 TeV) ");}
  if (year=="2016") {t2a = new TLatex(0.7,0.9,"2016postVFP - 16.15 fb^{-1} (13 TeV) ");}
  if (year=="2016all") {t2a = new TLatex(0.7,0.9,"2016 - 35.93 fb^{-1} (13 TeV) ");}
  if (year=="2016preVFP") {t2a = new TLatex(0.7,0.9,"2016preVFP - 19.72 fb^{-1} (13 TeV) ");}
  t2b = new TLatex(0.3,0.8," #bf{CMS} #it{Preliminary}");
  t2a->SetNDC();
  t2a->SetTextFont(42);
  t2a->SetTextSize(0.035);
  t2a->SetTextAlign(20);
  //t2a->SetTextAlign(31+32);
  t2a->Draw("same");
  t2b->SetNDC();
  t2b->SetTextFont(42);
  t2b->SetTextSize(0.04);
  t2b->SetTextAlign(20);
  t2b->Draw("same");

  c1->SetName(saveName);
  addCanvasName(c1);
  c1->SaveAs(saveName);

  TCanvas *c2 =new TCanvas("c2", " ", 0, 0, 700, 800);

  c2->Range(0,0,1,1);
  c2->SetFillColor(0);
  c2->SetBorderMode(0);
  c2->SetBorderSize(2);
  c2->SetFrameBorderMode(0);
  c2->Draw();

  c2->cd();
  grrawmcpar->SetTitle("");
  grrawmcpar->SetMarkerStyle(8);
  grrawmcpar->SetMarkerSize(0.8);
  grrawmcpar->SetMarkerColor(kBlue);
  grrawmcpar->SetLineColor(kBlue);
  grrawmcpar->SetLineWidth(2);

  grrawdpar->SetTitle("");
  grrawdpar->SetMarkerStyle(9);
  grrawdpar->SetMarkerSize(0.8);
  grrawdpar->SetMarkerColor(kBlue);
  grrawdpar->SetLineColor(kBlue);
  grrawdpar->SetLineWidth(2);
  grrawdpar->SetLineStyle(2);

  grrawdpar->GetXaxis()->SetTitle("q_{T} [GeV]");
  //grrawdpar->GetXaxis()->SetRangeUser(0, 300);
  if (vs =="_npv_") { grrawdpar->GetXaxis()->SetRangeUser(0, 70);
        grrawdpar->GetXaxis()->SetTitle("Nvtx ");

  }
  grrawdpar->GetXaxis()->SetTitleSize(0.04);

  grrawdpar->GetYaxis()->SetTitle("#sigma (u_{||}  )[GeV]");
  grrawdpar->GetYaxis()->SetRangeUser(0., 70);
  grrawdpar->GetYaxis()->SetTitleSize(0.04);
  grrawdpar->GetYaxis()->SetTitleOffset(1.2);


  grt1mcpar->SetTitle("");
  grt1mcpar->SetMarkerStyle(8);
  grt1mcpar->SetMarkerSize(0.8);
  grt1mcpar->SetMarkerColor(kRed);
  grt1mcpar->SetLineColor(kRed);
  grt1mcpar->SetLineWidth(2);
  grt1smcpar->SetTitle("");
  grt1smcpar->SetMarkerStyle(8);
  grt1smcpar->SetMarkerSize(0.8);
  grt1smcpar->SetMarkerColor(kRed-2);
  grt1smcpar->SetLineColor(kRed-2);
  grt1smcpar->SetLineWidth(2);

  grt1dpar->SetTitle("");
  grt1dpar->SetMarkerStyle(9);
  grt1dpar->SetMarkerSize(0.8);
  grt1dpar->SetMarkerColor(kRed);
  grt1dpar->SetLineColor(kRed);
  grt1dpar->SetLineWidth(2);
  grt1dpar->SetLineStyle(2);

  grpuppimcpar->SetTitle("");
  grpuppimcpar->SetMarkerStyle(8);
  grpuppimcpar->SetMarkerSize(0.8);
  grpuppimcpar->SetMarkerColor(kGreen);
  grpuppimcpar->SetLineColor(kGreen);
  grpuppimcpar->SetLineWidth(2);

  grpuppidpar->SetTitle("");
  grpuppidpar->SetMarkerStyle(9);
  grpuppidpar->SetMarkerSize(0.8);
  grpuppidpar->SetMarkerColor(kGreen);
  grpuppidpar->SetLineColor(kGreen);
  grpuppidpar->SetLineWidth(2);
  grpuppidpar->SetLineStyle(2);



  grrawdpar->Draw("apz");
  grrawmcpar->Draw("pez same");
  grt1dpar->Draw("pez same");
  grt1mcpar->Draw("pez same");
  grt1smcpar->Draw("pez same");
  grpuppidpar->Draw("pez same");
  grpuppimcpar->Draw("pez same");

  line->Draw("same");
  //if (vs == "_vspt_") { 
   legend1->SetY1(0.65);
  //legend1->SetX2(0.5);
  legend1->SetY2(0.85);
//}
  legend1->Draw("same");

  t2a->Draw("same");
  c2->SetName(saveNamepar);
  addCanvasName(c2);
  c2->SaveAs(saveNamepar);


  TCanvas *c3 =new TCanvas("c3", " ", 0, 0, 700, 800);

  c3->Range(0,0,1,1);
  c3->SetFillColor(0);
  c3->SetBorderMode(0);
  c3->SetBorderSize(2);
  c3->SetFrameBorderMode(0);
  c3->Draw();


  c3->cd();
  grrawmcperp->SetTitle("");
  grrawmcperp->SetMarkerStyle(8);
  grrawmcperp->SetMarkerSize(0.8);
  grrawmcperp->SetMarkerColor(kBlue);
  grrawmcperp->SetLineColor(kBlue);
  grrawmcperp->SetLineWidth(2);

  grrawdperp->SetTitle("");
  grrawdperp->SetMarkerStyle(9);
  grrawdperp->SetMarkerSize(0.8);
  grrawdperp->SetMarkerColor(kBlue);
  grrawdperp->SetLineColor(kBlue);
  grrawdperp->SetLineWidth(2);
  grrawdperp->SetLineStyle(2);

  grrawdperp->GetXaxis()->SetTitle("q_{T} [GeV]");
  //grrawdperp->GetXaxis()->SetRangeUser(0, 300);
  if (vs =="_npv_") { grrawdperp->GetXaxis()->SetRangeUser(0, 70);

        grrawdperp->GetXaxis()->SetTitle("Nvtx ");

  }
  grrawdperp->GetXaxis()->SetTitleSize(0.04);

  grrawdperp->GetYaxis()->SetTitle("#sigma (u_{#perp}  )[GeV]");
  grrawdperp->GetYaxis()->SetRangeUser(0., 70);
  grrawdperp->GetYaxis()->SetTitleSize(0.04);
  grrawdperp->GetYaxis()->SetTitleOffset(1.3);


  grt1mcperp->SetTitle("");
  grt1mcperp->SetMarkerStyle(8);
  grt1mcperp->SetMarkerSize(0.8);
  grt1mcperp->SetMarkerColor(kRed);
  grt1mcperp->SetLineColor(kRed);
  grt1mcperp->SetLineWidth(2);
  grt1smcperp->SetTitle("");
  grt1smcperp->SetMarkerStyle(8);
  grt1smcperp->SetMarkerSize(0.8);
  grt1smcperp->SetMarkerColor(kRed-2);
  grt1smcperp->SetLineColor(kRed-2);
  grt1smcperp->SetLineWidth(2);

  grt1dperp->SetTitle("");
  grt1dperp->SetMarkerStyle(9);
  grt1dperp->SetMarkerSize(0.8);
  grt1dperp->SetMarkerColor(kRed);
  grt1dperp->SetLineColor(kRed);
  grt1dperp->SetLineWidth(2);
  grt1dperp->SetLineStyle(2);

  grpuppimcperp->SetTitle("");
  grpuppimcperp->SetMarkerStyle(8);
  grpuppimcperp->SetMarkerSize(0.8);
  grpuppimcperp->SetMarkerColor(kGreen);
  grpuppimcperp->SetLineColor(kGreen);
  grpuppimcperp->SetLineWidth(2);

  grpuppidperp->SetTitle("");
  grpuppidperp->SetMarkerStyle(9);
  grpuppidperp->SetMarkerSize(0.8);
  grpuppidperp->SetMarkerColor(kGreen);
  grpuppidperp->SetLineColor(kGreen);
  grpuppidperp->SetLineWidth(2);
  grpuppidperp->SetLineStyle(2);




  grrawdperp->Draw("apz");
  grrawmcperp->Draw("pez same");
  grt1dperp->Draw("pez same");
  grt1mcperp->Draw("pez same");
  grt1smcperp->Draw("pez same");
  grpuppidperp->Draw("pez same");
  grpuppimcperp->Draw("pez same");

  line->Draw("same");
  //legend1->SetX1(0.3);
  //if (vs == "_vspt_") { 
   legend1->SetY1(0.65);
  //legend1->SetX2(0.5);
  legend1->SetY2(0.85);
  //}
  legend1->Draw("same");

  t2a->Draw("same");
  c3->SetName(saveNameperp);
  addCanvasName(c3);
  c3->SaveAs(saveNameperp);




















}



