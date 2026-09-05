/**
 * MetroLens AI™ - Member 5 Chunk M5-2 Automated Verification Suite
 * Tests: Validation utilities, magic byte detection, response normalizer,
 * mock adapter, and live API adapter error handling.
 */

import {
  detectMagicBytes,
  formatFileSize,
  MAX_FILE_SIZE_BYTES,
  validateInspectionImage,
} from "../utils/validation";
import {
  normalizeInspectionResponse,
  synthesizeVerdictSummary,
} from "../services/adapters/responseNormalizer";
import { SYNTHETIC_FIXTURES } from "../mocks/fixtures";
import { MockInspectionAdapter } from "../services/adapters/mockAdapter";
import { LiveApiAdapter } from "../services/adapters/liveApiAdapter";
import { InspectionClientError } from "../services/inspectionClient";

async function runTests() {
  console.log("============================================================");
  console.log("METROLENS AI - MEMBER 5 (CHUNK M5-2) TEST SUITE");
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
  // 1. File Size Formatting Tests
  // ------------------------------------------------------------
  console.log("\n--- 1. File Size Formatting ---");
  assert(formatFileSize(0) === "0 Bytes", "0 bytes formats correctly");
  assert(formatFileSize(1024) === "1 KB", "1024 bytes formats as 1 KB");
  assert(formatFileSize(1024 * 1024 * 2.5) === "2.5 MB", "2.5 MB formats correctly");
  assert(
    formatFileSize(MAX_FILE_SIZE_BYTES) === "15 MB",
    "15 MiB formats as 15 MB boundary"
  );

  // ------------------------------------------------------------
  // 2. Binary Magic Bytes Sniffing Tests
  // ------------------------------------------------------------
  console.log("\n--- 2. Magic Byte Sniffing ---");

  // JPEG Header: FF D8 FF
  const jpegBytes = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10, 0x4a, 0x46, 0x49, 0x46, 0x00, 0x01]);
  const jpegFile = new File([jpegBytes], "package.jpg", { type: "image/jpeg" });
  const detectedJpeg = await detectMagicBytes(jpegFile);
  assert(detectedJpeg === "image/jpeg", "JPEG magic bytes detected (FF D8 FF)");

  // PNG Header: 89 50 4E 47 0D 0A 1A 0A
  const pngBytes = new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d]);
  const pngFile = new File([pngBytes], "label.png", { type: "image/png" });
  const detectedPng = await detectMagicBytes(pngFile);
  assert(detectedPng === "image/png", "PNG magic bytes detected (89 50 4E 47)");

  // WebP Header: RIFF .... WEBP
  const webpBytes = new Uint8Array([
    0x52, 0x49, 0x46, 0x46, // RIFF
    0x24, 0x00, 0x00, 0x00, // size
    0x57, 0x45, 0x42, 0x50, // WEBP
  ]);
  const webpFile = new File([webpBytes], "product.webp", { type: "image/webp" });
  const detectedWebp = await detectMagicBytes(webpFile);
  assert(detectedWebp === "image/webp", "WebP magic bytes detected (RIFF...WEBP)");

  // Corrupt / Non-image bytes
  const corruptBytes = new Uint8Array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b]);
  const corruptFile = new File([corruptBytes], "corrupt.jpg", { type: "image/jpeg" });
  const detectedCorrupt = await detectMagicBytes(corruptFile);
  assert(detectedCorrupt === null, "Corrupt binary header correctly rejected");

  // ------------------------------------------------------------
  // 3. Client Validation Edge Cases
  // ------------------------------------------------------------
  console.log("\n--- 3. Client-Side Validation Rules ---");

  // Empty file (0 bytes)
  const emptyFile = new File([], "empty.png", { type: "image/png" });
  const emptyValidation = await validateInspectionImage(emptyFile);
  assert(!emptyValidation.valid && emptyValidation.error?.type === "FILE_EMPTY", "Empty file rejected with FILE_EMPTY");

  // Oversized file (> 15MB)
  const oversizedBlob = new Blob([new Uint8Array(16 * 1024 * 1024)]);
  const oversizedFile = new File([oversizedBlob], "huge.png", { type: "image/png" });
  const sizeValidation = await validateInspectionImage(oversizedFile);
  assert(
    !sizeValidation.valid && sizeValidation.error?.type === "FILE_TOO_LARGE",
    "File exceeding 15MB rejected with FILE_TOO_LARGE"
  );

  // Prohibited Document Type (PDF)
  const pdfFile = new File([new Uint8Array([0x25, 0x50, 0x44, 0x46])], "invoice.pdf", {
    type: "application/pdf",
  });
  const pdfValidation = await validateInspectionImage(pdfFile);
  assert(
    !pdfValidation.valid && pdfValidation.error?.type === "UNSUPPORTED_TYPE",
    "PDF document rejected with UNSUPPORTED_TYPE"
  );

  // ------------------------------------------------------------
  // 4. Response Normalizer Tests
  // ------------------------------------------------------------
  console.log("\n--- 4. Response Normalizer ---");

  // Test SYNTH-01 (COMPLIANT)
  const synth01Raw = SYNTHETIC_FIXTURES["SYNTH-01-ENG-FMCG"].data;
  const synth01Model = normalizeInspectionResponse(synth01Raw, {
    isSynthetic: true,
    packageTitle: SYNTHETIC_FIXTURES["SYNTH-01-ENG-FMCG"].title,
  });

  assert(synth01Model.verdict.status === "COMPLIANT", "SYNTH-01 mapped to COMPLIANT");
  assert(synth01Model.verdict.isCompliant === true, "SYNTH-01 isCompliant === true");
  assert(synth01Model.verdict.requiresReview === false, "SYNTH-01 requiresReview === false");
  assert(synth01Model.isSynthetic === true, "SYNTH-01 has isSynthetic flag");
  assert(
    synth01Model.syntheticDisclaimer !== undefined,
    "SYNTH-01 includes synthetic disclaimer"
  );
  assert(
    Object.keys(synth01Model.declarations).length >= 5,
    "SYNTH-01 includes 5 mandatory declarations"
  );
  assert(
    synth01Model.calibration.status === "CALIBRATED",
    "SYNTH-01 calibration status preserved"
  );

  // Test SYNTH-04 (NON_COMPLIANT)
  const synth04Raw = SYNTHETIC_FIXTURES["SYNTH-04-MICRO-FONT"].data;
  const synth04Model = normalizeInspectionResponse(synth04Raw, {
    isSynthetic: true,
    packageTitle: SYNTHETIC_FIXTURES["SYNTH-04-MICRO-FONT"].title,
  });

  assert(synth04Model.verdict.status === "NON_COMPLIANT", "SYNTH-04 mapped to NON_COMPLIANT");
  assert(synth04Model.verdict.isCompliant === false, "SYNTH-04 isCompliant === false");
  assert(
    synth04Model.verdict.summaryReason.includes("Rule 7"),
    "SYNTH-04 summary reason cites Rule 7 deficit"
  );

  // Test SYNTH-08 (SUSPECT_REVIEW)
  const synth08Raw = SYNTHETIC_FIXTURES["SYNTH-08-LOW-CONTRAST-FADED"].data;
  const synth08Model = normalizeInspectionResponse(synth08Raw, {
    isSynthetic: true,
    packageTitle: SYNTHETIC_FIXTURES["SYNTH-08-LOW-CONTRAST-FADED"].title,
  });

  assert(synth08Model.verdict.status === "SUSPECT_REVIEW", "SYNTH-08 mapped to SUSPECT_REVIEW");
  assert(synth08Model.verdict.requiresReview === true, "SYNTH-08 requiresReview === true");

  // Test Malformed/Null Server Response
  try {
    normalizeInspectionResponse(null as any);
    assert(false, "Null server response should throw error");
  } catch (err: any) {
    assert(
      err instanceof InspectionClientError && err.code === "INVALID_SERVER_RESPONSE",
      "Null server response throws INVALID_SERVER_RESPONSE"
    );
  }

  // ------------------------------------------------------------
  // 5. Mock Inspection Adapter Tests
  // ------------------------------------------------------------
  console.log("\n--- 5. Mock Inspection Adapter ---");
  const mockAdapter = new MockInspectionAdapter(50); // fast 50ms for tests
  assert(mockAdapter.name === "MockSyntheticInspectionAdapter", "MockAdapter has proper identifier");
  assert(mockAdapter.isMock === true, "MockAdapter isMock flag is true");

  const health = await mockAdapter.getHealth();
  assert(health.status === "OK" && health.isLive === false, "MockAdapter health returns OK/synthetic");

  // Inspect SYNTH-01 simulation
  const validImageFile = new File([pngBytes], "SYNTH-01-ENG-FMCG.png", { type: "image/png" });
  const mockInspection = await mockAdapter.inspect(validImageFile);
  assert(mockInspection.verdict.status === "COMPLIANT", "MockAdapter inspects and resolves COMPLIANT");
  assert(mockInspection.isSynthetic === true, "MockAdapter inspect sets synthetic flag");

  // Inspect SYNTH-04 simulation
  const microFontFile = new File([pngBytes], "SYNTH-04-MICRO-FONT.png", { type: "image/png" });
  const microInspection = await mockAdapter.inspect(microFontFile);
  assert(microInspection.verdict.status === "NON_COMPLIANT", "MockAdapter routes MICRO to NON_COMPLIANT");

  // ------------------------------------------------------------
  // 6. Live API Adapter Error Handling Tests
  // ------------------------------------------------------------
  console.log("\n--- 6. Live API Adapter (Network Failure Handling) ---");
  const liveAdapter = new LiveApiAdapter("http://localhost:59999"); // intentionally dead port
  assert(liveAdapter.name === "LiveFastApiInspectionAdapter", "LiveApiAdapter has proper identifier");
  assert(liveAdapter.isMock === false, "LiveApiAdapter isMock flag is false");

  const liveHealth = await liveAdapter.getHealth();
  assert(
    liveHealth.status === "UNAVAILABLE" && liveHealth.isLive === false,
    "Live health reports UNAVAILABLE when backend is unreachable"
  );

  try {
    await liveAdapter.inspect(validImageFile);
    assert(false, "Live inspect should throw NETWORK_ERROR on dead endpoint");
  } catch (err: any) {
    assert(
      err instanceof InspectionClientError && err.code === "NETWORK_ERROR",
      "Live inspect catches connection failure and raises structured NETWORK_ERROR"
    );
  }

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

runTests().catch((err) => {
  console.error("Test execution failed:", err);
  process.exit(1);
});
