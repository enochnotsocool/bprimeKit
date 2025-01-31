##**************************************************************************************************
##
##    FileName   :  bprimeKit_miniAOD.py
##    Description:  Configuration file for running bprimeKit ntuple production for miniAOD
##    Usage      :  cmsRun bprimeKit_miniAOD.py 
##    options    :  maxEvts=<number>
##
##**************************************************************************************************

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as opts

options = opts.VarParsing ('analysis')

options.register('maxEvts',
                 -1,# default value: process all events
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int,
                 'Number of events to process')


options.register('sample',
#'/store/data/Run2015B/DoubleMuon/MINIAOD/PromptReco-v1/000/251/244/00000/E42FEF61-6E27-E511-B93A-02163E0143C0.root',
'/store/data/Run2015B/DoubleMuon/MINIAOD/PromptReco-v1/000/251/162/00000/12284DB9-4227-E511-A438-02163E013674.root',
#'/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/883/00000/62919ECB-1F2D-E511-B387-02163E013796.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')

options.register('lheLabel',
                 'source',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'LHE module label')

options.register('outputLabel',
                 'B2GEDMNtuple.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Output label')

options.register('globalTag',
      '74X_dataRun2_Prompt_v0',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Global Tag')

options.register('isData',
                 True,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Is data?')

options.register('LHE',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Keep LHEProducts')


options.register('Debug',
                 0,# default value: no messages
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int,
                 'debug level')

options.parseArguments()

if(options.isData):options.LHE = False

    
###inputTag labels
muLabel   = 'slimmedMuons'
elLabel   = 'slimmedElectrons'
jLabel    = 'slimmedJets'
jLabelAK8 = 'slimmedJetsAK8'

pvLabel           = 'offlineSlimmedPrimaryVertices'
convLabel         = 'reducedEgamma:reducedConversions'
particleFlowLabel = 'packedPFCandidates'
metLabel          = 'slimmedMETs'
rhoLabel          = 'fixedGridRhoFastjetAll'

triggerResultsLabel    = "TriggerResults"
triggerSummaryLabel    = "hltTriggerSummaryAOD"
hltMuonFilterLabel     = "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f40QL3crIsoRhoFiltered0p15"
hltPathLabel           = "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"
hltElectronFilterLabel = "hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8"
lheLabel               = "source"

process = cms.Process("b2gEDMNtuples")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('HLTrigReport')
### Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
### Number of maximum events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts) )


#------------------------------------------------------------------------------- 
#   b tag discriminators 
#------------------------------------------------------------------------------- 
bTagDiscriminators = [
   'combinedSecondaryVertexBJetTags'              ,
   'pfJetBProbabilityBJetTags'                    ,
   'pfJetProbabilityBJetTags'                     ,
   'pfTrackCountingHighPurBJetTags'               ,
   'pfTrackCountingHighEffBJetTags'               ,
   'pfSimpleSecondaryVertexHighEffBJetTags'       ,
   'pfSimpleSecondaryVertexHighPurBJetTags'       ,
   'pfCombinedSecondaryVertexV2BJetTags'          ,
   'pfCombinedInclusiveSecondaryVertexV2BJetTags' ,
   'pfCombinedSecondaryVertexSoftLeptonBJetTags'  ,
   'pfCombinedMVABJetTags' 
]

#-------------------------------------------------------------------------------
#  Input file 
#-------------------------------------------------------------------------------
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
        options.sample
        )
)

process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load( "PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff" )
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = options.globalTag 
    


###
### AK8 jets with subjet b-tagging
###

#------------------------------------------------------------------------------- 
#   Make Jets 
#------------------------------------------------------------------------------- 

## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", 
        src = cms.InputTag("packedGenParticles"), 
        cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16") )
## Fat GenJets
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak8GenJetsNoNu = ak4GenJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag("packedGenParticlesForJetsNoNu")
)

## Pruned fat GenJets (two jet collections are produced, fat jets and subjets)
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak8GenJetsNoNuPruned = ak4GenJets.clone(
    SubJetParameters,
    rParam = cms.double(0.8),
    src = cms.InputTag("packedGenParticlesForJetsNoNu"),
    usePruning = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)

## Select charged hadron subtracted packed PF candidates
process.pfCHS = cms.EDFilter(
   "CandPtrSelector", 
   src = cms.InputTag("packedPFCandidates"), 
   cut = cms.string("fromPV")
)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets


process.ak8PFJetsCHS = ak4PFJets.clone(
    rParam        = cms.double(0.8),
    src           = cms.InputTag("pfCHS"),
    doAreaFastjet = cms.bool(True),
    jetPtMin      = cms.double(100.)
)


process.ak8PFJetsCHSConstituents = cms.EDFilter(
   "MiniAODJetConstituentSelector",
   src = cms.InputTag("ak8PFJetsCHS"),
   cut = cms.string("pt > 100.0")
)

## Pruned fat PFJets (two jet collections are produced, fat jets and subjets)
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
process.ak8PFJetsCHSPruned = ak5PFJetsPruned.clone(
    rParam                 = cms.double(0.8) ,
    src                    = cms.InputTag("ak8PFJetsCHSConstituents" , "constituents") ,
    doAreaFastjet          = cms.bool(True)  ,
    writeCompound          = cms.bool(True)  ,
    jetCollInstanceName    = cms.string("SubJets")     ,
    jetPtMin               = cms.double(100.)
)



from PhysicsTools.PatAlgos.tools.jetTools import *
## PATify fat jets
addJetCollection(
    process,
    labelName          = 'AK8PFCHS',
    jetSource          = cms.InputTag('ak8PFJetsCHS'),
    algo               = 'ak',  # needed for jet flavor clustering
    rParam             = 0.8, # needed for jet flavor clustering
    pvSource           = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates       = cms.InputTag('packedPFCandidates'),
    svSource           = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    jetCorrections     = ('AK8PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection   = cms.InputTag('ak8GenJetsNoNu')
)
getattr(process,'patJetPartons').particles = cms.InputTag('prunedGenParticles')
getattr(process,'patJetPartonMatchAK8PFCHS').matched = cms.InputTag('prunedGenParticles')
if hasattr(process,'pfInclusiveSecondaryVertexFinderTagInfosAK8PFCHS'):
    getattr(process,'pfInclusiveSecondaryVertexFinderTagInfosAK8PFCHS').extSVCollection = cms.InputTag('slimmedSecondaryVertices')
getattr(process,'patJetsAK8PFCHS').addAssociatedTracks = cms.bool(False) # needs to be disabled since there is no track collection present in MiniAOD
getattr(process,'patJetsAK8PFCHS').addJetCharge = cms.bool(False)        # needs to be disabled since there is no track collection present in MiniAOD

from RecoJets.JetProducers.ak8PFJetsCHS_groomingValueMaps_cfi import *
process.ak8PFJetsCHSPrunedMass = cms.EDProducer("RecoJetDeltaRValueMapProducer",
    src     = cms.InputTag("ak8PFJetsCHS"),
    matched = cms.InputTag("ak8PFJetsCHSPruned"),
    distMax = cms.double(0.8),
    value   = cms.string('mass') )

### Add Nsubjettiness
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness
process.Njettiness = Njettiness.clone(
    src = cms.InputTag("ak8PFJetsCHS"),
    cone = cms.double(0.8)
    )

process.patJetsAK8PFCHS.userData.userFloats.src += ['ak8PFJetsCHSPrunedMass','Njettiness:tau1','Njettiness:tau2','Njettiness:tau3']

## PATify pruned fat jets
addJetCollection(
    process,
    labelName          = 'AK8PFCHSPruned',
    jetSource          = cms.InputTag('ak8PFJetsCHSPruned'),
    btagDiscriminators = ['None'],
    jetCorrections     = ('AK8PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection   = cms.InputTag('ak8GenJetsNoNu'),
    getJetMCFlavour    = False # jet flavor disabled
)
getattr(process,'patJetPartonMatchAK8PFCHSPruned').matched = cms.InputTag('prunedGenParticles')
## PATify pruned subjets
addJetCollection(
    process,
    labelName          = 'AK8PFCHSPrunedSubjets',
    jetSource          = cms.InputTag('ak8PFJetsCHSPruned','SubJets'),
    algo               = 'ak',  # needed for subjet flavor clustering
    rParam             = 0.8, # needed for subjet flavor clustering
    pvSource           = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates       = cms.InputTag('packedPFCandidates'),
    svSource           = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    jetCorrections     = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection   = cms.InputTag('ak8GenJetsNoNuPruned','SubJets'),
    explicitJTA        = True,  # needed for subjet b tagging
    svClustering       = True, # needed for subjet b tagging
    fatJets            = cms.InputTag('ak8PFJetsCHS'),             # needed for subjet flavor clustering
    groomedFatJets     = cms.InputTag('ak8PFJetsCHSPruned') # needed for subjet flavor clustering
)
getattr(process,'patJetGenJetMatchAK8PFCHSPrunedSubjets').matched = cms.InputTag('ak8GenJetsNoNuPruned', 'SubJets')
getattr(process,'patJetPartonMatchAK8PFCHSPrunedSubjets').matched = cms.InputTag('prunedGenParticles')
if hasattr(process,'pfInclusiveSecondaryVertexFinderTagInfosAK8PFCHSPrunedSubjets'):
    getattr(process,'pfInclusiveSecondaryVertexFinderTagInfosAK8PFCHSPrunedSubjets').extSVCollection = cms.InputTag('slimmedSecondaryVertices')
getattr(process,'patJetsAK8PFCHSPrunedSubjets').addAssociatedTracks = cms.bool(False) # needs to be disabled since there is no track collection present in MiniAOD
getattr(process,'patJetsAK8PFCHSPrunedSubjets').addJetCharge = cms.bool(False)        # needs to be disabled since there is no track collection present in MiniAOD

## Establish references between PATified fat jets and subjets using the BoostedJetMerger
process.selectedPatJetsAK8PFCHSPrunedPacked = cms.EDProducer("BoostedJetMerger",
    jetSrc=cms.InputTag("selectedPatJetsAK8PFCHSPruned"),
    subjetSrc=cms.InputTag("selectedPatJetsAK8PFCHSPrunedSubjets")
)


#------------------------------------------------------------------------------- 
#   TOP TAG Jets 
#-------------------------------------------------------------------------------

# patJetsCMSTopTagCHS
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *

process.cmsTopTagCHS = cms.EDProducer(
    "CATopJetProducer",
    PFJetParameters.clone( src           = cms.InputTag("ak8PFJetsCHSConstituents", "constituents"),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet  = cms.bool(False),
                           jetPtMin      = cms.double(100.0)
                           ),
    AnomalousCellParameters,
    CATopJetParameters.clone( jetCollInstanceName = cms.string("SubJets"),
                              verbose             = cms.bool(False),
                              algorithm           = cms.int32(1), # 0 = KT, 1 = CA, 2 = anti-KT
                              tagAlgo             = cms.int32(0), # 0= legacy top
                              useAdjacency        = cms.int32(2), # modified adjacency
                              centralEtaCut       = cms.double(2.5), # eta for defining "central" jets
                              sumEtBins           = cms.vdouble(0,1600,2600), # sumEt bins over which cuts vary. vector= {bin 0 lower bound, bin 1 lower bound, ...}
                              rBins               = cms.vdouble(0.8,0.8,0.8), # Jet distance paramter R. R values depend on sumEt bins.
                              ptFracBins          = cms.vdouble(0.05,0.05,0.05), # minimum fraction of central jet pt for subjets (deltap)
                              deltarBins          = cms.vdouble(0.19,0.19,0.19), # Applicable only if useAdjacency= 1. deltar adjacency values for each sumEtBin
                              nCellBins           = cms.vdouble(1.9,1.9,1.9),
                            ),
    jetAlgorithm  = cms.string("CambridgeAachen"),
    rParam        = cms.double(0.8),
    writeCompound = cms.bool(True)
    )
process.CATopTagInfos = cms.EDProducer("CATopJetTagger",
                                    src        = cms.InputTag("cmsTopTagCHS"),
                                    TopMass    = cms.double(171),
                                    TopMassMin = cms.double(0.),
                                    TopMassMax = cms.double(250.),
                                    WMass      = cms.double(80.4),
                                    WMassMin   = cms.double(0.0),
                                    WMassMax   = cms.double(200.0),
                                    MinMassMin = cms.double(0.0),
                                    MinMassMax = cms.double(200.0),
                                    verbose    = cms.bool(False)
                                    )
addJetCollection(
    process,
    labelName          = 'CMSTopTagCHS',
    jetSource          = cms.InputTag('cmsTopTagCHS'),
    jetCorrections     = ('AK8PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    pvSource           = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates       = cms.InputTag('packedPFCandidates'),
    svSource           = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    genJetCollection   = cms.InputTag('ak8GenJetsNoNu'),
    getJetMCFlavour    = False
    )
getattr(process,'patJetPartons').particles = cms.InputTag('prunedGenParticles')
getattr(process,'patJetPartonMatchCMSTopTagCHS').matched = cms.InputTag('prunedGenParticles')
if hasattr(process,'pfInclusiveSecondaryVertexFinderTagInfosCMSTopTagCHS'):
    getattr(process,'pfInclusiveSecondaryVertexFinderTagInfosCMSTopTagCHS').extSVCollection = cms.InputTag('slimmedSecondaryVertices')
process.patJetsCMSTopTagCHS.addTagInfos = True
process.patJetsCMSTopTagCHS.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfos')
    )
getattr(process,'patJetsCMSTopTagCHS').addAssociatedTracks = cms.bool(False) # needs to be disabled since there is no track collection present in MiniAOD
getattr(process,'patJetsCMSTopTagCHS').addJetCharge = cms.bool(False)        # needs to be disabled since there is no track collection present in MiniAOD

addJetCollection(
    process,
    labelName          = 'CMSTopTagCHSSubjets',
    jetSource          = cms.InputTag('cmsTopTagCHS','SubJets'),
    pvSource           = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates       = cms.InputTag('packedPFCandidates'),
    svSource           = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = ['pfCombinedSecondaryVertexBJetTags'],
    jetCorrections     = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    explicitJTA        = True,  # needed for subjet b tagging
    svClustering       = True, # needed for subjet b tagging
    getJetMCFlavour    = False,
    genJetCollection   = cms.InputTag('ak8GenJetsNoNu'),
    )

getattr(process,'patJetPartonMatchCMSTopTagCHSSubjets').matched = cms.InputTag('prunedGenParticles')
if hasattr(process,'pfInclusiveSecondaryVertexFinderTagInfosCMSTopTagCHSSubjets'):
    getattr(process,'pfInclusiveSecondaryVertexFinderTagInfosCMSTopTagCHSSubjets').extSVCollection = cms.InputTag('slimmedSecondaryVertices')
getattr(process,'patJetsCMSTopTagCHSSubjets').addAssociatedTracks = cms.bool(False) # needs to be disabled since there is no track collection present in MiniAOD
getattr(process,'patJetsCMSTopTagCHSSubjets').addJetCharge = cms.bool(False)        # needs to be disabled since there is no track collection present in MiniAOD

process.patJetsCMSTopTagCHSPacked = cms.EDProducer("BoostedJetMerger",
    jetSrc=cms.InputTag("patJetsCMSTopTagCHS" ),
    subjetSrc=cms.InputTag("patJetsCMSTopTagCHSSubjets")
    )

### Selected leptons and jets
process.skimmedPatMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag(muLabel),
    cut = cms.string("pt > 30 && abs(eta) < 2.4")
    )

process.skimmedPatElectrons = cms.EDFilter(
    "PATElectronSelector",
    src = cms.InputTag(elLabel),
    cut = cms.string("pt > 10 && abs(eta) < 2.5")
    )

process.skimmedPatMET = cms.EDFilter(
    "PATMETSelector",
    src = cms.InputTag(metLabel),
    cut = cms.string("")
    )


process.skimmedPatJets = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag(jLabel),
    cut = cms.string(" pt > 25 && abs(eta) < 5.")
    )

process.skimmedPatJetsAK8 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag(jLabelAK8),
    cut = cms.string("pt > 100 && abs(eta) < 5.")    
    )

