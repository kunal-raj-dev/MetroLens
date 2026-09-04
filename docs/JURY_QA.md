# COMPREHENSIVE JURY Q&A DEFENSE STRATEGY (32 ADVERSARIAL QUESTIONS) — V0.3
## MetroLens AI — Automated Legal Metrology Inspection System (SIH26034)
**Evaluation Context:** InnoHack 3.0 / Smart India Hackathon 2026 | **Defense Framework:** Categorized by FACT, ENGINEERING DECISION, LIMITATION, and FUTURE WORK.  
**Governing Standard:** Zero Invented Numbers. Defendable Science and Transparent Boundary Realism.

---

### Category A: Optical Physics & Geometric Measurement

#### Q1: "How can you claim to measure a 1.5mm font when packaging is captured at an angle and perspective foreshortens the image?"
- **Answer:**
  - **FACT:** When a camera views a planar surface at an inclination angle $\theta$, physical dimensions along the tilt axis foreshorten by $\cos\theta$. At $30^\circ$ tilt, dimensions compress by $13.4\%$.
  - **ENGINEERING DECISION:** We resolve the monocular scale ambiguity by introducing a universally accessible metric scale anchor—a standard Indian 10-Rupee coin (official RBI outer diameter: $27.0\text{mm}$) or a standard ISO ID card ($85.60 \times 53.98\text{mm}$). Under our constrained capture protocol ($\le 10^\circ$ tilt guided by real-time viewfinder alignment reticles), the scale factor $S = \text{diameter} / d_{\text{pixels}}$ recovers physical millimeters. For tilted planes, 4-corner rectangular correspondences unwarp perspective into an orthorectified metric plane prior to measuring stroke heights.
  - **LIMITATION:** An unconstrained circular contour alone leaves surface normal azimuth ambiguous under extreme tilt ($>35^\circ$). We enforce coplanarity guidelines and flag severe tilt for manual review.
  - **FUTURE WORK:** Hardware-assisted AR depth mesh unwarping using mobile ToF sensors.
- **Evidence:** Live UI screen displaying scale factor recovery and rectified text crops.

#### Q2: "What if the packaging is curved, like a soda can, shampoo bottle, or glass jar?"
- **Answer:**
  - **FACT:** A right circular cylinder $\mathbf{P}(\phi, y) = (R\cos\phi, y, R\sin\phi)$ has curvature strictly along its circumferential axis. Along the vertical generator line parallel to the cylinder axis, the surface coordinate maps linearly to the sensor: $y_{\text{proj}} = y_{\text{actual}}$.
  - **ENGINEERING DECISION:** Under Rule 7, statutory font height is strictly measured along the **vertical axis** (numeral capital height / ascender-descender). Therefore, on upright right circular cylinders, horizontal curvature does not foreshorten vertical numeral stroke height. We restrict automated measurement to the **central $40^\circ$ generator strip** ($\cos\phi \ge 0.94$).
  - **LIMITATION:** This mathematical invariance holds strictly for true right cylinders held vertically perpendicular to the camera. Tapered bottles, conical necks, spherical jars, and crumpled pouches violate this assumption.
  - **ENGINEERING DECISION:** The system detects non-cylindrical or irregular packaging and automatically flags: `MANUAL_REVIEW_REQUIRED — Non-Planar Curvature Detected`.
- **Evidence:** Central generator crop visualization on a physical beverage can.

#### Q3: "What is your measurement uncertainty, and how do you prevent false-positive violation notices on borderline fonts?"
- **Answer:**
  - **FACT:** Handheld calipers and optical binarization both exhibit edge-detection variance ($\pm 0.05\text{–}0.10\text{mm}$).
  - **ENGINEERING DECISION:** We do not issue unilateral violation notices on borderline measurements. The rule engine implements a **Statutory Benefit-of-Doubt Buffer of $0.10\text{mm}$**:
    - If statutory minimum is $1.50\text{mm}$, an actionable potential non-compliance is flagged only if measured height falls strictly below $1.40\text{mm}$.
    - Measurements between $1.40\text{mm}$ and $1.50\text{mm}$ are classified as `MANUAL_REVIEW_REQUIRED`, presenting a side-by-side zoomed crop for officer confirmation.
  - **LIMITATION:** Optical measurement precision is bounded by sensor pixel density and focus blur.
- **Evidence:** UI amber `MANUAL_REVIEW_REQUIRED` card demonstrating the $0.10\text{mm}$ benefit-of-doubt buffer.

