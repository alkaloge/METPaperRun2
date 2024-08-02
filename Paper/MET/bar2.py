import ROOT
import json
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath,  SetOwnership, TColor, kYellow, kGreen, kWhite, kMagenta, kCyan, kBlue, kOrange, kTeal
# Read in JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Set up canvas and axis ranges
canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)
xmin = 0.5
xmax = len(data) + 0.5
ymin = 0
ymax = 100
colors = {'dy':kYellow, 'qcd':kMagenta, 'qcdpt':kMagenta, 'top':kBlue, 'ew':kGreen+2, 'ewk':kCyan, 'ewknlo':kCyan+1, 'ewknlo61':kCyan+1, 'ewkincl':kTeal, 'ewkincl61':kTeal-4}
# Create THStacks and fill with histograms
stacks = []
for i, entry in enumerate(data):
    print i, entry
    name = "stack{0:s}".format(str(i))
    title = "Stack {0:s}".format(str(i+1))
    stack = ROOT.THStack(name, title)
    for cat in entry.keys():
        if cat == "selection":
            continue
        histo = ROOT.TH1F(cat, cat, 1, i, i+1)
        print 'histo', cat, i, i+1, 'setBincontent as well'
        histo.SetBinContent(i+1, entry[cat])
        #histo.SetFillColor(colors[cat])
        histo.SetFillColorAlpha(colors[cat],0.5)
        stack.Add(histo)
    stacks.append(stack)

print len(stacks)

canvas.cd()
print len(stacks), stacks
# Draw the THStacks on the canvas
for i, stack in enumerate(stacks):
    #hist = stack.GetHistogram()
    hist_list = stack.GetHists()
    print hist_list[0].GetNbinsX()
    #for ii in range(1, hist.GetNbinsX()+1): print("Bin {}: {}".format(ii, hist.GetBinContent(ii)))
    if i==0 : stack.Draw("hist")
    else : stack.Draw("hist same")
    #stack.GetXaxis().SetRangeUser(xmin, xmax)
    stack.SetTitle(data[i]["selection"])

# Set y-axis range
canvas.Modified()
canvas.GetFrame().SetBorderSize(12)
canvas.GetFrame().SetFillColor(ROOT.kWhite)
canvas.GetFrame().SetFillStyle(0)
canvas.Range(xmin, ymin, 4, ymax)
canvas.SetFillColor(ROOT.kWhite)
canvas.SetBorderMode(0)
canvas.SetBorderSize(2)
canvas.SetTickx(1)
canvas.SetTicky(1)
canvas.SetLeftMargin(0.12)
canvas.SetRightMargin(0.12)
canvas.SetTopMargin(0.08)
canvas.SetBottomMargin(0.12)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.Update()
canvas.SaveAs("stacks.png")


