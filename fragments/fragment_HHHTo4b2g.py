import FWCore.ParameterSet.Config as cms


# link to datacards: 
# https://github.com/cms-sw/genproductions/tree/da9674a3507c727dfd7042001b989782859101d6/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Higgs/tth01j_5f_ckm_NLO_FXFX_MH

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/isilon/data/users/mstamenk/eos-triple-h/gridpacks/GF_HHH_SM_c3_0_d4_0_no_b_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    generateConcurrently = cms.untracked.bool(True),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

#Link to GS fragment
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
	maxEventsToPrint = cms.untracked.int32(1),
	pythiaPylistVerbosity = cms.untracked.int32(1),
	filterEfficiency = cms.untracked.double(1.0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	comEnergy = cms.double(13000.),
	PythiaParameters = cms.PSet(
	pythia8CommonSettingsBlock,
	pythia8CP5SettingsBlock,
	pythia8PSweightsSettingsBlock,
	pythia8aMCatNLOSettingsBlock,
  	processParameters = cms.vstring(
            '25:m0 = 125.0',
            '25:onMode = off',
            '25:onIfMatch = 5 -5', #H decay to b
            '25:onIfMatch = 22 22', #H decay to tau
            'ResonanceDecayFilter:filter = on',
            'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
            'ResonanceDecayFilter:mothers = 25', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
            'ResonanceDecayFilter:daughters = 5,5,5,5,22,22',
  ),
	parameterSets = cms.vstring('pythia8CommonSettings',
		'pythia8CP5Settings',
		'pythia8PSweightsSettings',
		'pythia8aMCatNLOSettings',
		'processParameters',
	)
  )
)

ProductionFilterSequence = cms.Sequence(generator)