#### Q4: "How do you calculate the Principal Display Panel (PDP) area to know which font threshold from Table 1 applies?"
- **Answer:**
  - **FACT:** Under Rule 7, PDP area for a rectangular container is height $\times$ width of the largest face. Under Rule 7 Table-I/II, area $A$ determines statutory font minimums ($1.0\text{mm}$ for $A \le 50\text{ cm}^2$, $1.5\text{mm}$ for $50 < A \le 100\text{ cm}^2$, $2.5\text{mm}$ for $100 < A \le 500\text{ cm}^2$).
  - **ENGINEERING DECISION:** When the inspector captures the package panel with the metric anchor, our boundary detector segments the outer container edges. Using the calibrated millimeter-per-pixel scale, the system calculates surface area $A$ in $\text{cm}^2$, which directly indexes Table 1.
  - **LIMITATION:** In monocular vision, calculating 3D surface area on non-planar packages requires manual panel dimension entry or flat carton unfolding.
- **Evidence:** On-screen calculation card displaying calculated PDP area indexing Rule 7 Table-I/II.

#### Q5: "What if the 10-Rupee coin is worn out, dirty, or tilted relative to the package?"
- **Answer:**
  - **FACT:** Circulated coins experience edge wear, and user placement may not be perfectly coplanar.
  - **ENGINEERING DECISION:** The viewfinder draws an alignment guide instructing the officer to place the coin flat against the packaging panel. The ellipse-fitting module checks the axis eccentricity ratio; if eccentricity indicates out-of-plane tilt $>15^\circ$, the system alerts the user to re-align.
  - **FALLBACK:** If the coin is unavailable or dirty, the inspector taps **"Manual Scale Override"** in the UI, selecting an alternative known reference (e.g. an ATM card) or clicking two points of known physical distance.
- **Evidence:** Viewfinder eccentricity rejection warning and UI manual scale override button.

---

### Category B: Legal Metrology Statutes & Jan Vishwas Act Enforcement

#### Q6: "Does your software automatically issue fines or compounding notices to shopkeepers?"
- **Answer:**
  - **FACT:** Under the **Jan Vishwas (Amendment of Provisions) Act, 2023**, Section 36(1) of the Legal Metrology Act, 2009 was fundamentally amended to decriminalize first-time packaging non-compliances. The law mandates an **Improvement Notice** for the first offence, granting 15–30 days to rectify with zero financial penalty. Repeated offences must be adjudicated by a statutory **Adjudicating Officer** appointed under Section 48A.
  - **ENGINEERING DECISION:** MetroLens AI **NEVER** issues automated fines or judicial summons. It functions strictly as an **Evidentiary Compliance Assessment System under Section 15**, generating a tamper-evident report recommending an Improvement Notice under Section 36(1) or physical sample seizure.
  - **LIMITATION:** Software is an assistive tool; legal authority rests exclusively with the human officer.
- **Evidence:** Generated Assessment Report citing Section 36(1) Improvement Notice statutory wording.

#### Q7: "Why was the generated report renamed from 'Image-Based Compliance Assessment Report' in v0.3?"
- **Answer:**
  - **FACT:** Under the Legal Metrology (Packaged Commodities) Rules, 2011, "Image-Based Compliance Assessment Report" is an application format for registration of manufacturers/packers under Rule 27; it is not a statutory inspection or violation notice. Seizure notices are issued under Form 1 / Section 15.
  - **ENGINEERING DECISION:** We eliminated "Image-Based Compliance Assessment Report" across all documents, code, and UI to ensure absolute legal integrity. The output is officially titled: **"MetroLens AI — Image-Based Compliance Assessment Report"** with subtitle: *Automated Regulatory Inspection & Evidentiary Screening Report*.
- **Evidence:** Renamed PDF report title and clean legal citation block.

