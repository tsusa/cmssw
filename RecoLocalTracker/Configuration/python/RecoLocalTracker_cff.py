import FWCore.ParameterSet.Config as cms

#
# Tracker Local Reco
# Initialize magnetic field
#
from RecoLocalTracker.SiStripRecHitConverter.SiStripRecHitConverter_cfi import *
from RecoLocalTracker.SiStripRecHitConverter.SiStripRecHitMatcher_cfi import *
from RecoLocalTracker.SiStripRecHitConverter.StripCPEfromTrackAngle_cfi import *
from RecoLocalTracker.SiStripZeroSuppression.SiStripZeroSuppression_cfi import *
from RecoLocalTracker.SiStripClusterizer.SiStripClusterizer_cfi import *
from RecoLocalTracker.SiPixelClusterizer.SiPixelClusterizerPreSplitting_cfi import *
from RecoLocalTracker.SiPixelDigiMorphing.SiPixelDigiMorphing_cfi import *
from RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi import *
from RecoLocalTracker.SubCollectionProducers.clustersummaryproducer_cfi import *

pixeltrackerlocalrecoTask = cms.Task(siPixelClustersPreSplitting,siPixelRecHitsPreSplitting)
pixeltrackerlocalrecoTask_withMorphing = cms.Task(siPixelDigisMorphed,siPixelClustersPreSplitting,siPixelRecHitsPreSplitting)


from Configuration.Eras.Modifier_run3_common_cff import run3_common
run3_common.toReplaceWith(pixeltrackerlocalrecoTask,pixeltrackerlocalrecoTask_withMorphing)

striptrackerlocalrecoTask = cms.Task(siStripZeroSuppression,siStripClusters,siStripMatchedRecHits)
trackerlocalrecoTask = cms.Task(pixeltrackerlocalrecoTask,striptrackerlocalrecoTask,clusterSummaryProducer)

pixeltrackerlocalreco = cms.Sequence(pixeltrackerlocalrecoTask)
striptrackerlocalreco = cms.Sequence(striptrackerlocalrecoTask)
trackerlocalreco = cms.Sequence(trackerlocalrecoTask)

from RecoLocalTracker.SiPhase2Clusterizer.phase2TrackerClusterizer_cfi import *
from RecoLocalTracker.Phase2TrackerRecHits.Phase2StripCPEGeometricESProducer_cfi import *
from RecoLocalTracker.SiPhase2VectorHitBuilder.siPhase2RecHitMatcher_cfi import *

_pixeltrackerlocalrecoTask_phase2 = pixeltrackerlocalrecoTask.copy()
_pixeltrackerlocalrecoTask_phase2.add(siPhase2Clusters)
phase2_tracker.toReplaceWith(pixeltrackerlocalrecoTask, _pixeltrackerlocalrecoTask_phase2)
phase2_tracker.toReplaceWith(trackerlocalrecoTask, trackerlocalrecoTask.copyAndExclude([striptrackerlocalrecoTask]))