process.skimmedPatSubJetsAK8 = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag("selectedPatJetsAK8PFCHSPrunedSubjets"),
    cut = cms.string("pt > 0")
    )

process.skimmedCMSTOPTAGSubJets = cms.EDFilter(
    "CandViewSelector",
    src = cms.InputTag("selectedPatJetsCMSTopTagCHSSubjets"),
    cut = cms.string("pt > 0")
)


process.EventUserData = cms.EDProducer(
    'EventUserData',
    pileup = cms.InputTag("addPileupInfo"),
    pvSrc  = cms.InputTag("offlineSlimmedPrimaryVertices")
)

process.muonUserData = cms.EDProducer(
    'MuonUserData',
    muonLabel          = cms.InputTag("skimmedPatMuons"),
    pv                 = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults     = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary     = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltMuonFilter      = cms.InputTag(hltMuonFilterLabel),
    hltPath            = cms.string("HLT_IsoMu40_eta2p1_v11"),
    hlt2reco_deltaRmax = cms.double(0.1),
    # mainROOTFILEdir  = cms.string("../data/")
    )

process.jetUserData = cms.EDProducer(
    'JetUserData',
    jetLabel           = cms.InputTag("slimmedJets"),
    ### TTRIGGER ###
    triggerResults     = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary     = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2),
    )