#### Q8: "How does the system verify the Unit Sale Price (USP) mandate introduced in recent amendments?"
- **Answer:**
  - **FACT:** Under Rule 6(11) (enacted via GSR 779(E) and enforced October 1, 2022), pre-packaged commodities containing $>1$ unit or $>1\text{kg/L}$ must declare Unit Sale Price in standardized denominations: per g or per 100g ($<1\text{kg}$), per kg ($\ge 1\text{kg}$), per ml/100ml ($<1\text{L}$), per L ($\ge 1\text{L}$), or per item/number.
  - **ENGINEERING DECISION:** Our rule engine extracts Net Quantity and MRP, determines the mandatory statutory denomination, computes expected USP via deterministic arithmetic ($\text{Expected USP} = \text{MRP} / \text{Quantity}$), and validates that the declared USP matches the calculation within standard rounding limits ($\pm 1\%$).
  - **LIMITATION:** If declared USP text is completely obscured or worn off, OCR cannot extract it; the system flags `POTENTIAL_NON_COMPLIANCE — Omission of Mandatory USP Declaration`.
- **Evidence:** Automated unit tests in `tests/test_rule_6_11_usp.py` covering 25 arithmetic edge cases.

#### Q9: "How do you handle statutory exemptions, such as packages containing 10 grams or less?"
- **Answer:**
  - **FACT:** Rule 26(a) exempts packages with net quantity $\le 10\text{g}$ or $\le 10\text{ml}$ from mandatory declarations. However, **tobacco and tobacco products are explicitly excluded from this exemption**. Furthermore, under **GSR 881(E) (effective February 1, 2026)**, packaging exemptions for pan masala and gutkha pouches were formally revoked!
  - **ENGINEERING DECISION:** The rule engine does not apply a blanket exemption based solely on net weight. It first checks the product commodity category: if the commodity is tobacco or pan masala, miniature exemptions are bypassed and full declarations are enforced. Only non-tobacco commodities $\le 10\text{g}$ trigger `STATUTORY_EXEMPTION_APPLIED`.
- **Evidence:** Unit test verifying miniature pan masala non-exemption under GSR 881(E).

#### Q10: "Can an electronic product declare manufacturer details via QR code instead of physical print?"
- **Answer:**
  - **FACT:** Under Department of Consumer Affairs circulars (2022/2023), electronic commodities are permitted to declare detailed manufacturer addresses and technical specifications via an on-pack QR code, provided MRP, Net Quantity, Mfg Date, and Country of Origin remain physically printed on the carton.
  - **ENGINEERING DECISION:** For verified electronic products, our engine detects QR codes and checks payload accessibility. Missing physical address text on the outer carton is not flagged as a violation if a valid QR code is detected. This exemption is strictly quarantined from food and cosmetic categories.
- **Evidence:** Category-aware exemption switch in `modules/rules/rule_engine.py`.

---

### Category C: AI Perception vs. Deterministic Logic

#### Q11: "Why shouldn't we just pass the photo to Gemini or GPT-4V and ask it if the label is legal?"
- **Answer:**
  - **FACT:** Large Language Models are probabilistic next-token predictors. In regulatory compliance, LLMs suffer from:
    1. *Spatial Blindness:* Zero metric perception; an LLM cannot compute whether a character is $1.15\text{mm}$ or $1.50\text{mm}$.
    2. *Statutory Hallucination:* LLMs probabilistically invent non-existent legal clauses or misapply category exemptions.
    3. *Arithmetic Flaws:* LLMs fail at reliable decimal divisions required for Unit Sale Price.
  - **ENGINEERING DECISION:** We enforce a strict **4-Pillar Separation of Concerns**:
    - **AI Perceives:** Local PaddleOCR extracts text strings and bounding boxes.
    - **Math Validates:** OpenCV homography computes metric scale; IEEE 754 float division audits USP.
    - **Rules Decide:** Deterministic Python state machines enforce Gazette clauses.
    - **Humans Govern:** Low-confidence edge cases are routed to human officers.
- **Evidence:** Zero LLM calls in the compliance decision path (`modules/rules/`).

#### Q12: "Where IS artificial intelligence actually used in your system?"
- **Answer:**
  - **ENGINEERING DECISION:** AI is used strictly where machine learning is statistically superior to deterministic heuristics:
    1. *Scene Text Detection & Recognition:* PaddleOCR DBNet++ and SVTR models handle artistic fonts, colored backgrounds, and varied lighting.
    2. *Multilingual Text Processing:* Pre-trained Devanagari models recognize Hindi packaging text.
    3. *Optional Entity Normalization:* Lightweight SLM assists regex normalizers in mapping messy OCR strings to canonical schema fields.
- **Evidence:** ONNX runtime pipeline in `modules/ocr/`.

