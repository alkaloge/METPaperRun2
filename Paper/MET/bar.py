import ROOT
import json

with open("data.json") as f:
    data = json.load(f)

color_dict = {'top': 'blue', 'dy': 'red', 'qcd': 'green', 'ewk': 'orange', 'ew': 'purple'}
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
stacks = []
for entry in data:
    histo = ROOT.THStack(entry["selection"], entry["selection"])
    for cat, value in entry.items():
        if cat == "selection":
            continue
        histo_aux = ROOT.TH1F(cat, cat, 1, 0, 1)
        histo_aux.SetBinContent(1, value)
        #histo_aux.SetFillColor(int(color_dict[cat]))
        histo.Add(histo_aux)
    stacks.append(histo)

stacks[0].Draw("hist")
stacks[0].GetXaxis().SetTitle("Stack 1")
stacks[0].GetYaxis().SetTitle("Counts")
stacks[1].Draw("hist same")
stacks[1].GetXaxis().SetTitle("Stack 2")
stacks[1].GetYaxis().SetTitle("Counts")

legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(stacks[0], stacks[0].GetTitle(), "f")
legend.AddEntry(stacks[1], stacks[1].GetTitle(), "f")
legend.Draw()

canvas.Update()
canvas.SaveAs("histos.png")


