# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
photons, photonLabel = Handle("std::vector<pat::Photon>"), "slimmedPhotons"
taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
tauLabelb = "slimmedTausBoosted"
jets = Handle("std::vector<pat::Jet>")
fatjets, fatjetLabel = Handle("std::vector<pat::Jet>"), "slimmedJetsAK8"
mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
verticesScore = Handle("edm::ValueMap<float>")
seenIt = {} # list of things we've seen (so that we dump them in full only once)

# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
events = Events("root://eoscms//eos/cms/store/relval/CMSSW_8_0_3/RelValTTbarLepton_13/MINIAODSIM/80X_mcRun2_asymptotic_2016_v3_gs7120p2NewGTv3-v1/00000/4E291B64-DCEF-E511-B99D-0025905A60B0.root")
events = Events("test.root")

for iev,event in enumerate(events):
    if iev >= 10: break
    event.getByLabel(muonLabel, muons)
    event.getByLabel(electronLabel, electrons)
    event.getByLabel(photonLabel, photons)
    event.getByLabel(tauLabel, taus)
    event.getByLabel(fatjetLabel, fatjets)
    event.getByLabel(metLabel, mets)
    event.getByLabel(vertexLabel, vertices)
    event.getByLabel(vertexLabel, verticesScore)

    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    # Vertices
    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        print "Event has no good primary vertex."
        continue
    else:
        PV = vertices.product()[0]
        print "PV at x,y,z = %+5.3f, %+5.3f, %+6.3f, ndof: %.1f, score: (pt2 of clustered objects) %.1f" % (PV.x(), PV.y(), PV.z(), PV.ndof(),verticesScore.product().get(0))

    # Muons
    for i,mu in enumerate(muons.product()):
        if mu.pt() < 5 or not mu.isLooseMuon(): continue
        print "muon %2d: pt %4.1f, dz(PV) %+5.3f, POG loose id %d, tight id %d." % (
            i, mu.pt(), mu.muonBestTrack().dz(PV.position()), mu.isLooseMuon(), mu.isTightMuon(PV))

    # Electrons
    for i,el in enumerate(electrons.product()):
        if el.pt() < 5: continue
        print "elec %2d: pt %4.1f, supercluster eta %+5.3f, sigmaIetaIeta %.3f (full5x5), non-triggering Spring15 MVA score %+.3f, lost hits %d, pass conv veto %d" % (
                    i, el.pt(), el.superCluster().eta(), el.full5x5_sigmaIetaIeta(), el.userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"), el.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS), el.passConversionVeto())
        if 'ele' not in seenIt:
            for  eleid in el.electronIDs():
                print  "\t%s %s" % (eleid.first, eleid.second)
            seenIt['ele'] = True

    # Photon
    for i,pho in enumerate(photons.product()):
        if pho.pt() < 20 or pho.chargedHadronIso()/pho.pt() > 0.3: continue
        print "phot %2d: pt %4.1f, supercluster eta %+5.3f, sigmaIetaIeta %.3f (full5x5 shower shapes)" % (
                    i, pho.pt(), pho.superCluster().eta(), pho.full5x5_sigmaIetaIeta())
        if 'pho' not in seenIt:
            for  phoid in pho.photonIDs():
                print  "\t%s %s" % (phoid.first, phoid.second)
            seenIt['pho'] = True

    # Tau
    event.getByLabel(tauLabel, taus)
    for i,tau in enumerate(taus.product()):
        if tau.pt() < 20: continue
        print "tau  %2d: pt %4.1f, dxy signif %.1f, ID(byMediumCombinedIsolationDeltaBetaCorr3Hits) %.1f, lead candidate pt %.1f, pdgId %d " % (
                    i, tau.pt(), tau.dxy_Sig(), tau.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"), tau.leadCand().pt(), tau.leadCand().pdgId())
        if 'tau' not in seenIt:
            for  tauid in tau.tauIDs():
                print  "\t%s %s" % (tauid.first, tauid.second)
            seenIt['tau'] = True
    # Tau (Boosted)
    event.getByLabel(tauLabelb, taus)
    for i,tau in enumerate(taus.product()):
        if tau.pt() < 20: continue
        print "boosted tau  %2d: pt %4.1f, dxy signif %.1f, ID(byMediumCombinedIsolationDeltaBetaCorr3Hits) %.1f, lead candidate pt %.1f, pdgId %d " % (
                    i, tau.pt(), tau.dxy_Sig(), tau.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"), tau.leadCand().pt(), tau.leadCand().pdgId())
        if 'taub' not in seenIt:
            for  tauid in tau.tauIDs():
                print  "\t%s %s" % (tauid.first, tauid.second)
            seenIt['taub'] = True

    # Jets (AK4, CHS and Puppi)
    for jetLabel, algo in ("slimmedJets", "CHS"), ("slimmedJetsPuppi", "PUPPI"):
        event.getByLabel(jetLabel, jets)
        for i,j in enumerate(jets.product()):
            if j.pt() < 20: continue
            print "jet %s %3d: pt %5.1f (raw pt %5.1f, matched-calojet pt %5.1f), eta %+4.2f, btag CSVIVFv2 %.3f, CMVAv2 %.3f, pileup mva disc %+.2f" % (
                algo, i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.userFloat("caloJetMap:pt") if algo == "CHS" else -99.0, j.eta(), max(0,j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")), max(0,j.bDiscriminator("pfCombinedMVAV2BJetTags")), j.userFloat("pileupJetId:fullDiscriminant") if algo == "CHS" else -99)
            if 'jetAk4'+algo not in seenIt:
                constituents = [ j.daughter(i2) for i2 in xrange(j.numberOfDaughters()) ]
                constituents.sort(key = lambda c:c.pt(), reverse=True)
                for i2, cand in enumerate(constituents):
                    if i2 > 12:
                            print "         ....."
                            break
                    print "         constituent %3d: pt %6.2f, dz(pv) %+.3f, pdgId %+3d, hcal energy fraction %.2f, puppi weight %.3f " % (i2,cand.pt(),cand.dz(PV.position()),cand.pdgId(),cand.hcalFraction(),cand.puppiWeight())
                print "   btag discriminators:"
                for btag in j.getPairDiscri():
                    print  "\t%s %s" % (btag.first, btag.second)
                print "   userFloats:"
                for ufl in j.userFloatNames():
                    print  "\t%s %s" % (ufl, j.userFloat(ufl))
                seenIt['jetAk4'+algo] = True

    # Fat AK8 Jets
    for i,j in enumerate(fatjets.product()):
        print "jetAK8 %3d: pt %5.1f (raw pt %5.1f), eta %+4.2f, mass %5.1f ungroomed, %5.1f softdrop, %5.1f pruned CHS. " % (
            i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.eta(), j.mass(), j.userFloat('ak8PFJetsPuppiSoftDropMass'), j.userFloat('ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass'))
        # If you use CMSSW_9_4_<=6 to read MiniAOD, to get the constituents of the AK8 jets, you have to loop over all of the
        # daughters recursively. To save space, the first two constituents are actually
        # the Soft Drop SUBJETS, which will then point to their daughters.
        # The remaining constituents are those constituents removed by soft drop but
        # still in the AK8 jet.
        if 'jetAk8' not in seenIt:
            constituents = []
            for ida in xrange( j.numberOfDaughters() ) :
                cand = j.daughter(ida)
                if cand.numberOfDaughters() == 0 :
                    constituents.append( cand )
                else : # only needed in CMSSW_9_4_<=6
                    for jda in xrange( cand.numberOfDaughters() ) : # only needed in CMSSW_9_4_<=6
                        cand2 = cand.daughter(jda) # only needed in CMSSW_9_4_<=6
                        constituents.append( cand2 ) # only needed in CMSSW_9_4_<=6
            constituents.sort(key = lambda c:c.pt(), reverse=True)
            for i2, cand in enumerate(constituents):
                if i2 >4:
                            print "         ....."
                            break
                print "         constituent %3d: pt %6.2f, pdgId %+3d, #dau %+3d" % (i2,cand.pt(),cand.pdgId(), cand.numberOfDaughters())
            print "   btag discriminators:"
            for btag in j.getPairDiscri():
                print  "\t%s %s" % (btag.first, btag.second)
            print "   userFloats:"
            for ufl in j.userFloatNames():
                print  "\t%s %s" % (ufl, j.userFloat(ufl))
            seenIt['jetAk8'] = True
        # Print Subjets
        if 'jetAk8SD' not in seenIt:
            wSubjets = j.subjets('SoftDropPuppi')
            for isd,sdsub in enumerate( sdSubjets ) :
                print "   w subjet %3d: pt %5.1f (raw pt %5.1f), eta %+4.2f, mass %5.1f " % (
                    isd, sdsub.pt(), sdsub.pt()*sdsub.jecFactor('Uncorrected'), sdsub.eta(), sdsub.mass()
                    )
                print "   \tbtag discriminators:"
                for btag in sdsub.getPairDiscri():
                    print  "\t\t%s %s" % (btag.first, btag.second)
                print "   \tuserFloats:"
                for ufl in sdsub.userFloatNames():
                    print  "\t\t%s %s" % (ufl, sdsub.userFloat(ufl))
                seenIt['jetAk8SD'] = True

    # MET:
    met = mets.product().front()
    print "MET: pt %5.1f, phi %+4.2f, sumEt (%.1f). rawMET: %.1f, genMET %.1f. MET with JES up/down: %.1f/%.1f" % (
        met.pt(), met.phi(), met.sumEt(),  met.uncorPt());
        #try met.genMET().pt(),
        #met.shiftedPt(ROOT.pat.MET.JetEnUp), met.shiftedPt(ROOT.pat.MET.JetEnDown));

