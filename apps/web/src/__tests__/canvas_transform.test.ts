/**
 * MetroLens AI™ - Evidence Canvas Transform & Geometry Test Suite
 * Tests pure coordinate math, forward/inverse mappings, round-trip identities,
 * fit-to-screen aspect preservation, and ray-casting hit-testing.
 */

import {
  imageToCanvas,
  canvasToImage,
  fitToScreen,
  zoomAt,
  pointInPolygon,
  pointInBBox,
  sanitizePolygon,
  CanvasTransform,
  Point,
} from "../features/inspection/canvasTransform";

function runTests() {
  console.log("============================================================");
  console.log("METROLENS AI - CANVAS TRANSFORM & GEOMETRY TEST SUITE");
  console.log("============================================================");

  let passed = 0;
  let failed = 0;

  function assert(condition: boolean, testName: string) {
    if (condition) {
      console.log(`[PASS] ${testName}`);
      passed++;
    } else {
      console.error(`[FAIL] ${testName}`);
      failed++;
    }
  }

  // ------------------------------------------------------------
  // 1. Forward Transform (imageToCanvas)
  // ------------------------------------------------------------
  console.log("\n--- 1. Forward Transform Tests ---");
  const p1: Point = { x: 100, y: 50 };
  const identityT: CanvasTransform = { scale: 1.0, panX: 0, panY: 0 };
  const c1 = imageToCanvas(p1, identityT);
  assert(c1.x === 100 && c1.y === 50, "Identity transform maps (100, 50) -> (100, 50)");

  const scale2T: CanvasTransform = { scale: 2.0, panX: 10, panY: 20 };
  const c2 = imageToCanvas(p1, scale2T);
  assert(c2.x === 210 && c2.y === 120, "Scale 2.0 with pan (10, 20) maps (100, 50) -> (210, 120)");

  // ------------------------------------------------------------
  // 2. Inverse Transform (canvasToImage)
  // ------------------------------------------------------------
  console.log("\n--- 2. Inverse Transform Tests ---");
  const i2 = canvasToImage(c2, scale2T);
  assert(
    Math.abs(i2.x - 100) < 1e-6 && Math.abs(i2.y - 50) < 1e-6,
    "Inverse transform maps (210, 120) back to (100, 50)"
  );

  // ------------------------------------------------------------
  // 3. Mandatory Round-Trip Invariant: canvasToImage(imageToCanvas(P)) == P
  // ------------------------------------------------------------
  console.log("\n--- 3. Mandatory Round-Trip Invariant Tests ---");
  const testPoints: Point[] = [
    { x: 0, y: 0 },
    { x: 640, y: 360 },
    { x: 28.96, y: 72.57 },
    { x: 346.18, y: 111.66 },
    { x: 125.4, y: 280.9 },
  ];

  const testTransforms: CanvasTransform[] = [
    { scale: 0.5, panX: 50, panY: 30 },
    { scale: 1.25, panX: -40, panY: 85 },
    { scale: 3.1415, panX: 120, panY: -60 },
    { scale: 0.088, panX: 0, panY: 0 },
  ];

  let allRoundTripsPassed = true;
  for (const pt of testPoints) {
    for (const tr of testTransforms) {
      const canvasPt = imageToCanvas(pt, tr);
      const restoredPt = canvasToImage(canvasPt, tr);
      const errX = Math.abs(restoredPt.x - pt.x);
      const errY = Math.abs(restoredPt.y - pt.y);
      if (errX > 1e-5 || errY > 1e-5) {
        allRoundTripsPassed = false;
        console.error(`Roundtrip failed for pt (${pt.x}, ${pt.y}) under transform`, tr);
      }
    }
  }
  assert(allRoundTripsPassed, "Round-trip identity holds for all points across all transforms (|err| < 1e-5)");

  // ------------------------------------------------------------
  // 4. Fit to Screen Aspect Preservation
  // ------------------------------------------------------------
  console.log("\n--- 4. Fit-To-Screen Tests ---");
  // Container: 800x600, Image: 640x360, padding: 0
  const fit1 = fitToScreen(640, 360, 800, 600, 0);
  assert(fit1.scale === 1.25, "Fit scale for 640x360 into 800x600 is 1.25");
  assert(fit1.panX === 0, "Horizontal pan is 0 (width fills container)");
  assert(fit1.panY === 75, "Vertical pan is 75 (centers 450px in 600px height)");

  // Container: 400x800, Image: 640x360, padding: 20 (avail: 360x760)
  const fit2 = fitToScreen(640, 360, 400, 800, 20);
  const expectedScale = 360 / 640; // 0.5625
  assert(Math.abs(fit2.scale - expectedScale) < 1e-6, "Fit scale correctly bounds by available width");
  assert(Math.abs(fit2.panX - 20) < 1e-6, "Horizontal pan equals padding");
  assert(fit2.panY > 20, "Vertical pan centers image vertically in tall container");

  // ------------------------------------------------------------
  // 5. Cursor-Anchored Zoom
  // ------------------------------------------------------------
  console.log("\n--- 5. Cursor-Anchored Zoom Tests ---");
  const cursorPoint: Point = { x: 300, y: 200 };
  const initialT: CanvasTransform = { scale: 1.0, panX: 50, panY: 50 };
  const zoomedT = zoomAt(cursorPoint, initialT, 1.5);

  // The image point under the cursor before zoom must remain under the cursor after zoom
  const imgPtBefore = canvasToImage(cursorPoint, initialT);
  const imgPtAfter = canvasToImage(cursorPoint, zoomedT);
  assert(
    Math.abs(imgPtBefore.x - imgPtAfter.x) < 1e-5 &&
    Math.abs(imgPtBefore.y - imgPtAfter.y) < 1e-5,
    "Cursor-anchored zoom keeps the focal image point stationary under cursor"
  );
  assert(zoomedT.scale === 1.5, "Scale zoomed by 1.5x");

  // ------------------------------------------------------------
  // 6. Point-in-Polygon Ray Casting Hit-Testing
  // ------------------------------------------------------------
  console.log("\n--- 6. Polygon Hit-Testing Tests ---");
  // Convex quadrilateral (rectangle): [20, 20] to [120, 80]
  const rectPoly: [number, number][] = [
    [20, 20],
    [120, 20],
    [120, 80],
    [20, 80],
  ];

  assert(pointInPolygon({ x: 50, y: 50 }, rectPoly) === true, "Point (50, 50) is inside rectangle");
  assert(pointInPolygon({ x: 10, y: 10 }, rectPoly) === false, "Point (10, 10) is outside rectangle");
  assert(pointInPolygon({ x: 150, y: 50 }, rectPoly) === false, "Point (150, 50) is outside rectangle");

  // Rotated quadrilateral (diamond): Top (50, 0), Right (100, 50), Bottom (50, 100), Left (0, 50)
  const diamondPoly: [number, number][] = [
    [50, 0],
    [100, 50],
    [50, 100],
    [0, 50],
  ];
  assert(pointInPolygon({ x: 50, y: 50 }, diamondPoly) === true, "Center of diamond is inside");
  assert(pointInPolygon({ x: 10, y: 10 }, diamondPoly) === false, "Top-left corner outside diamond");

  // ------------------------------------------------------------
  // 7. Defensive Sanitization & Malformed Inputs
  // ------------------------------------------------------------
  console.log("\n--- 7. Malformed Geometry Sanitization ---");
  const malformed1 = sanitizePolygon(null, { xMin: 10, yMin: 20, xMax: 110, yMax: 70 });
  assert(malformed1.length === 4, "Null polygon safely falls back to bounding box");
  assert(malformed1[0][0] === 10 && malformed1[2][0] === 110, "Fallback bounding box coordinates correct");

  const malformed2 = sanitizePolygon([[NaN, 0], [10, 10]], null);
  assert(malformed2.length === 4, "Invalid array with NaN falls back to safe unit quad without throwing");

  // ------------------------------------------------------------
  // Summary
  // ------------------------------------------------------------
  console.log("\n============================================================");
  console.log(`TEST SUMMARY: ${passed} PASSED, ${failed} FAILED`);
  console.log("============================================================");

  if (failed > 0) {
    process.exit(1);
  }
}

runTests();
