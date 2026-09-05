"""
Smoke test for nirikshak-worker service.
"""

import numpy as np
from apps.worker.main import InspectionPipelineWorker
from nirikshak_shared.models.contracts import InspectionRequest
from nirikshak_shared.models.primitives import InspectionStatus, OverallVerdict


def test_pipeline_worker_blurry_rejection():
    worker = InspectionPipelineWorker()
    req = InspectionRequest(inspection_id="insp_blur_001")
    blurry_img = np.full((100, 100, 3), 128, dtype=np.uint8)

    res = worker.process_inspection(req, blurry_img)
    assert res.status == InspectionStatus.REJECTED_QUALITY
    assert not res.quality_gate_passed
    assert res.overall_verdict == OverallVerdict.INCONCLUSIVE


def test_pipeline_worker_valid_image():
    worker = InspectionPipelineWorker()
    req = InspectionRequest(inspection_id="insp_ok_001")
    textured_img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)

    res = worker.process_inspection(req, textured_img)
    assert res.status == InspectionStatus.SUCCESS
    assert res.quality_gate_passed
    assert len(res.rule_evaluations) > 0
