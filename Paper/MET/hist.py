import ROOT

# Create a TH1 histogram with 4 bins
hist = ROOT.TH1F("hist", "Randomly Filled Histogram", 4, 0, 4)

# Set the random seed for reproducibility (optional)
ROOT.gRandom.SetSeed(0)

# Fill the histogram with random values
for _ in range(100):
    value = ROOT.gRandom.Uniform(0, 4)  # Generate a random value between 0 and 4
    hist.Fill(value)

# Print the content of each bin
for bin in range(1, hist.GetNbinsX() + 1):
    print("Bin {}: Content = {}, Error = {}".format(bin, hist.GetBinContent(bin), hist.GetBinError(bin)))

# Draw the histogram
canvas = ROOT.TCanvas("canvas", "Histogram Canvas")
hist.Draw()

# Show the canvas
canvas.Draw()




