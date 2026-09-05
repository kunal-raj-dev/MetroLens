"""
Nirikshak Worker Service: Synchronous inspection pipeline orchestration worker.
Executes the full 8-stage inspection flow deterministically:
1. Input Normalization & Cryptographic Digest (SHA-256)
2. Optical Quality Gate (Sharpness & Glare)
3. Optical Scale Calibration (Reference coin / Fiducial detection)
4. Multilingual Scene Text Extraction (OCRService)
5. Statutory Semantic Extraction (Rule 6 Declarations)
6. Metrological Measurement (Rule 7 Numeral Font Height)
7. Deterministic Legal Rule Evaluation (Rule 6 presence & Rule 7 Table-I)
8. Cryptographic Evidence DAG & Master Result Assembly
"""

import time
import hashlib
from typing import Union, Optional, Dict, Any, List
from pathlib import Path
import numpy as np
import cv2

from nirikshak_shared.models.contracts import (
    InspectionRequest,
    InspectionResult,
    OCRObservation,
    DeclarationField,
    MeasurementResult,
    RuleEvaluation,
    EvidenceItem,
    InspectionError,
)
from nirikshak_shared.models.primitives import (
    InspectionStatus,
    OverallVerdict,
    CalibrationStatus,
    PanelName,
    ObservedValue,
    RuleVerdict,
    BoundingBox,
)
from nirikshak_vision import check_image_quality
from nirikshak_calibration import detect_reference_and_calibrate, CalibrationOutcome
from nirikshak_ocr import OCRService, OCRError
from nirikshak_extraction import DeclarationExtractor
from nirikshak_measurement import calculate_font_height_mm
from nirikshak_rules_engine import NirikshakRulesEngine
from nirikshak_evidence import compute_sha256, create_evidence_item


