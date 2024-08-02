
import ROOT as root
import sys
import math
from array import array


global etaLabel


class SFs():
    def __init__(self):
        # initialize your global vars instead as
        global eff_dataH  # = root.std.map("string", root.TGraphAsymmErrors)()
        global eff_mcH  # = root.std.map("string", root.TGraphAsymmErrors)()
        global inputRootFile

    def ScaleFactor(self, inputFile):
        self.inputRootFile = str(inputFile)
        self.eff_dataH = root.std.map("string", root.TGraphAsymmErrors)()
        self.eff_mcH = root.std.map("string", root.TGraphAsymmErrors)()
        EtaBins = []
        if "Mu" in str(inputFile):
            EtaBins = ["Lt0p9", "0p9to1p2", "1p2to2p1", "Gt2p1"]
        if "El" in str(inputFile):
            EtaBins = [
                "Lt1p0",
                "1p0to1p48",
                "1p48to1p65",
                "1p65to2p1",
                "Gt2p1"]

        print('Opening ScaleFactors file', inputFile)
        self.fileIn = root.TFile(self.inputRootFile, "read")
        print('=====================================================')
        self.fileIn.ls()
        HistoBaseName = "ZMassEta"
        self.etaBinsH = self.fileIn.Get("etaBinsH")
        nEtaBins = int(self.etaBinsH.GetNbinsX())
        # print "EtaBins...........",nEtaBins, len(EtaBins)
        for iBin in range(0, nEtaBins):
            etaLabel = EtaBins[iBin]
            GraphName = HistoBaseName + etaLabel + "_Data"
            # print GraphName,etaLabel

            self.eff_dataH[etaLabel] = self.fileIn.Get(str(GraphName))
            self.SetAxisBins(self.eff_dataH[etaLabel])

            GraphName = HistoBaseName + etaLabel + "_MC"
            self.eff_mcH[etaLabel] = self.fileIn.Get(str(GraphName))
            self.SetAxisBins(self.eff_mcH[etaLabel])

            # print "some checks.................",self.eff_mcH[etaLabel].GetXaxis().GetNbins(),self.eff_dataH[etaLabel].GetXaxis().GetNbins(),"etaLabel",etaLabel,self.eff_dataH[etaLabel].GetN(),"eff_mcH.GetN()",self.eff_mcH[etaLabel].GetN()
            # print "just get some value",self.eff_mcH[etaLabel].GetX()[5],"for
            # etaLabel",etaLabel

    def SetAxisBins(self, graph):
        NPOINTS = graph.GetN()
        AXISBINSS = array('d')
        for i in range(0, NPOINTS):
            AXISBINSS.append(graph.GetX()[i] - graph.GetErrorXlow(i))

        AXISBINSS.append(
            graph.GetX()[
                NPOINTS -
                1] +
            graph.GetErrorXhigh(
                NPOINTS -
                1))

        graph.GetXaxis().Set(int(NPOINTS), AXISBINSS)

    def get_ScaleFactor(self, pt, eta):
        efficiency_data = self.get_EfficiencyData(pt, eta)
        efficiency_mc = self.get_EfficiencyMC(pt, eta)
        if efficiency_mc != 0.:
            SF = float(efficiency_data) / float(efficiency_mc)
        else:
            SF = 1.

        # print "ScaleFactor::get_ScaleFactor(double pt, double eta) Scale
        # Factor set to",SF,self.efficiency_data,self.efficiency_mc
        return SF

    def get_EfficiencyMC(self, pt, eta):
        eta = math.fabs(eta)
        label = str(self.FindEtaLabel(eta))
        binNumber = self.etaBinsH.GetXaxis().FindFixBin(eta)
        label = self.etaBinsH.GetXaxis().GetBinLabel(binNumber)
        ptbin = self.FindPtBin("mc", label, pt)
        Eta = math.fabs(eta)
        label = label.replace("Eta", "")

        eff = 1.
        if ptbin == -99:
            eff = 1
        else:
            #eff = self.eff_mcH[label].GetY()[ptbin - 1]

            try:
                # Check if self.eff_mcH[label] is None
                if self.eff_mcH[label] is None:
                    raise ValueError(f"eff_mcH does not contain a valid entry for {label}")

                # Check if self.eff_mcH[label].GetY() is valid and has enough points
                y_values = self.eff_mcH[label].GetY()
                if y_values is None or len(y_values) < ptbin:
                    raise ValueError(f"eff_mcH[{label}].GetY() does not contain enough points")

                # Now safely access the values
                eff = y_values[ptbin - 1]
            except (IndexError, ReferenceError, ValueError) as e:
                print(f"An error occurred: {e} in get_EfficiencyMC")


        # print "inside eff_mc
        # pt",pt,"eta",eta,"label",label,"N",self.eff_mcH[label].GetN(),"ptbin",ptbin,
        # eff

        if eff > 1.:
            eff = -1
        if eff < 0:
            eff = 0.
        return eff

    def get_EfficiencyData(self, pt, eta):

        eta = math.fabs(eta)
        label = str(self.FindEtaLabel(eta))
        binNumber = self.etaBinsH.GetXaxis().FindFixBin(eta)
        label = self.etaBinsH.GetXaxis().GetBinLabel(binNumber)
        # print self.eff_dataH
        ptbin = self.FindPtBin("data", label, pt)
        Eta = math.fabs(eta)
        label = label.replace("Eta", "")
        eff = 1.
        if ptbin == -99:
            eff = 1
            print ('this is a case with ptbin=-99', eff)
        else:
            #eff = self.eff_dataH[label].GetY()[ptbin - 1]

            try:
                # Check if self.eff_dataH[label] is None
                if self.eff_dataH[label] is None:
                    raise ValueError(f"eff_dataH does not contain a valid entry for {label}")

                # Check if self.eff_dataH[label].GetY() is valid and has enough points
                y_values = self.eff_dataH[label].GetY()
                if y_values is None or len(y_values) < ptbin:
                    raise ValueError(f"eff_dataH[{label}].GetY() does not contain enough points")

                # Now safely access the values
                eff = y_values[ptbin - 1]
            except (IndexError, ReferenceError, ValueError) as e:
                print(f"An error occurred: {e} in get_EfficiencyData", ptbin, eta, pt,  ptbin)



        # print "inside eff_data",eff
        # print "inside eff_data
        # pt",pt,"eta",eta,"label",label,"N",self.eff_dataH[label].GetN(),"ptbin",ptbin,
        # eff

        if eff > 1.:
            eff = -1
        if eff < 0:
            eff = 0.

        return eff

    def FindPtBin(self, whatisit, EtaLabel, Pt):

        eff_map = self.eff_mcH
        EtaLabel = EtaLabel.replace("Eta", "")
        if whatisit == "mc":
            eff_map = self.eff_mcH  # EtaLabel = "ZMass"+EtaLabel+"_MC"
        if whatisit == "data":
            eff_map = self.eff_dataH  # EtaLabel = "ZMass"+EtaLabel+"_MC"
        #if whatisit == "data" : EtaLabel = "ZMass"+EtaLabel+"_Data"
        # print "and inside
        # FintPtBin",EtaLabel,self.eff_mcH[EtaLabel].GetN(),EtaLabel,eff_map[EtaLabel].GetN()

        Npoints = eff_map[EtaLabel].GetN()
        ptMAX, ptMIN = 0, 0
        #try:
        #    #print (EtaLabel)
        #    ptMAX = (eff_map[EtaLabel].GetX()[Npoints - 1]) +  (eff_map[EtaLabel].GetErrorXhigh(Npoints - 1))
        #except IndexError or ReferenceError:
        #    return -99

        try:
            # Check if eff_map[EtaLabel] is None
            if eff_map[EtaLabel] is None:
                raise ValueError(f"eff_map does not contain a valid entry for {EtaLabel}")

            # Check if eff_map[EtaLabel].GetX() is valid and has enough points
            x_values = eff_map[EtaLabel].GetX()
            if x_values is None or len(x_values) < Npoints:
                raise ValueError(f"eff_map[{EtaLabel}].GetX() does not contain enough points")

            # Check if Npoints - 1 is a valid index for GetErrorXhigh
            if Npoints - 1 >= eff_map[EtaLabel].GetN():
                raise ValueError(f"Npoints - 1 is out of bounds for GetErrorXhigh")

            # Now safely access the values
            ptMAX = (x_values[Npoints - 1]) + (eff_map[EtaLabel].GetErrorXhigh(Npoints - 1))
        except (IndexError, ReferenceError, ValueError) as e:
            print(f"An error occurred: {e} in FindPtMax")


        #try:
        #    ptMIN = (eff_map[EtaLabel].GetX()[0]) -  (eff_map[EtaLabel].GetErrorXlow(0))
        #except IndexError:
        #    return -99
        # print Npoints, "Npoints for         ===============>",eff_map[EtaLabel].GetN(),EtaLabel,Pt,eff_map[EtaLabel].GetN(),whatisit,ptMAX,ptMIN,eff_map[EtaLabel].GetXaxis().FindBin(Pt)

        try:
            # Check if eff_map[EtaLabel] is None
            if eff_map[EtaLabel] is None:
                raise ValueError(f"eff_map does not contain a valid entry for {EtaLabel}")

            # Check if eff_map[EtaLabel].GetX() is valid and has at least one point
            x_values = eff_map[EtaLabel].GetX()
            if x_values is None or len(x_values) == 0:
                raise ValueError(f"eff_map[{EtaLabel}].GetX() does not contain any points")

            # Check if GetErrorXlow(0) is a valid call
            if 0 >= eff_map[EtaLabel].GetN():
                raise ValueError(f"Index 0 is out of bounds for GetErrorXlow")

            # Now safely access the values
            ptMIN = (x_values[0]) - (eff_map[EtaLabel].GetErrorXlow(0))
        except (IndexError, ReferenceError, ValueError) as e:
            print(f"An error occurred: {e} in FindptMin")

        if callable(Pt):
            Pt = Pt()

        # Ensure Pt is converted to float
        Pt = float(Pt)
    
        if float(Pt) >= ptMAX:
            return Npoints
        elif float(Pt) < ptMIN:
            return -99
        else:
            return eff_map[EtaLabel].GetXaxis().FindFixBin(Pt)

    def FindEtaLabel(self, Eta):

        Eta = math.fabs(Eta)
        binNumber = self.etaBinsH.GetXaxis().FindFixBin(Eta)
        EtaLabel = self.etaBinsH.GetXaxis().GetBinLabel(binNumber)

        # print "inside FindEtaLabel",EtaLabel

        return EtaLabel
