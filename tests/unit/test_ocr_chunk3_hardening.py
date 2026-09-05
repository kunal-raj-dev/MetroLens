"""
Phase 32 Hardening and Regression Tests for Chunk 3.
Verifies:
1. Default OCRConfig has preprocessing_mode == "raw" (canonical default baseline).
2. compute_routing_accuracy computes correct script routing percentage strictly independent of CER.
3. validate_manifest returns PASS_EMPTY_BLOCKED for empty blocked manifest and PASS_VALID_POPULATED for populated manifest.
4. Benchmark final_results.json records exactly 8 configurations and 72 total inference passes.
5. OCRResult routing_summary is properly populated and polygon coordinates remain invariant under default baseline.
"""

import json
from pathlib import Path
import pytest
import numpy as np

from nirikshak_ocr import (
    OCRConfig,
    OCREngine,
    compute_routing_accuracy,
    compute_cer,
    compute_wer
)
from tools.validate_dataset_manifest import validate_manifest


ROOT_DIR = Path(__file__).resolve().parents[2]


def test_default_config_is_raw_baseline():
    """Verify that OCRConfig defaults to raw preprocessing (canonical default baseline)."""
    cfg = OCRConfig()
    assert cfg.preprocessing_mode == "raw"
    assert cfg.preprocess_target == "crop"
    assert cfg.clahe_clip_limit == 2.0
    assert cfg.adaptive_contrast_threshold == 35.0


def test_compute_routing_accuracy_independent_of_cer():
    """Verify compute_routing_accuracy calculates accurate script routing metrics isolated from CER/WER."""
    # Perfect routing decisions
    decisions_perfect = [
        ("latin", "latin"),
        ("devanagari", "devanagari"),
        ("latin", "latin"),
        ("devanagari", "devanagari")
    ]
    res_perfect = compute_routing_accuracy(decisions_perfect)
    assert res_perfect["total_routed"] == 4
    assert res_perfect["correct_routed"] == 4
    assert res_perfect["incorrect_routed"] == 0
    assert res_perfect["routing_accuracy"] == 1.0

    # 50% routing decisions with whitespace / case variations
    decisions_mixed = [
        (" Latin ", "latin"),
        ("devanagari", "latin"),
        ("LATIN", "latin"),
        ("latin", "devanagari")
    ]
    res_mixed = compute_routing_accuracy(decisions_mixed)
    assert res_mixed["total_routed"] == 4
    assert res_mixed["correct_routed"] == 2
    assert res_mixed["incorrect_routed"] == 2
    assert res_mixed["routing_accuracy"] == 0.5

    # Empty decisions edge case
    res_empty = compute_routing_accuracy([])
    assert res_empty["total_routed"] == 0
    assert res_empty["routing_accuracy"] == 1.0

    # Confirm isolation: CER on garbage string is 1.0+, while routing accuracy is 1.0 if script matches
    p_text = "xyzabc123"
    gt_text = "different"
    cer = compute_cer(p_text, gt_text)
    assert cer > 0.5  # High CER (bad recognition)
    routing_eval = compute_routing_accuracy([("latin", "latin")])
    assert routing_eval["routing_accuracy"] == 1.0  # Routing is still 100% correct


def test_validate_manifest_blocked_and_populated_states(tmp_path):
    """Verify manifest validator correctly distinguishes PASS_EMPTY_BLOCKED from PASS_VALID_POPULATED."""
    # 1. Existing real packaging manifest is EMPTY / BLOCKED
    real_manifest_path = ROOT_DIR / "data" / "manifests" / "real_packaging_manifest.json"
    valid, details = validate_manifest(real_manifest_path)
    assert valid is True
    assert "PASS_EMPTY_BLOCKED" in details

    # 2. Fabricate a mock populated manifest in a mock project layout
    mock_data_dir = tmp_path / "data" / "manifests"
    mock_data_dir.mkdir(parents=True, exist_ok=True)
    mock_img_dir = tmp_path / "data" / "raw"
    mock_img_dir.mkdir(parents=True, exist_ok=True)
    mock_img = mock_img_dir / "sample.png"
    mock_img.write_bytes(b"dummy_image_data")

    populated_data = {
        "title": "Mock Populated Dataset",
        "status": "ACTIVE_POPULATED",
        "collection_target": 1,
        "records": [
            {
                "image_id": "MOCK-001",
                "sku_id": "SKU-TEST-01",
                "dataset_split": "development",
                "relative_image_path": "data/raw/sample.png"
            }
        ]
    }
    mock_manifest = mock_data_dir / "mock_manifest.json"
    with open(mock_manifest, "w", encoding="utf-8") as f:
        json.dump(populated_data, f)

    valid_pop, details_pop = validate_manifest(mock_manifest)
    assert valid_pop is True
    assert "PASS_VALID_POPULATED" in details_pop



def test_benchmark_artifact_configuration_count():
    """Verify that final_results.json records exactly 8 configurations and 72 inference passes."""
    final_res_path = ROOT_DIR / "benchmarks" / "ocr" / "chunk3" / "final_results.json"
    assert final_res_path.is_file(), f"Benchmark results artifact missing: {final_res_path}"

    with open(final_res_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    exec_summary = data.get("execution_summary", {})
    assert exec_summary.get("total_configurations") == 8
    assert exec_summary.get("evaluated_passes") == 64
    assert exec_summary.get("warmup_passes") == 8
    assert exec_summary.get("total_inference_passes") == 72

    engine_defaults = data.get("engine_defaults", {})
    assert engine_defaults.get("canonical_default_configuration") == "B0_BASELINE_RAW"
    assert engine_defaults.get("provisional_experimental_candidate") == "P_ADAPTIVE_CROP"

    comparisons = data.get("comparisons", {})
    assert len(comparisons) == 7  # 7 comparisons against B0
    assert "P_ADAPTIVE_CROP" in comparisons
    assert comparisons["P_ADAPTIVE_CROP"]["decision"] == "PROVISIONAL_EXPERIMENTAL"
    assert comparisons["P_ADAPTIVE_CROP"]["reconciliation_note"] is not None


def test_engine_default_execution_preserves_polygons():
    """Verify that default OCREngine runs end-to-end and preserves valid coordinates."""
    img_path = ROOT_DIR / "AI_CONTEXT" / "EXPERIMENTS" / "CHUNK_1_OCR_MODEL_SELECTION" / "03_DATASET" / "images" / "SYNTH-01-ENG-FMCG.png"
    if not img_path.is_file():
        pytest.skip(f"Test fixture missing: {img_path}")

    engine = OCREngine()  # Defaults to raw
    assert engine.config.preprocessing_mode == "raw"
    result = engine.extract(str(img_path))

    assert len(result.tokens) > 0
    assert "latin" in result.routing_summary
    for tok in result.tokens:
        assert len(tok.polygon) == 4
        assert len(tok.bbox) == 4
        assert tok.bbox[0] <= tok.bbox[2]
        assert tok.bbox[1] <= tok.bbox[3]