process.jetUserDataAK8 = cms.EDProducer(
    'JetUserData',
    jetLabel           = cms.InputTag("slimmedJetsAK8"),
    pv                 = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults     = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary     = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2)
)

process.cmstoptagjetUserData = cms.EDProducer(
    'JetUserData',
    jetLabel           = cms.InputTag("patJetsCMSTopTagCHS"),
    packedjetLabel     = cms.InputTag("patJetsCMSTopTagCHSPacked"),
    subjetLabel        = cms.InputTag("patJetsCMSTopTagCHSSubjets"),
    pv                 = cms.InputTag(pvLabel),
    ### TTRIGGER ###
    triggerResults     = cms.InputTag(triggerResultsLabel,"","HLT"),
    triggerSummary     = cms.InputTag(triggerSummaryLabel,"","HLT"),
    hltJetFilter       = cms.InputTag("hltSixCenJet20L1FastJet"),
    hltPath            = cms.string("HLT_QuadJet60_DiJet20_v6"),
    hlt2reco_deltaRmax = cms.double(0.2)
)

process.electronUserData = cms.EDProducer(
    'ElectronUserData',
    eleLabel            = cms.InputTag("skimmedPatElectrons"),
    pv                  = cms.InputTag(pvLabel),
    conversion          = cms.InputTag(convLabel),
    rho                 = cms.InputTag(rhoLabel),
    triggerResults      = cms.InputTag(triggerResultsLabel),
    triggerSummary      = cms.InputTag(triggerSummaryLabel),
    hltElectronFilter   = cms.InputTag(hltElectronFilterLabel),  ##trigger matching code to be fixed!
    hltPath             = cms.string("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"),
    #electronVetoIdMap  = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V0-miniAOD-standalone-veto"),
    #electronTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V0-miniAOD-standalone-tight"),
    )


