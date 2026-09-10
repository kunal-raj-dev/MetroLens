"""
MetroLens API Gateway: End-to-End Inspection Pipeline Orchestrator.
Coordinates:
1. Bounded ingestion (Magic bytes, 40MP cap, EXIF sanitization, SHA-256 digest).
2. Ephemeral Spool Session Lifecycle (SpoolService, isolated sandbox directories).
3. Image Quality Pre-Flight Gate (Laplacian blur variance, specular glare thresholding).
4. Optical Metric Scale Calibration (Fiducial reference detection and mm/px conversion).
5. Multilingual OCR Perception (OCRService via PaddleOCR ONNX Runtime; failures create no assessment).
6. Deterministic Entity Normalization (TokenNormalizer regex/CTC parsing into CanonicalDeclaration).
7. Master Statutory Rules Engine (StatutoryRuleEngine: Rule 6(1), Rule 6(11) USP, Rule 7 Font Height, Rule 26/3 Exemptions).
8. Conservative single-panel review; no officer notice issuance.
9. Visual Forensic Evidence Crops (PIL spatial cropping and base64 data URI serialization).
10. Granular stage latency telemetry.
"""

import base64
import hashlib
import io
import logging
import math
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image
from fastapi import HTTPException
from decimal import Decimal, ROUND_HALF_UP

from apps.api.middleware.security import ImageSecurityValidator
from apps.api.schemas import (
    CalibrationInfo,
    DeclarationsInfo,
    EvidenceCrop,
    ExemptionStatus,
    FontHeightAudit,
    ImageMetadata,
    ImprovementNoticeInfo,
    InspectionResponse,
    OCRBoundingBox,
    OCRObservation,
    Rule6MandatoryStatus,
    RuleEvaluationsGroup,
    TelemetryInfo,
    TelemetryStages,
    USPAudit,
)
from apps.api.services.spool_service import SpoolService, spool_service

from nirikshak_calibration import (
    compute_scale_factor,
    CalibrationStatus,
    detect_anchor,
    AnchorType as CalibrationAnchorType,
    AnchorDetectionStatus,
)
from nirikshak_rules_engine.normalizer import TokenNormalizer
from nirikshak_rules_engine.rule_engine import StatutoryRuleEngine
from nirikshak_rules_engine.schemas import (
    CanonicalDeclaration,
    ComplianceEvaluationResult,
    ComplianceState,
    MetricScaleResult,
    OCRToken as RulesOCRToken,
    EvidenceCropMetadata,
)
from nirikshak_vision import check_image_quality

logger = logging.getLogger("metrolens.pipeline")


