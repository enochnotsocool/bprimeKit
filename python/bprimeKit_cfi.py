import FWCore.ParameterSet.Config as  cms
from MyAna.bprimeKit.ObjectParameters_cfi import *

bprimeKit = cms.EDAnalyzer(
   "bprimeKit",
   MCtag                     = cms.untracked.bool(False),
   
   rhoLabel                  = cms.InputTag("fixedGridRhoFastjetAll"), 
   metlabel                  = cms.VInputTag("slimmedMETs"),

   #----- Photon information ------------------------------------------------------------------------ 
   PhoCollections            = cms.vstring('PhotonInfo'),
   pholabel                  = cms.VInputTag('slimmedPhotons'),
   phoLooseIdMap             = cms.InputTag( "egmPhotonIDs:cutBasedPhotonID-PHYS14-PU20bx25-V2-standalone-loose"     ) ,
   phoMediumIdMap            = cms.InputTag( "egmPhotonIDs:cutBasedPhotonID-PHYS14-PU20bx25-V2-standalone-medium"    ) ,
   phoTightIdMap             = cms.InputTag( "egmPhotonIDs:cutBasedPhotonID-PHYS14-PU20bx25-V2-standalone-tight"     ) ,
   #phoMVAValuesMap           = cms.InputTag( "photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring15NonTrigValues" ) ,
   phoChargedIsolation       = cms.InputTag( "photonIDValueMapProducer:phoChargedIsolation"                          ) ,
   phoNeutralHadronIsolation = cms.InputTag( "photonIDValueMapProducer:phoNeutralHadronIsolation"                    ) ,
   phoPhotonIsolation        = cms.InputTag( "photonIDValueMapProducer:phoPhotonIsolation"                           ) ,
   
   #----- Lepton related information -------------------------------------------------------------------
   LepCollections  = cms.vstring( 'LepInfo'),
   muonlabel       = cms.VInputTag('slimmedMuons'     ) ,
   eleclabel       = cms.VInputTag('slimmedElectrons' ) ,
   taulabel        = cms.VInputTag('slimmedTaus'      ) ,
   eleVetoIdMap    = cms.InputTag( "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto"   ) ,
   eleLooseIdMap   = cms.InputTag( "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose"  ) ,
   eleMediumIdMap  = cms.InputTag( "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium" ) ,
   eleTightIdMap   = cms.InputTag( "egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight"  ) ,
   eleHEEPIdMap    = cms.InputTag( "egmGsfElectronIDs:heepElectronID-HEEPV51"                                  ) ,
   #eleMVAValuesMap = cms.InputTag( "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Phys14NonTrigValues"   ) ,

   #----- Jet Information ------------------------------------------------------------------------------
   jetlabel       = cms.VInputTag( 'slimmedJets' , 'slimmedJetsAK8' , 'slimmedJetsAK8') ,
   JetCollections = cms.vstring  ( 'JetInfo'     , 'AK8BosonJetInfo', 'CA8TopJetInfo' ) ,

   #----- MC Generation information --------------------------------------------------------------------
   genlabel                  = cms.VInputTag("prunedGenParticles"),
   genevtlabel               = cms.VInputTag("generator"),
   gtdigilabel               = cms.VInputTag("gtDigis"),

   PairCollection            = cms.untracked.int32(1),
   hltlabel                  = cms.VInputTag("TriggerResults::HLT"),
   offlinePVlabel            = cms.VInputTag("offlineSlimmedPrimaryVertices"),#CMSSW73X "offlinePrimaryVertices"),
   offlinePVBSlabel          = cms.VInputTag("offlinePrimaryVerticesWithBS"),# CMSSW73X"offlinePrimaryVerticesWithBS"),
   offlineBSlabel            = cms.VInputTag("offlineBeamSpot"),
   pfCands                   = cms.InputTag("packedPFCandidates"),
   puInfoLabel               = cms.VInputTag("addPileupInfo"),
   
   EIDMVAInputTags = cms.vstring(
      'dataEIDMVA/Electrons_BDTG_NonTrigV0_Cat1.weights.xml' ,
      'dataEIDMVA/Electrons_BDTG_NonTrigV0_Cat2.weights.xml' ,
      'dataEIDMVA/Electrons_BDTG_NonTrigV0_Cat3.weights.xml' ,
      'dataEIDMVA/Electrons_BDTG_NonTrigV0_Cat4.weights.xml' ,
      'dataEIDMVA/Electrons_BDTG_NonTrigV0_Cat5.weights.xml' ,
      'dataEIDMVA/Electrons_BDTG_NonTrigV0_Cat6.weights.xml' ,
      'dataEIDMVA/Electrons_BDTG_TrigV0_Cat1.weights.xml'    ,
      'dataEIDMVA/Electrons_BDTG_TrigV0_Cat2.weights.xml'    ,
      'dataEIDMVA/Electrons_BDTG_TrigV0_Cat3.weights.xml'    ,
      'dataEIDMVA/Electrons_BDTG_TrigV0_Cat4.weights.xml'    ,
      'dataEIDMVA/Electrons_BDTG_TrigV0_Cat5.weights.xml'    ,
      'dataEIDMVA/Electrons_BDTG_TrigV0_Cat6.weights.xml'
   ),

   IncludeL7           = cms.untracked.bool(False),
   SelectionParameters = defaultObjectParameters.clone(),
   Debug               = cms.untracked.int32(100),
)