from PhysicsTools.PatAlgos.tools.pfTools import *
## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag('offlineSlimmedPrimaryVertices'))

#################################################


from PhysicsTools.CandAlgos.EventShapeVars_cff import *
process.eventShapePFVars = pfEventShapeVars.clone()
process.eventShapePFVars.src = cms.InputTag(particleFlowLabel)

process.eventShapePFJetVars = pfEventShapeVars.clone()
process.eventShapePFJetVars.src = cms.InputTag("skimmedPatJets")

process.centrality = cms.EDProducer("CentralityUserData",
    src = cms.InputTag("skimmedPatJets")
    )                                    

process.TriggerUserData = cms.EDProducer(
    'TriggerUserData',
    bits      = cms.InputTag("TriggerResults","","HLT"),
    prescales = cms.InputTag("patTrigger"),
    storePrescales = cms.untracked.bool(True), 
   hltProcName = cms.untracked.string("HLT"),
    objects   = cms.InputTag("selectedPatTrigger")
    )                                 


### Including ntuplizer 
process.load("Analysis.B2GAnaFW.b2gedmntuples_cff")
process.options.allowUnscheduled = cms.untracked.bool(True)

process.edmNtuplesOut = cms.OutputModule(
      "PoolOutputModule",
      fileName = cms.untracked.string('B2GEDMNtuple.root'),
      outputCommands = cms.untracked.vstring(
         "drop *",
         "keep *_muons_*_*",
         "keep *_electrons_*_*",
         "keep *_photons_*_*",
         "keep *_photonjets_*_*",
         "keep *_jetsAK4_*_*",
         "keep *_jetsAK8_*_*",
         "keep *_eventShape*_*_*",
         "keep *_*_*centrality*_*",
         "keep *_met_*_*",
         "keep *_eventInfo_*_*",
         "keep *_subjetsAK8_*_*",
         "keep *_subjetsCmsTopTag*_*_*",
         "keep *_jetKeysAK4_*_*",
         "keep *_jetKeysAK8_*_*",
         "keep *_subjetKeysAK8_*_*",
         "keep *_subjetsCmsTopTagKeys_*_*",
         "keep *_electronKeys_*_*",   
         "keep *_muonKeys_*_*",
         "keep *_TriggerUserData*_trigger*_*",
         "keep *_fixedGridRhoFastjetAll_*_*",
         "keep *_eventUserData_*_*"
         ),
      dropMetaData = cms.untracked.string('ALL'),
      )
