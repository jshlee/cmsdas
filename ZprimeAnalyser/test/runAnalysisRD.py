import FWCore.ParameterSet.Config as cms

process = cms.Process("ZprimeAnalyser")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.options.allowUnscheduled = cms.untracked.bool(True)
process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
process.source.fileNames.append('file:/cmsdas/scratch/jlee/SingleMuon/Run2015B-PromptReco-v1/MINIAOD/089D049E-262D-E511-85A7-02163E0146EB.root')

import FWCore.PythonUtilities.LumiList as LumiList
process.source.lumisToProcess = LumiList.LumiList(filename = 'Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt').getVLuminosityBlockRange()
### for electron ID
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')
from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)
process.load('RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff')
setupVIDSelection(process.egmGsfElectronIDs,process.heepElectronID_HEEPV60)
process.addHEEPID = cms.EDAnalyzer('VIDUsageExample',
     eles = cms.InputTag("slimmedElectrons"),
     id = cms.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV60"),
)

### analysis 
process.tree = cms.EDAnalyzer("ZprimeAnalyser",
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    muons = cms.InputTag("slimmedMuons"),
    elecs = cms.InputTag("slimmedElectrons"),
    jets = cms.InputTag("slimmedJets"),
    mets = cms.InputTag("slimmedMETs"),
    mcLabel = cms.InputTag("prunedGenParticles"),
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("out_tree.root"
))

process.p = cms.Path(process.egmGsfElectronIDSequence * process.addHEEPID * process.tree)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

