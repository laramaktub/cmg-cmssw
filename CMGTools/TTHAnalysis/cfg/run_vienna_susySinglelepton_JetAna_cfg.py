##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES       ##
## skim condition: >= 0 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import * 

# Lepton Preselection
# ele
lepAna.loose_electron_id = "POG_MVA_ID_Run2_NonTrig_Loose"
lepAna.loose_electron_pt  = 5
# mu
lepAna.loose_muon_pt  = 5

# Redefine what I need
lepAna.packedCandidates = 'packedPFCandidates'

# selec Iso
isolation = "miniIso"

if isolation == "miniIso":
# do miniIso
    lepAna.doMiniIsolation = True
    lepAna.miniIsolationPUCorr = 'rhoArea'
    lepAna.miniIsolationVetoLeptons = None
    lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
    lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
# normal relIso03
    lepAna.ele_isoCorr = "rhoArea" 
    lepAna.mu_isoCorr = "rhoArea" 

    lepAna.loose_electron_relIso = 0.5
    lepAna.loose_muon_relIso = 0.5

# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999
#LepSkim.idCut  = ""
#LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---
jetAna.minLepPt = 10 
jetAna.jetCol = 'slimmedJets'
#jetAna.jetCol = 'patJetsAK4PFCHS'
jetAna.copyJetsByValue = False
jetAna.mcGT = "PHYS14_V4_MC"
jetAna.doQG = True
jetAna.smearJets = False #should be false in susycore, already
jetAna.recalibrateJets = True #should be true in susycore, already
metAna.recalibrate = False #should be false in susycore, already


# --- JET-LEPTON CLEANING ---
jetAnaAK4CHS = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzerAK4CHS',
    jetCol = 'patJetsAK4PFCHS',
    copyJetsByValue = True,
    genJetCol = ('patJetsAK4PFCHS','genJets'),
    rho = ('fixedGridRhoFastjetAll','',''),
    cleanSelectedLeptons = False, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.4,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    minLepPt = 10,
    relaxJetId = False,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = "MC", # True, False, 'MC', 'Data'
    recalibrationType = "AK4PFchs",
    mcGT     = "PHYS14_V4_MC",
    jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
    shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts  
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    cleanGenJetsFromPhoton = False
    )
jetAnaAK4CHS.collectionPostFix="AK4CHS"

isoTrackAna.setOff=False


from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHSVAna)

susyCoreSequence.insert(susyCoreSequence.index(jetAna), jetAnaAK4CHS)

## Single lepton + ST skim
from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
ttHSTSkimmer = cfg.Analyzer(
    ttHSTSkimmer, name='ttHSTSkimmer',
    minST = 200,
    )

from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer import ttHReclusterJetsAnalyzer
ttHReclusterJets = cfg.Analyzer(
    ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
    pTSubJet = 30,
    etaSubJet = 5.0,
            )

triggerFlagsAna.triggerBits = {
#put trigger here for data
}

# Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusySingleLepton import *
## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusySingleLepton',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susySingleLepton_globalVariables,
     globalObjects = susySingleLepton_globalObjects,
     collections = susySingleLepton_collections,
)

#-------- SAMPLES AND TRIGGERS -----------

#from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14_private import *
from CMGTools.TTHAnalysis.samples.samples_13TeV_PHYS14 import *
#selectedComponents = [QCD_HT_100To250, QCD_HT_250To500, QCD_HT_500To1000, QCD_HT_1000ToInf,TTJets, TTWJets, TTZJets, TTH, SMS_T1tttt_2J_mGl1500_mLSP100, SMS_T1tttt_2J_mGl1200_mLSP800] + SingleTop + WJetsToLNuHT + DYJetsM50HT + T5ttttDeg + T1ttbbWW + T5qqqqWW


#-------- SEQUENCE
sequence = cfg.Sequence(susyCoreSequence+[
    ttHEventAna,
#    ttHSTSkimmer,
    ttHReclusterJets,
#    ttHJetToolboxAnalyzer,
    treeProducer,
    ])


#-------- HOW TO RUNtest = 1
test = 1
if test==1:
    # test a single component, using a single thread.
    comp = TTJets
    #comp = SMS_T1tttt_2J_mGl1500_mLSP100
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    print len(comp.files)
    #comp.splitFactor = len(comp.files)
    comp.splitFactor = 1
elif test==2:    
    # test all components (1 thread per component).
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[:1]


from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor("%s/src/JMEAnalysis/JetToolbox/test/jettoolbox_cfg.py" % os.environ['CMSSW_BASE'])

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     preprocessor=preprocessor,
                     events_class = Events)