### keep info from LHEProducts if they are stored in PatTuples
if(options.LHE):
  process.LHEUserData = cms.EDProducer("LHEUserData",
  lheLabel = cms.InputTag(options.lheLabel)
  )
  #process.analysisPath+=process.LHEUserData
  process.edmNtuplesOut.outputCommands+=('keep *_*LHE*_*_*',)
  process.edmNtuplesOut.outputCommands+=('keep LHEEventProduct_*_*_*',)
### end LHE products     

if not options.isData : 
    process.edmNtuplesOut.outputCommands+=(
        'keep *_generator_*_*',
        "keep *_genPart_*_*",
        "keep *_genJetsAK8_*_*",
        "keep *_genJetsAK8SoftDrop_*_*"
        )

process.edmNtuplesOut.fileName=options.outputLabel

#process.edmNtuplesOut.SelectEvents = cms.untracked.PSet(
#    SelectEvents = cms.vstring('filterPath')
#    )

#------------------------------------------------------------------------------- 
#   QG tagger pre-requisites
#------------------------------------------------------------------------------- 
qgDatabaseVersion = 'v1'

from CondCore.DBCommon.CondDBSetup_cfi import *
QGPoolDBESSource = cms.ESSource("PoolDBESSource",
      CondDBSetup,
      toGet = cms.VPSet(),
      connect = cms.string('frontier://FrontierProd/CMS_COND_PAT_000'),
   )