class PipelineOrchestrator:
    """
    Coordinates image perception and preliminary rule evaluation.
    The HTTP route serializes CPU processing; latency depends on the image and host.
    """

    def __init__(
        self,
        security_gate: Optional[Any] = None,
        spooler: Optional[SpoolService] = None,
        rule_engine: Optional[StatutoryRuleEngine] = None,
        normalizer: Optional[TokenNormalizer] = None,
    ):
        self.security_gate = security_gate or ImageSecurityValidator
        self.spooler = spooler or spool_service
        self.rule_engine = rule_engine or StatutoryRuleEngine()
        self.normalizer = normalizer or TokenNormalizer()
        self._ocr_service = None
        self._ocr_initialized = False

    def _get_ocr_service(self) -> Optional[Any]:
        """Lazy-loads OCRService singleton safely; returns None if ONNX weights are missing."""
        if not self._ocr_initialized:
            try:
                from nirikshak_ocr.service import OCRService
                self._ocr_service = OCRService.get_instance()
                logger.info("OCRService successfully connected to PipelineOrchestrator.")
            except Exception as e:
                logger.warning(
                    "OCRService ONNX runtime unavailable (models not found or offline mode): %s. "
                    "No assessment will be created.",
                    e,
                )
                self._ocr_service = None
            self._ocr_initialized = True
        return self._ocr_service

    def orchestrate_inspection(
        self,
        image_bytes: bytes,
        filename: str = "upload.jpg",
        anchor_type: str = "INR_10_COIN",
        panel_type: str = "FRONT_PDP",
        officer_id: str = "Unverified operator",
    ) -> InspectionResponse:
        """
        Executes synchronous end-to-end inspection pipeline.
        
        Args:
            image_bytes: Raw binary image payload.
            filename: Client-provided asset filename.
            anchor_type: Fiducial calibration reference ("INR_10_COIN", "ISO_CARD", "NONE").
            panel_type: Package view ("FRONT_PDP", "BACK_INFO", "ALL_IN_ONE").
            officer_id: Server-supplied operator attribution, not verified officer identity.

        Returns:
            Authoritative InspectionResponse conforming to docs/API_CONTRACT.md.
        """
        total_start = time.perf_counter()
        inspection_id = f"INSP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex.upper()}"
        logger.info("Starting inspection %s for file '%s' (%d bytes)", inspection_id, filename, len(image_bytes))

        # ---------------------------------------------------------------------
        # 0. Ingestion Security & Ephemeral Spooling
        # ---------------------------------------------------------------------
        sanitized_record = self.security_gate.sanitize_and_verify(image_bytes)
        sanitized_bytes = sanitized_record.sanitized_bytes
        image_hash = sanitized_record.raw_sha256
        img_width = sanitized_record.width
        img_height = sanitized_record.height

        # Open PIL Image for subsequent cropping and dimension checks
        pil_image = Image.open(io.BytesIO(sanitized_bytes))
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        # Convert to BGR numpy array for CV2 and Vision operations
        img_np = np.array(pil_image)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # ---------------------------------------------------------------------
        # 1. Quality Gate Pre-flight
        # ---------------------------------------------------------------------
        t_stage1 = time.perf_counter()
        q_result = check_image_quality(img_bgr)
        stage_quality_ms = (time.perf_counter() - t_stage1) * 1000.0
        if not q_result.passed:
            raise HTTPException(422, "Image quality is insufficient for reliable inspection. Retake a sharp photo without glare.")

        image_metadata = ImageMetadata(
            filename=filename,
            width_px=img_width,
            height_px=img_height,
            sha256_hash=image_hash,
            is_quality_valid=q_result.passed,
            blur_score=round(q_result.laplacian_variance, 2),
            glare_percentage=round(q_result.glare_ratio * 100.0, 2),
        )

        # ---------------------------------------------------------------------
        # 2. Metric Scale Calibration
        # ---------------------------------------------------------------------
        t_stage2 = time.perf_counter()
        calibration_info, metric_scale_result = self._perform_calibration(
            img_bgr=img_bgr,
            anchor_type=anchor_type,
            img_width=img_width,
            img_height=img_height,
        )
        stage_calibration_ms = (time.perf_counter() - t_stage2) * 1000.0

        # ---------------------------------------------------------------------
        # 3. Multilingual OCR Perception
        # ---------------------------------------------------------------------
        t_stage3 = time.perf_counter()
        extracted_tokens = self._extract_ocr_tokens(
            img_bgr=img_bgr,
            image_id=inspection_id,
        )
        stage_ocr_ms = (time.perf_counter() - t_stage3) * 1000.0

        # ---------------------------------------------------------------------
        # 4. Token Normalization
        # ---------------------------------------------------------------------
        t_stage4 = time.perf_counter()
        declarations = self.normalizer.normalize(extracted_tokens)
        stage_norm_ms = (time.perf_counter() - t_stage4) * 1000.0

        # ---------------------------------------------------------------------
        # 5. Master Statutory Rules Engine
        # ---------------------------------------------------------------------
        t_stage5 = time.perf_counter()
        # Measure font height from tokens if available
        # OCR line boxes are not measured numeral glyph heights. Until reliable
        # glyph segmentation and package-area measurement exist, Rule 7 needs review.
        measured_font_height_mm = None

        compliance_result = self.rule_engine.evaluate(
            decl=declarations,
            scale=metric_scale_result,
            inspection_id=inspection_id,
            measured_font_height_mm=measured_font_height_mm,
        )
        # This endpoint observes one photograph, not the complete physical package.
        # OCR absence is not proof that a declaration is absent from other panels.
        for rule in compliance_result.rule_evaluations:
            if rule.status == "FAIL" and rule.observed_value in (None, "Not detected"):
                rule.status = "REVIEW"
                rule.is_compliant = False
                rule.notes = "Not observed on the photographed panel; inspect the remaining package panels before deciding compliance."
        if compliance_result.overall_verdict == ComplianceState.NON_COMPLIANT.value:
            compliance_result.overall_verdict = ComplianceState.RED.value
            compliance_result.primary_legal_summary = (
                "Potential non-compliance requires review of the photographed panel and any unobserved package panels. "
                "This image-only screening does not establish whole-package compliance or a statutory violation."
            )
        if any(token.confidence < 0.60 for token in extracted_tokens):
            # The normalizer has no field-level confidence provenance yet. A weak
            # token must therefore block conclusions, including a quantity exemption.
            compliance_result.overall_verdict = ComplianceState.AMBER.value
            compliance_result.verdict_badge_color = "amber"
            compliance_result.primary_legal_summary = (
                "Manual review required: OCR confidence is below 0.60 for part of the observed text. "
                "No compliance conclusion or package exemption is established from these observations."
            )
            for rule in compliance_result.rule_evaluations:
                rule.status = "REVIEW"
                rule.is_compliant = False
                rule.notes = "Low OCR confidence prevents confirming this check. Verify the text against the original image."
        # This MVP has neither individual officer identity nor an issuance workflow.
        compliance_result.improvement_notice = None
        if (compliance_result.overall_verdict == ComplianceState.COMPLIANT.value
                and any(r.status == "REVIEW" for r in compliance_result.rule_evaluations)):
            compliance_result.overall_verdict = ComplianceState.AMBER.value
            compliance_result.verdict_badge_color = "amber"
            compliance_result.primary_legal_summary = "Manual review required: one or more checks lack sufficient measurement or declaration evidence."
        compliance_result.sha256_hash = image_hash
        stage_rule_ms = (time.perf_counter() - t_stage5) * 1000.0

        # ---------------------------------------------------------------------
        # 6. Visual Forensic Evidence Packaging
        # ---------------------------------------------------------------------
        t_stage6 = time.perf_counter()
        evidence_crops = self._generate_evidence_crops(
            pil_image=pil_image,
            tokens=extracted_tokens,
            declarations=declarations,
            scale=metric_scale_result,
        )
        compliance_result.evidence_crops = [EvidenceCropMetadata(**crop.model_dump()) for crop in evidence_crops]
        stage_evidence_ms = (time.perf_counter() - t_stage6) * 1000.0

        # ---------------------------------------------------------------------
        # 7. Telemetry & Response Packaging
        # ---------------------------------------------------------------------
        total_duration_ms = (time.perf_counter() - total_start) * 1000.0

        rule_eval_group = self._build_rule_evaluations_group(compliance_result, declarations, metric_scale_result)
        improvement_notice_info = self._build_improvement_notice_info(compliance_result)
        declarations_info = self._build_declarations_info(declarations)

        verdict_val = (
            compliance_result.overall_verdict.value
            if hasattr(compliance_result.overall_verdict, "value")
            else str(compliance_result.overall_verdict)
        )
        summary_reason = compliance_result.primary_legal_summary

        response = InspectionResponse(
            inspection_id=inspection_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            state=verdict_val,
            summary_reason=summary_reason,
            image_metadata=image_metadata,
            calibration=calibration_info,
            declarations=declarations_info,
            rule_evaluations=rule_eval_group,
            improvement_notice=improvement_notice_info,
            evidence_crops=evidence_crops,
            ocr_observations=[OCRObservation(
                token_id=token.token_id, text=token.text, confidence=token.confidence,
                bounding_box=OCRBoundingBox(x_min=token.bbox[0], y_min=token.bbox[1],
                    x_max=token.bbox[2], y_max=token.bbox[3]),
                polygon=token.polygon, script=token.script,
            ) for token in extracted_tokens],
            telemetry=TelemetryInfo(
                total_duration_ms=round(total_duration_ms, 2),
                stages_ms=TelemetryStages(
                    quality_gate=round(stage_quality_ms, 2),
                    metric_calibration=round(stage_calibration_ms, 2),
                    ocr_perception=round(stage_ocr_ms, 2),
                    normalization=round(stage_norm_ms, 2),
                    rule_engine=round(stage_rule_ms, 2),
                    evidence_packaging=round(stage_evidence_ms, 2),
                ),
            ),
        )

        logger.info(
            "Inspection %s completed in %.2f ms (verdict: %s)",
            inspection_id,
            total_duration_ms,
            response.state,
        )
        # Retain original bytes and the privacy-safe derivative separately. Failed
        # inspections never acquire a successful record or a retained spool session.
        extension = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}[sanitized_record.format]
        spool_session = self.spooler.create_session(inspection_id)
        try:
            self.spooler.save_raw_image(inspection_id, image_bytes, extension)
            self.spooler.save_sanitized_image(inspection_id, sanitized_bytes, extension)
            spool_session.metadata.update({
                "compliance_result": compliance_result,
                "raw_sha256": image_hash,
                "sanitized_sha256": hashlib.sha256(sanitized_bytes).hexdigest(),
                "raw_size_bytes": len(image_bytes),
                "sanitized_size_bytes": len(sanitized_bytes),
                "actor": officer_id,
                "panel_type": panel_type,
            })
        except Exception:
            self.spooler.purge_session(inspection_id)
            raise
        return response

    # =========================================================================
    # Pipeline Sub-stages Implementation
    # =========================================================================

    def _perform_calibration(
        self,
        img_bgr: np.ndarray,
        anchor_type: str,
        img_width: int,
        img_height: int,
    ) -> Tuple[CalibrationInfo, Optional[MetricScaleResult]]:
        """Performs fiducial marker calibration via Member 2 CV or defaults to uncalibrated."""
        anchor_upper = (anchor_type or "NONE").upper()

        target_anchor: Optional[Union[CalibrationAnchorType, bool]] = None
        if anchor_upper in ("INR_10_COIN", "COIN_INR_10"):
            target_anchor = CalibrationAnchorType.COIN_INR_10
        elif anchor_upper in ("ISO_CARD", "ID1_CARD"):
            target_anchor = CalibrationAnchorType.ID1_CARD
        elif anchor_upper in ("AUTO",):
            target_anchor = None
        elif anchor_upper in ("NONE", "NO_ANCHOR"):
            target_anchor = False

        if target_anchor is not False:
            try:
                detection_res = detect_anchor(img_bgr, anchor_type=target_anchor)
                if detection_res.status == AnchorDetectionStatus.SUCCESS and detection_res.geometry:
                    if hasattr(detection_res.geometry, "major_axis_px"):
                        known_marker_mm = 27.0
                        marker_px = detection_res.geometry.major_axis_px
                        marker_name = "INR_10_COIN"
                    else:
                        known_marker_mm = 85.60
                        marker_px = max(detection_res.geometry.width_px, detection_res.geometry.height_px)
                        marker_name = "ISO_CARD"

                    scale_outcome = compute_scale_factor(
                        measured_marker_pixels=marker_px,
                        known_marker_mm=known_marker_mm,
                        marker_name=marker_name,
                    )

                    if scale_outcome.status == CalibrationStatus.CALIBRATED and scale_outcome.scale_factor_mm_per_pixel:
                        scale_mm_per_px = scale_outcome.scale_factor_mm_per_pixel

                        detected_type_str = "INR_10_COIN" if marker_name == "INR_10_COIN" else "ISO_CARD"
                        calib_info = CalibrationInfo(
                            is_calibrated=True,
                            anchor_type=detected_type_str,
                            coin_detected=(marker_name == "INR_10_COIN"),
                            scale_mm_per_px=round(scale_mm_per_px, 4),
                            pdp_width_mm=None,
                            pdp_height_mm=None,
                            pdp_area_cm2=None,
                            calibration_confidence=round(detection_res.confidence, 2),
                        )

                        tilt_deg = None
                        if hasattr(detection_res.geometry, "aspect_ratio") and detection_res.geometry.aspect_ratio is not None:
                            ar = min(1.0, float(detection_res.geometry.aspect_ratio))
                            tilt_deg = round(math.degrees(math.acos(ar)), 1)

                        metric_scale = MetricScaleResult(
                            is_calibrated=True,
                            scale_factor_mm_per_px=scale_mm_per_px,
                            pdp_area_sqcm=None,
                            anchor_type_detected=detected_type_str,
                            tilt_angle_deg=tilt_deg,
                            is_cylindrical=False,
                        )
                        return calib_info, metric_scale
            except Exception as exc:
                logger.warning("Optical anchor calibration failed: %s; falling back to uncalibrated.", exc)

        # Uncalibrated baseline (Zero Scale Fabrication)
        calib_info = CalibrationInfo(
            is_calibrated=False,
            anchor_type="NONE" if anchor_upper == "NONE" else anchor_upper,
            coin_detected=False,
            scale_mm_per_px=None,
            pdp_width_mm=None,
            pdp_height_mm=None,
            pdp_area_cm2=None,
            calibration_confidence=None,
        )
        metric_scale = MetricScaleResult(
            is_calibrated=False,
            scale_factor_mm_per_px=None,
            pdp_area_sqcm=None,
            anchor_type_detected="NONE" if anchor_upper == "NONE" else anchor_upper,
            tilt_angle_deg=None,
            is_cylindrical=False,
        )
        return calib_info, metric_scale

    def _extract_ocr_tokens(
        self,
        img_bgr: np.ndarray,
        image_id: str,
    ) -> List[RulesOCRToken]:
        """Only real inference may contribute observed evidence."""
        ocr_service = self._get_ocr_service()
        if ocr_service is None:
            raise HTTPException(503, "OCR is unavailable. Contact the service administrator.")
        try:
            ocr_result = ocr_service.extract(img_bgr, image_id=image_id)
            tokens = [
                RulesOCRToken(
                    token_id=tok.token_id, text=tok.text, confidence=tok.confidence,
                    bbox=list(tok.bbox), polygon=getattr(tok, "polygon", None),
                    script=getattr(tok, "script", "unknown"),
                    raw_pixel_height=getattr(tok, "raw_pixel_height", None),
                    model_name=getattr(tok, "model_name", ""),
                )
                for tok in ocr_result.tokens if tok.text.strip()
            ]
        except Exception as exc:
            logger.warning("OCR inference failed: %s", exc)
            raise HTTPException(503, "OCR processing failed. No assessment was created.") from exc
        if not tokens:
            raise HTTPException(422, "No readable text was detected. Retake a closer, sharper packaging photograph.")
        return tokens

    def _generate_evidence_crops(
        self,
        pil_image: Image.Image,
        tokens: List[RulesOCRToken],
        declarations: CanonicalDeclaration,
        scale: Optional[MetricScaleResult],
    ) -> List[EvidenceCrop]:
        """
        Extracts high-resolution visual evidence crops for key declarations.
        Returns serialized base64 data URIs.
        """
        img_w, img_h = pil_image.size
        crops: List[EvidenceCrop] = []

        field_patterns = [
            ("net_quantity", "Net Quantity & USP Crop", ["net", "qty", "quantity", "शुद्ध"]),
            ("mrp", "MRP & Tax Qualifier Crop", ["mrp", "price", "मूल्य", "₹", "rs"]),
            ("usp", "Unit Sale Price Crop", ["usp", "unit", "इकाई"]),
            ("manufacturer", "Manufacturer Declaration Crop", ["mfg", "mfr", "packed", "manufactured", "निर्माता"]),
        ]

        for field_name, label, keywords in field_patterns:
            matched_tok = None
            for tok in tokens:
                t_lower = tok.text.lower()
                if any(kw in t_lower for kw in keywords):
                    matched_tok = tok
                    break

            if matched_tok:
                bx1, by1, bx2, by2 = matched_tok.bbox
                # Add 8px padding
                pad = 8
                x1 = min(img_w, max(0, int(min(bx1, bx2) - pad)))
                y1 = min(img_h, max(0, int(min(by1, by2) - pad)))
                x2 = min(img_w, int(max(bx1, bx2) + pad))
                y2 = min(img_h, int(max(by1, by2) + pad))
                if x2 <= x1 or y2 <= y1:
                    continue
                w = x2 - x1
                h = y2 - y1

                cropped = pil_image.crop((x1, y1, x2, y2))
                cropped.thumbnail((640, 320))
                buf = io.BytesIO()
                cropped.save(buf, format="JPEG", quality=85)
                b64_data = base64.b64encode(buf.getvalue()).decode("ascii")
                data_uri = f"data:image/jpeg;base64,{b64_data}"

                measured_h = None

                crops.append(
                    EvidenceCrop(
                        field_name=field_name,
                        source_token_id=matched_tok.token_id,
                        label=label,
                        bbox_px=[x1, y1, w, h],
                        measured_height_mm=measured_h,
                        confidence=matched_tok.confidence,
                        crop_base64=data_uri,
                    )
                )

        return crops

    def _build_declarations_info(self, decl: CanonicalDeclaration) -> DeclarationsInfo:
        """Translates CanonicalDeclaration into API DeclarationsInfo schema."""
        return DeclarationsInfo(
            commodity_name=decl.commodity_name,
            mrp_inr=decl.mrp_inr,
            tax_qualifier_present=decl.tax_qualifier_present,
            net_quantity_value=decl.net_quantity_value,
            net_quantity_unit=decl.net_quantity_unit.value if decl.net_quantity_unit else None,
            declared_usp_value=decl.declared_usp_value,
            declared_usp_unit=decl.declared_usp_unit,
            mfg_month=decl.mfg_month,
            mfg_year=decl.mfg_year,
            manufacturer_name=decl.manufacturer_name,
            manufacturer_pincode=decl.manufacturer_pincode,
            consumer_care_email=decl.consumer_care_email,
            consumer_care_phone=decl.consumer_care_phone,
            country_of_origin=decl.country_of_origin,
        )

    def _build_rule_evaluations_group(
        self,
        result: ComplianceEvaluationResult,
        decl: CanonicalDeclaration,
        scale: Optional[MetricScaleResult],
    ) -> RuleEvaluationsGroup:
        """Constructs the nested rule_evaluations structure specified in API Contract."""
        evals_by_rule = {r.rule_id: r for r in result.rule_evaluations}

        # 1. Rule 6(1) Mandatory Status
        missing: List[str] = []
        details: Dict[str, str] = {}

        field_mapping = {
            "manufacturer_details": "LMPC-R06-MFR-001",
            "net_quantity": "LMPC-R06-QTY-001",
            "mrp": "LMPC-R06-MRP-001",
            "usp": "LMPC-R06-USP-001",
            "mfg_date": "LMPC-R06-DATE-001",
            "consumer_care": "LMPC-R06-CARE-001",
        }

        for key, rid in field_mapping.items():
            rec = evals_by_rule.get(rid)
            if rec:
                status = rec.status
                details[key] = status
                if status == "FAIL":
                    missing.append(key)
            else:
                details[key] = "NOT_APPLICABLE" if result.overall_verdict == ComplianceState.EXEMPTED.value else "REVIEW"

        r6_overall = "FAIL" if missing else ("REVIEW" if "REVIEW" in details.values() else (
            "NOT_APPLICABLE" if all(v == "NOT_APPLICABLE" for v in details.values()) else "PASS"))
        r6_status = Rule6MandatoryStatus(
            overall_status=r6_overall,
            missing_declarations=missing,
            details=details,
        )

        # 2. USP Audit
        usp_rec = evals_by_rule.get("LMPC-R06-USP-001")
        not_evaluated_status = "NOT_APPLICABLE" if result.overall_verdict == ComplianceState.EXEMPTED.value else "REVIEW"
        usp_status = usp_rec.status if usp_rec else not_evaluated_status
        usp_compliant = usp_status == "PASS"
        usp_notes = usp_rec.notes if usp_rec else "This check was not evaluated."
        expected_usp = None
        discrepancy_pct = None
        denominator = None
        if decl.net_quantity_value and decl.net_quantity_unit and decl.mrp_inr:
            denominator, quantity, _ = self.rule_engine.usp_validator.determine_statutory_denominator(
                decl.net_quantity_value, decl.net_quantity_unit,
            )
            if quantity and quantity > 0:
                expected = (Decimal(str(decl.mrp_inr)) / quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                expected_usp = float(expected)
                if expected > 0 and decl.declared_usp_value is not None:
                    discrepancy_pct = float(abs(Decimal(str(decl.declared_usp_value)) - expected) / expected * 100)

        usp_audit = USPAudit(
            status=usp_status,
            is_compliant=usp_compliant,
            declared_usp=decl.declared_usp_value,
            expected_usp=expected_usp,
            discrepancy_pct=discrepancy_pct,
            standard_denominator=denominator,
            notes=usp_notes,
        )

        # 3. Font Height Audit
        font_rec = evals_by_rule.get("LMPC-R07-FONT-001")
        pdp_area = scale.pdp_area_sqcm if (scale and scale.is_calibrated) else None
        font_status = font_rec.status if font_rec else not_evaluated_status
        font_compliant = font_status == "PASS"
        font_deficit = font_rec.deficit_mm if font_rec else None
        bod_applied = font_rec.benefit_of_doubt_applied if font_rec else False

        font_audit = FontHeightAudit(
            status=font_status,
            notes=font_rec.notes if font_rec else "This check was not evaluated.",
            is_compliant=font_compliant,
            pdp_area_cm2=pdp_area,
            statutory_min_height_mm=None,
            measured_net_qty_height_mm=None,
            deficit_mm=font_deficit,
            benefit_of_doubt_applied=bod_applied,
        )

        # 4. Exemption Status
        exemption_status = ExemptionStatus(
            is_exempt=(result.overall_verdict == ComplianceState.EXEMPTED),
            statutory_clause=None,
        )

        return RuleEvaluationsGroup(
            rule6_mandatory_status=r6_status,
            usp_audit=usp_audit,
            font_height_audit=font_audit,
            exemption_status=exemption_status,
        )

    def _build_improvement_notice_info(
        self, result: ComplianceEvaluationResult
    ) -> Optional[ImprovementNoticeInfo]:
        """Constructs ImprovementNoticeInfo if non-compliant."""
        if not result.improvement_notice or not result.improvement_notice.recommended:
            return None

        notice = result.improvement_notice
        return ImprovementNoticeInfo(
            recommended=notice.recommended,
            act_provision=notice.act_provision,
            cure_period_days=notice.cure_period_days,
            statutory_grounds=notice.statutory_grounds,
        )


# Singleton instance
pipeline_orchestrator = PipelineOrchestrator()
orchestrate_inspection = pipeline_orchestrator.orchestrate_inspection
