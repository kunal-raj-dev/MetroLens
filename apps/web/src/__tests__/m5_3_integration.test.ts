import { SYNTHETIC_FIXTURES, getFixtureById } from "../mocks/fixtures";
import { normalizeInspectionResponse } from "../services/adapters/responseNormalizer";
import {
  CanvasTransform,
  imageToCanvas,
  canvasToImage,
  fitToScreen,
  pointInPolygon,
  zoomAt,
} from "../features/inspection/canvasTransform";

function assert(condition: boolean, msg: string) {
  if (!condition) {
    console.error(`[FAIL] ${msg}`);
    process.exit(1);
  } else {
    console.log(`[PASS] ${msg}`);
  }
}

console.log("============================================================");
console.log("METROLENS AI - MEMBER 5 (CHUNK M5-3) INTEGRATION TEST SUITE");
console.log("============================================================\n");

// 1. Fixture Verification & Frozen OCR Coordinates
console.log("--- 1. Member 1 Frozen OCR Coordinate Verification ---");
const fixtureDef01 = getFixtureById("SYNTH-01");
assert(!!fixtureDef01, "SYNTH-01 fixture found");
const fixture01 = fixtureDef01!.data;
assert(
  Array.isArray(fixture01.ocr_observations) && fixture01.ocr_observations.length === 6,
  "SYNTH-01 contains exactly 6 real Member 1 OCR tokens"
);

for (const obs of fixture01.ocr_observations!) {
  assert(Boolean(obs.polygon && obs.polygon.length === 4), `Token ${obs.token_id} has 4-point polygon quad`);
  if (!obs.polygon) continue;
  for (const pt of obs.polygon) {
    assert(typeof pt[0] === "number" && typeof pt[1] === "number", `Token ${obs.token_id} points are numbers`);
    // Coordinate space verification: original pixel space [0, 640] x [0, 360]
    assert(
      pt[0] >= 0 && pt[0] <= 640 && pt[1] >= 0 && pt[1] <= 360,
      `Token ${obs.token_id} coordinate (${pt[0]}, ${pt[1]}) is within original image pixel bounds (640x360)`
    );
    // Explicit verification: Coordinates MUST NOT be normalized percentages [0, 1]
    const isNormalizedPercentage = pt[0] <= 1.0 && pt[1] <= 1.0;
    assert(
      !isNormalizedPercentage,
      `Token ${obs.token_id} coordinate is in real pixel space (not normalized [0, 1] percentage)`
    );
  }
}

// 2. Multilingual & Devanagari Hindi Token Verification
console.log("\n--- 2. Multilingual & Devanagari Hindi Token Verification ---");
const fixtureDef02 = getFixtureById("SYNTH-02");
assert(!!fixtureDef02, "SYNTH-02 fixture found");
const fixture02 = fixtureDef02!.data;
const hindiMrp = fixture02.ocr_observations?.find((t) => t.token_id === "hin_004");
assert(!!hindiMrp, "SYNTH-02 contains Devanagari MRP token (hin_004)");
assert(
  Boolean(hindiMrp?.text.includes("₹") && hindiMrp?.text.includes("अधिकतम")),
  `Devanagari MRP preserves Indian Rupee '₹' and Hindi text: "${hindiMrp?.text}"`
);
assert(
  hindiMrp?.language === "hi",
  "DTO 'hi' language metadata correctly preserved"
);
const normHindi = normalizeInspectionResponse(fixture02);
const normMrpTok = normHindi.ocrTokens.find((t) => t.id === "hin_004");
assert(
  normMrpTok?.script?.toLowerCase() === "devanagari" && normMrpTok?.language === "hi",
  "Devanagari script and 'hi' language correctly resolved in Frontend model"
);

// 3. Response Normalizer OCR Token Extraction
console.log("\n--- 3. Response Normalizer OCR Token Normalization ---");
const normalized01 = normalizeInspectionResponse(fixture01);
assert(
  normalized01.ocrTokens.length === 6,
  `Response normalizer produced ${normalized01.ocrTokens.length} OCRTokenModel objects`
);
const tok1 = normalized01.ocrTokens[0];
assert(tok1.id === "tok_006", "Token ID preserved");
assert(
  typeof tok1.boundingBox.width === "number" && tok1.boundingBox.width > 0,
  "Bounding box width calculated"
);
const netQtyTok = normalized01.ocrTokens.find((t) => t.fieldName === "net_quantity");
assert(
  !!netQtyTok && netQtyTok.id === "tok_004",
  "Declaration field mapping preserved for tok_004 (net_quantity)"
);

// 4. Transform Accuracy & Multi-Scale DPI Invariant
console.log("\n--- 4. Transform Accuracy & High-DPI Invariant ---");
const transform1x: CanvasTransform = { scale: 1.0, panX: 0, panY: 0 };
const transform2x: CanvasTransform = { scale: 2.0, panX: 50, panY: 100 };

// Image token point in original image space
const imgPt = { x: tok1.polygon[0][0], y: tok1.polygon[0][1] };
const canvasPt1x = imageToCanvas(imgPt, transform1x);
const canvasPt2x = imageToCanvas(imgPt, transform2x);

assert(
  canvasPt1x.x === imgPt.x && canvasPt1x.y === imgPt.y,
  "Identity transform leaves original pixel coordinates intact"
);
assert(
  canvasPt2x.x === imgPt.x * 2.0 + 50 && canvasPt2x.y === imgPt.y * 2.0 + 100,
  "Scale 2x with pan applies affine transform correctly"
);

// Inverting back must reproduce original coordinates exactly
const invertedPt = canvasToImage(canvasPt2x, transform2x);
assert(
  Math.abs(invertedPt.x - imgPt.x) < 1e-6 && Math.abs(invertedPt.y - imgPt.y) < 1e-6,
  "Inverse transform round-trip error < 1e-6"
);

// 5. Ray-Casting Polygon Hit-Testing
console.log("\n--- 5. Ray-Casting Polygon Hit-Testing ---");
// tok_006 polygon: [[30.0, 25.57], [364.0, 25.57], [364.0, 42.95], [30.0, 42.95]]
// Test a point inside tok_006
const insidePoint = { x: 100, y: 35 };
assert(
  pointInPolygon(insidePoint, tok1.polygon),
  "Point (100, 35) correctly identified INSIDE tok_006 quad"
);

// Test a point outside tok_006
const outsidePoint = { x: 500, y: 35 };
assert(
  !pointInPolygon(outsidePoint, tok1.polygon),
  "Point (500, 35) correctly identified OUTSIDE tok_006 quad"
);

// 6. Client Non-Adjudication Check
console.log("\n--- 6. Client Non-Adjudication Integrity ---");
// Verify that the frontend model does not fabricate legal verdicts or font heights
const synthDef04 = getFixtureById("SYNTH-04");
const norm04 = normalizeInspectionResponse(synthDef04!.data);
assert(
  norm04.verdict.status === "NON_COMPLIANT",
  "Verdict comes directly from backend payload without client recalculation"
);
assert(
  norm04.isSynthetic === true,
  "Synthetic flag explicitly set on synthetic fixture"
);
assert(
  norm04.syntheticDisclaimer !== undefined && norm04.syntheticDisclaimer.length > 10,
  "Prominent synthetic disclaimer present"
);

console.log("\n============================================================");
console.log("M5-3 INTEGRATION SUITE: ALL CHECKS PASSED PERFECTLY");
console.log("============================================================\n");