for type in ['AK4PFchs','AK4PFchs_antib']:
   QGPoolDBESSource.toGet.extend(
      cms.VPSet(cms.PSet(
         record = cms.string('QGLikelihoodRcd'),
         tag    = cms.string('QGLikelihoodObject_'+qgDatabaseVersion+'_'+type),
         label  = cms.untracked.string('QGL_'+type)
   )))
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets          = cms.InputTag('slimmedJets')
process.QGTagger.jetsLabel        = cms.string('QGL_AK4PFchs')
process.QGTagger.systematicsLabel = cms.string('')

#------------------------------------------------------------------------------- 
#   Egamma ID pre-requisites
#-------------------------------------------------------------------------------
from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
switchOnVIDPhotonIdProducer(process, dataFormat)

my_id_modules = [
   'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
   'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV51_cff']
for idmod in my_id_modules:
   setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

my_phoid_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_PHYS14_PU20bx25_V2_cff']
for idmod in my_phoid_modules:
   setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)


#------------------------------------------------------------------------------- 
#   Loading bprimeKit setup in python/bprimeKit_cfi.py 
#------------------------------------------------------------------------------- 

resultsFile = 'results.root'
process.TFileService = cms.Service("TFileService",
    fileName = cms.string( resultsFile )
)

process.load("MyAna.bprimeKit.bprimeKit_cfi")
process.bprimeKit.Debug=options.Debug

#process.fullPath = cms.Schedule(
#    process.analysisPath
#    )

process.endPath = cms.Path(
   process.egmGsfElectronIDSequence * 
   process.egmPhotonIDSequence *
   process.bprimeKit
)


#open('B2GEntupleFileDump.py','w').write(process.dumpPython())
