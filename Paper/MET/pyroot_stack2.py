import ROOT
import json
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, TMath,  SetOwnership, TColor, kYellow, kGreen, kWhite, kMagenta, kCyan, kBlue, kOrange, kTeal
import math, sys, optparse, array, time, copy

ROOT.gROOT.SetBatch(ROOT.kTRUE)
# Load the JSON data from file
with open('my_file.json', 'r') as f:
    data = json.load(f)

canvas = ROOT.TCanvas('canvas', 'canvas', 200, 100)

# Create a legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

# Create a list of colors

#colors = {'qcd': ROOT.kRed, 'top': ROOT.kGreen, 'ew': ROOT.kBlue, 'ewk': ROOT.kOrange}

colors = {'dy':kYellow, 'qcd':kMagenta, 'qcdpt':kMagenta, 'top':kBlue, 'ew':kGreen+2, 'ewk':kCyan, 'ewknlo':kCyan+1, 'ewknlo61':kCyan+1, 'ewkincl':kTeal, 'ewkincl61':kTeal-4}

canvas = ROOT.TCanvas('canvas', 'canvas')

stacks=[]
for i, entry in enumerate(data):

    # Create THStack
    label = entry['selection']
    stack = ROOT.THStack('stack_{0:s}'.format(label), '')
    # Set x-axis label
    #stack.GetXaxis().SetTitle(label)

    # Loop over each key in the entry
    for key, value in entry.items():
        if key == 'selection':
            continue
        print value, key
        # Create histogram and fill with color based on key
        hist = ROOT.TH1F(key, '', 100, 0, 1)
        hist.SetFillColor(colors[key])
        hist.Fill(value)
	if i==0 : 
	    legend.AddEntry(hist, "{0:s}".format(str(key)), 'l')

        # Add histogram to THStack
        stack.Add(hist)

    # Add THStack to list of stacks
    stacks.append(stack)

# Draw first THStack and set y-axis range
canvas.cd()
legend.Draw()
stacks[0].Draw('hist')
stacks[0].SetMaximum(10**8)

# Loop over remaining THStacks and draw them on top of each other
for stack in stacks[1:]:
    stack.Draw('hist same')

canvas.Update()
# Save canvas as PDF
canvas.SaveAs('output.pdf')
