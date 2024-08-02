import ROOT

def create_efficiency_with_systematics():
    ROOT.gROOT.SetBatch(True)  # Prevents graphics from being displayed

    # Create example histograms
    passed_hist = ROOT.TH1F("passed", "Passed Events", 10, 0, 10)
    total_hist = ROOT.TH1F("total", "Total Events", 10, 0, 10)

    # Fill example histograms (replace with your actual data)
    for i in range(1, 11):
        passed_hist.Fill(i, i)  # Example: fill with the actual passed events count
        total_hist.Fill(i, 20)  # Example: fill with the total events count

    # Create TEfficiency objects for central and systematic variations
    central_efficiency = ROOT.TEfficiency(passed_hist, total_hist)

    # Create systematic variations histograms
    jes_up_passed_hist = passed_hist.Clone("jes_up_passed")
    jes_up_passed_hist.Scale(1.05)  # Example: 5% increase for JES up variation

    jes_down_passed_hist = passed_hist.Clone("jes_down_passed")
    jes_down_passed_hist.Scale(0.95)  # Example: 5% decrease for JES down variation

    # Create TEfficiency objects for systematic variations
    jes_up_efficiency = ROOT.TEfficiency(jes_up_passed_hist, total_hist)
    jes_down_efficiency = ROOT.TEfficiency(jes_down_passed_hist, total_hist)

    # Create a canvas
    canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

    # Draw the central efficiency graph
    central_efficiency_graph = central_efficiency.CreateGraph()
    central_efficiency_graph.Draw("ap")

    # Set line color for central graph
    central_efficiency_graph.SetLineColor(ROOT.kBlack)

    # Calculate systematic uncertainty variations
    jes_up_band = ROOT.TGraphAsymmErrors()
    jes_down_band = ROOT.TGraphAsymmErrors()

    for i in range(central_efficiency.GetTotalHistogram().GetNbinsX()):
        central_efficiency_value = central_efficiency.GetEfficiency(i + 1)
        jes_up_value = jes_up_efficiency.GetEfficiency(i + 1)
        jes_down_value = jes_down_efficiency.GetEfficiency(i + 1)

        jes_up_band.SetPoint(i, central_efficiency_value, i + 0.5)
        jes_down_band.SetPoint(i, central_efficiency_value, i + 0.5)

        jes_up_band.SetPointError(i, 0, 0, central_efficiency_value - jes_down_value, jes_up_value - central_efficiency_value)
        jes_down_band.SetPointError(i, 0, 0, central_efficiency_value - jes_down_value, jes_up_value - central_efficiency_value)

    # Set line and fill colors for bands
    jes_up_band.SetLineColor(ROOT.kBlue)
    jes_up_band.SetFillColor(ROOT.kBlue)

    jes_down_band.SetLineColor(ROOT.kRed)
    jes_down_band.SetFillColor(ROOT.kRed)

    # Draw the systematic bands
    jes_up_band.Draw("3 same")
    jes_down_band.Draw("3 same")

    # Draw the central efficiency graph again
    central_efficiency_graph.Draw("p same")

    canvas.SaveAs("efficiency_with_systematics.png")

if __name__ == "__main__":
    create_efficiency_with_systematics()