#### Q13: "What happens if OCR misreads a character due to glare or packaging crinkles?"
- **Answer:**
  - **ENGINEERING DECISION:** We implement a two-stage defense:
    1. *Viewfinder Glare Pre-Check:* Evaluates saturation in HSV space ($V > 250, S < 30$). If specular glare obscures $>5\%$ of text ROI, it alerts the user to tilt slightly.
    2. *Graceful Confidence Degradation:* If OCR character confidence drops below $80\%$, the system does NOT flag a false violation. Instead, it marks that specific declaration as `MANUAL_REVIEW_REQUIRED` and displays a cropped snippet for 1-tap officer confirmation.
- **Evidence:** Live demonstration of the 1-tap officer review UI.

#### Q14: "How do you handle multilingual packaging printed in Hindi (Devanagari) or regional scripts?"
- **Answer:**
  - **FACT:** Rule 8 permits declarations in Hindi or English. Interstate commercial goods mandate English declarations under Rule 8(2).
  - **ENGINEERING DECISION:** PaddleOCR v4 includes native Devanagari weights. Our normalizer maps recognized Hindi terms (e.g. `अधिकतम खुदरा मूल्य` $\rightarrow$ `mrp`, `शुद्ध मात्रा` $\rightarrow$ `net_quantity`) into our canonical legal schema. If Hindi text confidence is low, the engine checks for co-located English declarations.
- **Evidence:** Hindi dictionary mapping module in `modules/ocr/hindi_dictionary_mapping.py`.

---

### Category D: Government Systems & Industry Differentiation

#### Q15: "What existing government system does this replace, and why hasn't the Ministry already built this?"
- **Answer:**
  - **FACT:** It replaces zero systems; it provides the **missing automated field perception layer for eMaap**.
  - **ENGINEERING DECISION:** eMaap is the National Legal Metrology portal for administrative workflows: dealer licensing, verification scheduling, and compounding fee management. It contains zero computer vision and zero automated mobile compliance checking. Field officers currently conduct inspections with plastic rulers and manually type findings into eMaap. MetroLens AI acts as a field perception microservice that exports standardized JSON compliance records ready for eMaap ingestion.
  - **LIMITATION:** eMaap does not currently publish a public third-party REST API; our system provides an eMaap-ready mock adapter interface.
- **Evidence:** Mock eMaap adapter tab in the inspection dashboard.

#### Q16: "How is this different from consumer food barcode scanning apps like Yuka or HealthifyMe?"
- **Answer:**
  - **FACT:** Barcode apps scan 1D EAN/UPC barcodes to look up crowdsourced nutritional databases. They do not inspect the physical printed packaging at all!
  - **ENGINEERING DECISION:** Barcode apps cannot detect physical shrinkflation (reducing weight from 100g to 82g), cannot measure font millimeter heights under Rule 7, cannot verify Unit Sale Price math, and cannot enforce Legal Metrology statutes. MetroLens AI performs direct computer vision inspection of the physical printed packaging surface.
- **Evidence:** System architecture inspecting raw pixels without querying barcode databases.

#### Q17: "How is this different from industrial print inspection systems like GlobalVision or EyeC?"
- **Answer:**
  - **FACT:** GlobalVision and EyeC are enterprise prepress quality-control systems costing $10,000 to $50,000 per seat. They require flatbed optical scanners in printing factories comparing vector PDF artwork against scanned press sheets.
  - **ENGINEERING DECISION:** Industrial inspection systems cannot be used by a government inspector standing in a retail grocery aisle examining a 3D physical crumpled pouch on a mobile phone. MetroLens AI is an edge-native, perspective-corrected mobile inspection system built specifically for field enforcement.
- **Evidence:** Mobile responsive viewfinder running on localhost.

---

### Category E: Evidentiary Admissibility & Legal Chain of Custody

#### Q18: "What legal validity does an AI report have in an Indian court of law?"
- **Answer:**
  - **FACT:** Under Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 (formerly Section 65B of the Indian Evidence Act), electronic records require proof of authenticity, integrity, and custody certified by an authorized officer. Software cannot certify its own legal admissibility by fiat.
  - **ENGINEERING DECISION:** The system functions as a **Prima Facie Evidentiary Screening Tool under Section 15**. To establish tamper-evidence, the generated Assessment Report embeds:
    1. Cryptographic SHA-256 hash of the raw uncompressed photo.
    2. Calibrated bounding box coordinates and millimeter measurements.
    3. ISO-8601 UTC timestamp and GPS coordinates.
    4. Model version commit hash and inspection session UUID.
  - **STATUTORY REALITY:** This tamper-evident package provides lawful factual justification for an inspecting officer to sign an official certificate, issue an Improvement Notice, or seize physical samples.
