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

process.p = cms.Path(process.tree)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