class InspectionPipelineWorker:
    """
    Executes the multi-stage inspection pipeline deterministically.
    Synchronous in-process worker (Web MVP architecture).
    """

    def __init__(self):
        self.ocr_service = OCRService.get_instance()
        self.extractor = DeclarationExtractor()
        self.rules_engine = NirikshakRulesEngine()
        self.last_timings: Dict[str, float] = {}


    def process_inspection(
        self,
        request: InspectionRequest,
        image_input: Union[np.ndarray, bytes, bytearray, str, Path],
    ) -> InspectionResult:
        """
        Executes end-to-end synchronous inspection pipeline on image input.
        Records granular stage latencies in telemetry timings.
        """
        stages_ms: Dict[str, float] = {}
        t_total_start = time.perf_counter()

        # 1. Ingestion & Normalization
        t0 = time.perf_counter()
        if isinstance(image_input, (bytes, bytearray)):
            image_bytes = bytes(image_input)
            image_array = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            image_sha256 = compute_sha256(image_bytes)
        elif isinstance(image_input, np.ndarray):
            image_array = image_input.copy()
            success, enc = cv2.imencode(".jpg", image_array)
            image_bytes = enc.tobytes() if success else b""
            image_sha256 = request.image_sha256 or (compute_sha256(image_bytes) if image_bytes else "0" * 64)
        elif isinstance(image_input, (str, Path)):
            with open(image_input, "rb") as f:
                image_bytes = f.read()
            image_array = cv2.imread(str(image_input))
            image_sha256 = compute_sha256(image_bytes)
        else:
            return InspectionResult(
                inspection_id=request.inspection_id,
                status=InspectionStatus.FAILED_PROCESSING,
                image_sha256="0" * 64,
                overall_verdict=OverallVerdict.INCONCLUSIVE,
                quality_gate_passed=False,
                calibration_status=CalibrationStatus.UNCALIBRATED,
                errors=[
                    InspectionError(
                        error_code="INVALID_INPUT_TYPE",
                        stage="ingestion",
                        message=f"Unsupported image input type: {type(image_input)}",
                        is_fatal=True,
                    )
                ],
            )

        if image_array is None or image_array.size == 0:
            return InspectionResult(
                inspection_id=request.inspection_id,
                status=InspectionStatus.FAILED_PROCESSING,
                image_sha256=image_sha256 if 'image_sha256' in locals() else "0" * 64,
                overall_verdict=OverallVerdict.INCONCLUSIVE,
                quality_gate_passed=False,
                calibration_status=CalibrationStatus.UNCALIBRATED,
                errors=[
                    InspectionError(
                        error_code="CORRUPT_IMAGE_PAYLOAD",
                        stage="ingestion",
                        message="Image could not be decoded; zero dimensions or corrupted buffer.",
                        is_fatal=True,
                    )
                ],
            )
        stages_ms["ingestion_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        # 2. Quality Gate
        t0 = time.perf_counter()
        qg = check_image_quality(image_array, min_laplacian_variance=50.0, max_glare_ratio=0.15)
        stages_ms["quality_gate_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        if not qg.passed:
            stages_ms["total_ms"] = round((time.perf_counter() - t_total_start) * 1000.0, 2)
            self.last_timings = stages_ms
            return InspectionResult(
                inspection_id=request.inspection_id,
                status=InspectionStatus.REJECTED_QUALITY,
                image_sha256=image_sha256,
                overall_verdict=OverallVerdict.INCONCLUSIVE,
                quality_gate_passed=False,
                calibration_status=CalibrationStatus.UNCALIBRATED,
                telemetry=stages_ms,
                errors=[
                    InspectionError(
                        error_code="QUALITY_REJECTED",
                        stage="quality_gate",
                        message=f"Image failed pre-flight quality check. Sharpness: {qg.laplacian_variance:.1f} (min 50.0), Glare: {qg.glare_ratio:.3f} (max 0.15).",
                        remediation_hint="Retake photograph in well-lit conditions with sharp focus and no flash glare.",
                        is_fatal=True,
                    )
                ],
            )


        # 3. Calibration
        t0 = time.perf_counter()
        calib = detect_reference_and_calibrate(image_array)
        stages_ms["calibration_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        # 4. OCR Perception
        t0 = time.perf_counter()
        try:
            ocr_result = self.ocr_service.extract(image_array, image_id=request.inspection_id)
            observations: List[OCRObservation] = ocr_result.to_observations()
        except OCRError as e:
            stages_ms["total_ms"] = round((time.perf_counter() - t_total_start) * 1000.0, 2)
            self.last_timings = stages_ms
            return InspectionResult(
                inspection_id=request.inspection_id,
                status=InspectionStatus.FAILED_PROCESSING,
                image_sha256=image_sha256,
                overall_verdict=OverallVerdict.INCONCLUSIVE,
                quality_gate_passed=True,
                calibration_status=calib.status,
                telemetry=stages_ms,
                errors=[
                    InspectionError(
                        error_code=getattr(e, "error_code", "OCR_ENGINE_ERROR"),
                        stage="ocr_perception",
                        message=str(e),
                        is_fatal=True,
                    )
                ],
            )

        stages_ms["ocr_perception_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        # 5. Semantic Declaration Extraction
        t0 = time.perf_counter()
        declarations: Dict[str, DeclarationField] = self.extractor.extract_declarations(observations)
        stages_ms["semantic_extraction_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        # 6. Physical Measurement (Font Height)
        t0 = time.perf_counter()
        measurements: Dict[str, MeasurementResult] = {}
        
        # Select net quantity token (or first available token) for numeral height audit
        net_qty_decl = declarations.get("net_quantity")
        candidate_token = None
        if net_qty_decl and net_qty_decl.source_token_ids:
            for obs in observations:
                if obs.token_id in net_qty_decl.source_token_ids:
                    candidate_token = obs
                    break
        elif observations:
            candidate_token = observations[0]

        if candidate_token:
            pixel_h = candidate_token.bounding_box.y_max - candidate_token.bounding_box.y_min
            meas = calculate_font_height_mm(
                pixel_height=pixel_h,
                scale_factor_mm_per_pixel=calib.scale_factor_mm_per_pixel,
            )
            meas.bounding_box = candidate_token.bounding_box
            measurements["net_quantity_font_height"] = meas

        stages_ms["measurement_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        # 7. Deterministic Legal Rule Evaluation
        t0 = time.perf_counter()
        font_meas = measurements.get("net_quantity_font_height")
        evals: List[RuleEvaluation] = self.rules_engine.evaluate_all(declarations, measurement=font_meas)
        stages_ms["rules_engine_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)

        # 8. Evidence DAG & Master Verdict Assembly
        t0 = time.perf_counter()
        evidence_chain: List[EvidenceItem] = []
        for field_name, decl in declarations.items():
            if decl.is_present and decl.bounding_box:
                ev_id = f"ev_decl_{field_name}_{decl.source_token_ids[0] if decl.source_token_ids else '0'}"
                norm_str = str(decl.normalized_value) if decl.normalized_value is not None else None
                obs_val = ObservedValue(
                    raw_text=decl.raw_text,
                    normalized_value=norm_str,
                    ocr_confidence=decl.confidence,
                )
                evidence_chain.append(
                    create_evidence_item(
                        evidence_id=ev_id,
                        image_sha256=image_sha256,
                        bounding_box=decl.bounding_box,
                        calibration_status=calib.status,
                        physical_scale_mm_per_pixel=calib.scale_factor_mm_per_pixel,
                        observed_value=obs_val,
                    )
                )

        has_fail = any(e.verdict == RuleVerdict.FAIL for e in evals)
        has_review = any(e.verdict == RuleVerdict.REVIEW for e in evals)

        if has_fail:
            overall_verdict = OverallVerdict.NON_COMPLIANT
        elif has_review or calib.status == CalibrationStatus.UNCALIBRATED:
            overall_verdict = OverallVerdict.SUSPECT_REVIEW
        else:
            overall_verdict = OverallVerdict.COMPLIANT

        stages_ms["evidence_assembly_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)
        stages_ms["total_ms"] = round((time.perf_counter() - t_total_start) * 1000.0, 2)
        self.last_timings = stages_ms

        return InspectionResult(
            inspection_id=request.inspection_id,
            status=InspectionStatus.SUCCESS,
            image_sha256=image_sha256,
            overall_verdict=overall_verdict,
            quality_gate_passed=True,
            calibration_status=calib.status,
            declarations=declarations,
            measurements=measurements,
            rule_evaluations=evals,
            evidence_chain=evidence_chain,
            telemetry=stages_ms,
            errors=[],
        )



def main():
    print("Nirikshak Worker Service initialized. Synchronous pipeline ready.")


if __name__ == "__main__":
    main()