- **Evidence:** Cryptographic hash integrity block on the generated PDF report.

#### Q19: "What if the manufacturer claims the software fabricated the violation?"
- **Answer:**
  - **ENGINEERING DECISION:** The system provides complete mathematical and visual explainability. The report does not output an opaque score; it displays the high-resolution crop of the offending text, plots the measured stroke height alongside the coin calibration trace, cites the exact Gazette clause, and provides the formula used. The manufacturer can verify the measurement with their own caliper on the retained physical sample.
- **Evidence:** Side-by-side evidence crop in generated PDF report.

#### Q20: "What if a shopkeeper has pasted a price sticker over the manufacturer MRP?"
- **Answer:**
  - **FACT:** Under Section 36(2) of the Act, altering, defacing, or affixing an additional sticker over the manufacturer's declared MRP is a specific statutory offence.
  - **ENGINEERING DECISION:** Our vision pipeline includes a rectangular contour anomaly detector that identifies adhesive sticker boundaries overlapping declaration text, alerting the inspector to potential retail price tampering.
- **Evidence:** Contour anomaly detector highlighting overlapping label patches.

---

### Category F: Operational Feasibility & Hackathon Execution

#### Q21: "Can this system run 100% offline in rural retail shops with zero internet connectivity?"
- **Answer:**
  - **FACT:** Rural retail mandis and remote grocery stores frequently have zero cellular reception.
  - **ENGINEERING DECISION:** The entire core pipeline—quantized PaddleOCR ONNX, OpenCV calibration, deterministic Python rule engine, SQLite database, and ReportLab PDF generator—runs locally on the host device. The entire live demonstration today is executing with Wi-Fi and Cellular toggled completely OFF.
- **Evidence:** Live demonstration executed with network interfaces disabled.

#### Q22: "What is your end-to-end processing latency on standard consumer hardware?"
- **Answer:**
  - **FACT:** Cloud API roundtrips take $3\text{–}5\text{ seconds}$ and fail without internet.
  - **ENGINEERING TARGET:** Total pipeline latency budget on a standard quad-core laptop CPU is $< 2.5\text{ seconds}$:
    - Preprocessing & Glare Check: $< 100\text{ms}$
    - Local PaddleOCR ONNX Inference: $< 1,200\text{ms}$
    - Entity Normalization: $< 300\text{ms}$
    - Deterministic Rule Engine Execution: $< 20\text{ms}$
    - Assessment Report Compilation: $< 400\text{ms}$
- **Evidence:** Real-time latency timer displayed on web dashboard.

#### Q23: "Why is e-commerce scraping not in your live demonstration?"
- **Answer:**
  - **FACT:** Headless scraping of Amazon/Blinkit listings in a live pitch carries severe failure risks due to Cloudflare bot-detection, CAPTCHAs, and dynamic DOM shifts.
  - **ENGINEERING DECISION:** Our 6-member team prioritized core optical physics, local OCR, and Jan Vishwas Act compliance. E-commerce scraping was formally deferred to post-hackathon to guarantee 100% stability and zero live demo glitches.
- **Evidence:** Explicit scope classification in `docs/PRODUCT_BLUEPRINT.md`.

#### Q24: "Can FMCG manufacturers use this software before printing packaging to prevent recalls?"
- **Answer:**
  - **ENGINEERING DECISION:** Yes! That is our primary B2B value proposition: **Brand Pre-Flight Mode**. A packaging designer uploads digital vector artwork (PDF/PNG) prior to mass printing. Because digital artwork has known DPI resolution, the system calculates exact physical millimeter font sizes and verifies 100% Legal Metrology compliance, preventing multi-crore cylinder re-engraving and packaging recall losses.
- **Evidence:** Pre-Flight Mode toggle on dashboard.

#### Q25: "What is your false-positive rate and how do you ensure honest brands aren't penalized?"
- **Answer:**
  - **FACT:** In regulatory law, false positives damage merchant trust and generate litigation.
  - **ENGINEERING DECISION:** We eliminate false accusations through our **5-State Compliance Model**:
    1. `NO_IMAGE_VERIFIABLE_VIOLATION_DETECTED` (Green): Fully satisfies all statutory checks.
    2. `MANUAL_REVIEW_REQUIRED` (Amber): Confidence $<80\%$ or font size within our $0.10\text{mm}$ benefit-of-doubt buffer.
    3. `POTENTIAL_NON_COMPLIANCE` (Red): Clear mathematical discrepancy or severe font deficit.
- **Evidence:** 5-state result cards in web UI.

#### Q26: "How did you establish ground truth font heights for your benchmark?"
- **Answer:**
  - **FACT:** Handheld calipers on 1.0mm ink text have human parallax variance of $\pm 0.10\text{mm}$.
  - **ENGINEERING DECISION:** Ground truth was established using **high-resolution 1200 DPI flatbed optical scans ($0.021\text{mm/pixel}$)** where two independent raters measured character stroke heights using digital reticles. Digital calipers were used for outer package dimensions ($H \times W$) and as a physical reference prop.
- **Evidence:** Digital caliper sitting on jury table + benchmark protocol document.

#### Q27: "What happens if a package is torn, crumpled, or partially occluded?"
- **Answer:**
  - **ENGINEERING DECISION:** If surface deformation prevents planar scale recovery or tears characters, OCR confidence drops below threshold. The system flags: `MANUAL_REVIEW_REQUIRED — Packaging Surface Deformed / Occluded`. It never guesses corrupted data.
- **Evidence:** Error handling state machine in rule engine.

#### Q28: "How does the system know which product category a package belongs to for category-specific exceptions?"
- **Answer:**
  - **ENGINEERING DECISION:** The normalizer matches extracted generic commodity names against the FSSAI / National Product Catalog taxonomy (e.g. identifying toothpaste, sanitizer, or confectionery). If category classification is ambiguous, the system prompts the inspector with a 1-tap category confirmation dropdown.
- **Evidence:** Category taxonomy mapping module in `modules/rules/category_taxonomy.py`.

#### Q29: "Can this system verify if a factory physically exists at the declared PIN code?"
- **Answer:**
  - **FACT:** Monocular computer vision can verify the *presence* and *syntactic completeness* of the address (6-digit Indian PIN code, state name, keywords "Mfg by").
  - **LIMITATION:** Verifying whether a physical factory building exists at that location requires an API query to MCA21 / GSTN or an on-site officer inspection. We classify address verification as **Partially Verifiable** and explicitly declare this boundary.
- **Evidence:** Statutory capability boundary table in `docs/LEGAL_RULE_MATRIX.md`.

#### Q30: "Why did you build this as a web application / PWA instead of a native Android APK?"
- **Answer:**
  - **ENGINEERING DECISION:** A Progressive Web Application (PWA) with local FastAPI backend provides 100% platform portability across Android phones, iPads, laptops, and field tablets with zero installation friction or app-store gatekeeping. Field officers can launch it instantly while retaining full offline camera hardware access.
- **Evidence:** Responsive web application running smoothly on mobile viewports.

#### Q31: "How do you update rules when the Ministry issues new Gazette amendments in the future?"
- **Answer:**
  - **ENGINEERING DECISION:** Our rule engine is completely decoupled from the computer vision models. Every rule is codified as an isolated, versioned Python class inheriting from an abstract `BaseStatutoryRule` schema with `effective_from` dates. When a new Gazette notification is published, a developer adds a new rule class or updates the parameter table without retraining OCR or touching computer vision algorithms.
- **Evidence:** Clean object-oriented rule architecture in `modules/rules/base_rule.py`.

#### Q32: "What is your biggest competitive advantage over other student teams in this hackathon?"
- **Answer:**
  - **ENGINEERING DECISION:** Other teams will present generic OCR wrappers: an uncalibrated script or an end-to-end ChatGPT prompt that hallucinates legal rules and has zero optical physics.
  - **OUR THREEFOLD TECHNICAL MOAT:**
    1. *Metric Scale Calibration:* We solve the monocular scale ambiguity using a standard 10-Rupee coin or ISO card, enabling physical font measurement.
    2. *Deterministic Statutory Engine:* We codified Gazette clauses, Unit Sale Price arithmetic, and the Jan Vishwas (Amendment of Provisions) Act, 2026 Improvement Notice framework into an audit-proof Python state machine.
    3. *100% In-Room Ground Truth:* We take any physical package sitting on your table right now, scan it live in 2 seconds, and defend every millimeter with this digital caliper.
- **Evidence:** The live demonstration just executed.
