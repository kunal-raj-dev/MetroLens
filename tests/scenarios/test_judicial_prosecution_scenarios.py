"""
End-to-End Judicial Prosecution & Enforcement Scenarios Test Suite
==================================================================
Comprehensive scenario test suite simulating realistic multi-party statutory
enforcement workflows under the Legal Metrology Act, 2009, Packaged Commodities
Rules, 2011, and Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS).

Scenarios Covered:
------------------
1. Short-Weight Edible Oil Seizure & BNSS Complaint Filing before Judicial Magistrate.
2. FMCG Rule 6 Declaration Omission & Section 48 Compounding with Cyber Treasury Reconciliation.
3. Industrial Recidivist (IS 1489 Cement): 3-Year Lookback Bar & Mandatory Criminal Trial.
4. E-Commerce Dark Store Raid & Section 49 Form I Corporate Director Liability Attribution.
5. Unregistered Corporate Packer: Arraignment of Managing Director under Section 49(1) Proviso.
6. Multi-Node Cluster Failover & Event Sourcing Audit Chain Replay.
7. Full-Spectrum Physical Metrology Inspection Pipeline (Unwrapping + Stroke Profiling + Barcode + PDF).
"""

import datetime
import io
import pytest
import numpy as np
import cv2
from PIL import Image, ImageDraw

# Vision Metrology
from apps.api.verification.geometric_unwrapping import (
    GeometricUnwrapper,
    CylinderParameters,
    SurfaceType,
)
from apps.api.verification.stroke_profile import (
    StrokeProfiler,
    StrokeVerdict,
)
from apps.api.verification.barcode_verifier import (
    BarcodeVerifier,
    ISOGrade,
)

# Judicial Subsystem
from apps.api.judicial.case_docket import (
    DocketBuilder,
    LegalMetrologyOffence,
    PartyRole,
    ProsecutionDocket,
)
from apps.api.judicial.compounding_ledger import (
    CompoundingLedger,
    CompoundingStatus,
    OffenceRecidivismLevel,
    TreasuryChallanReceipt,
)
from apps.api.judicial.corporate_liability import (
    CorporateEntity,
    CorporateLiabilityEvaluator,
    DirectorRecord,
    DirectorType,
    FormINomination,
    NominationStatus,
)

# Evidentiary Reporting Subsystem
from nirikshak_reporting.compounding_agreement import (
    CompoundingAgreementCompiler,
    CompoundingOrderData,
)
from nirikshak_reporting.seizure_memo import (
    SeizureMemoCompiler,
    SeizureMemoPayload,
    SeizedStockItem,
)
from nirikshak_reporting.district_enforcement_report import (
    DistrictEnforcementReportCompiler,
    DistrictEnforcementPayload,
    SectorMetric,
    RecidivistEntityRecord,
)

# Distributed Enterprise Services
from apps.api.services.leader_election import LeaderElectionCoordinator, NodeRole
from apps.api.services.event_sourcing import EventStore, InspectionAggregate
from apps.api.services.adaptive_rate_limiter import AdaptiveRateLimiter, ClientTier


# =============================================================================
# SCENARIO 1: Short-Weight Edible Oil Seizure & BNSS Complaint Docket
# =============================================================================

class TestScenario1ShortWeightSeizureAndProsecution:
    """
    Simulates:
    1. Inspecting officer visits retail establishment, verifies 1L edible oil pouch.
    2. Working standard shows 940 ml (short-measure of 60 ml exceeding Max Permissible Error).
    3. Rule 29 Seizure Memo is executed on-site with 2 independent Panch witnesses.
    4. Formal complaint docket is drafted under Section 190 BNSS and sealed with SHA-256 hash.
    5. Seizure Memo PDF is compiled for submission to the court.
    """

    def test_complete_edible_oil_seizure_and_docket_lifecycle(self):
        # 1. Prepare Seizure Inventory
        seized_items = [
            SeizedStockItem(
                item_sno=1,
                commodity_description="Refined Mustard Oil (Pouch)",
                brand_name="Kisan Pure",
                batch_or_lot_no="KP-2026-B11",
                declared_net_quantity="1 Litre",
                test_measured_quantity="940 ml",
                declared_mrp_inr=185.0,
                units_seized_count=20,
                security_seal_number="SEAL-KA-2026-901",
                contravention_alleged="Section 36(2) - Short Measure of 60 ml (MPE: 15 ml)",
            )
        ]

        seizure_payload = SeizureMemoPayload(
            seizure_memo_number="SEIZURE-2026-BLR-101",
            inspection_id="INSP-KA-2026-8812",
            date_of_seizure=datetime.date(2026, 3, 1),
            time_commenced="11:00 AM",
            time_concluded="01:30 PM",
            place_of_search_address="M/s National Grocery Mart, BTM Layout 2nd Stage, Bengaluru",
            police_station_jurisdiction="Madiwala Police Station",
            district="Bengaluru Urban",
            state="Karnataka",
            officer_name="Shri T. S. Venkatesh",
            officer_designation="Senior Inspector of Legal Metrology",
            officer_id_number="LM-INS-KA-118",
            occupier_name="Shri Arvind Shah",
            occupier_father_or_spouse="Shri Mohanlal Shah",
            occupier_designation="Proprietor",
            occupier_firm_name="National Grocery Mart",
            witness_1_name="Ramesh Gowda",
            witness_1_age=45,
            witness_1_father="Kempe Gowda",
            witness_1_address="No 14, 7th Main, BTM Layout, Bengaluru",
            witness_1_id="Aadhaar: XXXX-XXXX-4411",
            witness_2_name="Prakash Rao",
            witness_2_age=39,
            witness_2_father="Subba Rao",
            witness_2_address="No 88, 12th Cross, BTM Layout, Bengaluru",
            witness_2_id="Voter ID: KAR-BLR-88991",
            working_standard_weight_box_id="WS-KA-BLR-04",
            working_standard_last_verified=datetime.date(2026, 1, 15),
            seized_items=seized_items,
            custodial_malkhana_destination="Malkhana, O/o Assistant Controller South, Bengaluru",
        )

        # 2. Compile court-admissible Seizure Memo PDF
        seizure_compiler = SeizureMemoCompiler()
        pdf_bytes = seizure_compiler.compile_seizure_memo_pdf(seizure_payload)
        assert len(pdf_bytes) > 2000
        assert pdf_bytes.startswith(b"%PDF-")

        # 3. Assemble BNSS Section 190 Complaint Docket
        builder = DocketBuilder(
            docket_id="DOCKET-2026-KA-SHORT-01",
            district="Bengaluru Urban",
            state="Karnataka",
        )
        builder.set_court_details(
            court_name="Court of Chief Judicial Magistrate, Bengaluru Urban",
            police_station="Madiwala Police Station",
        )
        builder.set_investigating_officer(
            name="Shri T. S. Venkatesh",
            designation="Senior Inspector of Legal Metrology",
            gazette_no="GAZ-BLR-2023-112",
        )
        # Corporate Manufacturer
        builder.add_accused_corporate(
            party_id="ACCUSED-1",
            company_name="Kisan Agro Foods Pvt Ltd",
            cin="U15140KA2016PTC089771",
            pan="AAACK9988P",
            gstin="29AAACK9988P1Z4",
            registered_office="Plot 18, Industrial Area, Nelamangala, Bengaluru Rural",
            charges=[
                LegalMetrologyOffence.SEC_18_NON_STANDARD_PACKAGE,
                LegalMetrologyOffence.SEC_36_2_SHORT_WEIGHT_MEASURE,
            ],
        )
        # Retailer Occupier
        builder.add_accused_individual(
            party_id="ACCUSED-2",
            role=PartyRole.ACCUSED_RETAILER,
            full_name="Shri Arvind Shah",
            designation="Proprietor, National Grocery Mart",
            din=None,
            residential_address="Flat 204, BTM Residency, Bengaluru",
            charges=[LegalMetrologyOffence.SEC_36_1_PACKAGING_CONTRAVENTION],
        )
        builder.set_facts_and_chronology(
            synopsis=(
                "On 01-03-2026, an inspection of M/s National Grocery Mart revealed 20 pouches of "
                "Kisan Pure 1L Mustard Oil delivering only 940 ml, short by 60 ml, violating Section 36(2)."
            ),
            events=[
                ("2026-03-01T11:00:00", "Locus Search Commenced", "Search initiated in presence of Panch witnesses"),
                ("2026-03-01T11:45:00", "Volumetric Verification", "Calibrated burette proved 60 ml short-fill"),
                ("2026-03-01T12:30:00", "Seizure Executed", "20 packets seized and sealed under tag SEAL-KA-2026-901"),
            ],
        )
        builder.add_panchnama_witness(
            witness_no=1,
            name="Ramesh Gowda",
            age=45,
            father_or_spouse="Kempe Gowda",
            address="No 14, 7th Main, BTM Layout, Bengaluru",
            phone="9845012345",
            id_type="Aadhaar",
            id_masked="XXXX-XXXX-4411",
            statement="I was present throughout the search. The inspector measured the oil and it was short.",
        )
        builder.add_seized_exhibit(
            exhibit_id="Ex-P1",
            commodity="Refined Mustard Oil",
            brand="Kisan Pure",
            batch="KP-2026-B11",
            declared_qty="1 Litre",
            measured_qty="940 ml",
            mrp=185.0,
            mfg_date="2026-02-01",
            origin="India",
            seal_tag="SEAL-KA-2026-901",
            custody_loc="Malkhana South",
            photo_hashes=["B" * 64],
        )

        docket = builder.build_and_seal()

        # 4. Verify Cryptographic Integrity
        assert docket.verify_integrity() is True
        assert len(docket.docket_sha256_seal) == 64
        assert docket.prayer.issue_summons is True
        assert docket.prayer.request_forfeiture_of_seized_stock is True


# =============================================================================
# SCENARIO 2: FMCG Rule 6 Omission & Section 48 Compounding Lifecycle
# =============================================================================

class TestScenario2CompoundingLifecycle:
    """
    Simulates:
    1. First-time offender (biscuit manufacturer) omitted Unit Sale Price (USP) under Rule 6(1)(e).
    2. Section 48 eligibility assessment verifies clean 3-year record -> Approved.
    3. Statutory Compounding Notice issued assessing ₹15,000 fee.
    4. Cyber Treasury e-Challan payment received and reconciled against Head of Account 0435.
    5. Section 48(3) Statutory Order of Discharge compiled as signed PDF.
    """

    def test_complete_compounding_lifecycle_and_discharge(self):
        ledger = CompoundingLedger()

        # 1. Assess Eligibility
        assessment = ledger.assess_eligibility(
            gstin="29AAACB8899K1Z2",
            pan="AAACB8899K",
            statutory_section="Rule 6",
            date_of_commission=datetime.date(2026, 2, 20),
        )
        assert assessment.is_compoundable is True
        assert assessment.recidivism_level == OffenceRecidivismLevel.FIRST_OFFENCE

        # 2. Issue Compounding Notice
        notice = ledger.create_compounding_notice(
            case_number="CMP-2026-BLR-055",
            inspection_id="INSP-2026-9901",
            offender_name="Royal Bakes & Confectionery Pvt Ltd",
            gstin="29AAACB8899K1Z2",
            pan_number="AAACB8899K",
            offence_type="Omission of Unit Sale Price (USP)",
            statutory_section="Rule 6",
            date_of_commission=datetime.date(2026, 2, 20),
            assessed_fee_inr=15000.0,
        )
        assert notice.status == CompoundingStatus.NOTICE_ISSUED

        # 3. Pay via Cyber Treasury e-Challan
        challan = TreasuryChallanReceipt(
            challan_number="KA-CYBER-TR-2026-009811",
            bank_reference_utr="ICICIN0088991122",
            amount_inr=15000.0,
            remitter_name="Royal Bakes & Confectionery Pvt Ltd",
            cyber_treasury_auth_code="AUTH-CT-99120",
        )
        updated = ledger.record_treasury_challan("CMP-2026-BLR-055", challan)
        assert updated.status == CompoundingStatus.PAYMENT_VERIFIED

        # 4. Grant Discharge Order
        discharged = ledger.issue_discharge_order("CMP-2026-BLR-055", authorized_officer="Assistant Controller South")
        assert discharged.status == CompoundingStatus.DISCHARGE_ORDER_ISSUED
        assert "DISCHARGE-SEC48" in discharged.discharge_order_number

        # 5. Compile Section 48 Statutory Order PDF
        order_data = CompoundingOrderData(
            order_number=discharged.discharge_order_number,
            case_reference="CMP-2026-BLR-055",
            inspection_id="INSP-2026-9901",
            date_of_order=datetime.date.today(),
            state_government_name="Karnataka",
            department_name="Department of Consumer Affairs & Legal Metrology",
            authorized_officer_name="Shri P. B. Patil",
            authorized_officer_designation="Assistant Controller of Legal Metrology",
            authorized_officer_station="Bengaluru South Division",
            offender_entity_name="Royal Bakes & Confectionery Pvt Ltd",
            offender_cin_or_reg="U15412KA2017PTC099123",
            offender_gstin="29AAACB8899K1Z2",
            offender_pan="AAACB8899K",
            offender_address="Plot 5, Electronic City Phase 2, Bengaluru",
            director_or_proprietor_name="Shri Rajesh Sharma",
            statutory_offences_compounded=["Rule 6(1)(e): Omission of Unit Sale Price"],
            date_of_offence_commission=datetime.date(2026, 2, 20),
            inspection_location="Supermarket Mart, Koramangala, Bengaluru",
            compounding_fee_inr=15000.0,
            treasury_challan_number=challan.challan_number,
            treasury_payment_date=datetime.date.today(),
            bank_utr_reference=challan.bank_reference_utr,
        )

        agreement_compiler = CompoundingAgreementCompiler()
        pdf_bytes = agreement_compiler.compile_order_pdf(order_data)
        assert len(pdf_bytes) > 2000
        assert pdf_bytes.startswith(b"%PDF-")


# =============================================================================
# SCENARIO 3: Recidivist Cement Packer (IS 1489) - 3-Year Lookback Bar
# =============================================================================

class TestScenario3CementRecidivistBarred:
    """
    Simulates:
    1. Cement packer compounded short weight under Section 36 in Sept 2024.
    2. In March 2026 (18 months later), another short weight violation is detected.
    3. Under Section 48(2), compounding is STRICTLY BARRED (3-year statutory lookback window).
    4. Compounding is rejected; case is escalated to criminal court trial.
    """

    def test_recidivism_triggers_statutory_bar_and_prosecution(self):
        ledger = CompoundingLedger()

        # Step 1: Record 2024 compounding
        rec1 = ledger.create_compounding_notice(
            case_number="CMP-2024-CEMENT-01",
            inspection_id="INSP-2024-041",
            offender_name="Deccan Cements & Building Products Ltd",
            gstin="29AAACD9900P1Z8",
            pan_number="AAACD9900P",
            offence_type="Short Weight in 50kg Bag (IS 1489)",
            statutory_section="Section 36(1)",
            date_of_commission=datetime.date(2024, 9, 10),
            assessed_fee_inr=35000.0,
        )
        ch1 = TreasuryChallanReceipt(
            challan_number="KA-TR-2024-0012",
            bank_reference_utr="SBIN00441199",
            amount_inr=35000.0,
        )
        ledger.record_treasury_challan("CMP-2024-CEMENT-01", ch1)
        discharged1 = ledger.issue_discharge_order("CMP-2024-CEMENT-01")
        discharged1.discharge_date = datetime.date(2024, 9, 25)

        # Step 2: Repeat Offence in March 2026
        eligibility = ledger.assess_eligibility(
            gstin="29AAACD9900P1Z8",
            pan="AAACD9900P",
            statutory_section="Section 36(1)",
            date_of_commission=datetime.date(2026, 3, 10),
        )

        assert eligibility.is_compoundable is False
        assert eligibility.recidivism_level == OffenceRecidivismLevel.REPEAT_WITHIN_3_YEARS
        assert "STRICTLY NON-COMPOUNDABLE" in eligibility.statutory_reasoning

        # Step 3: Record notice in ledger -> Auto-rejected as recidivist
        rec2 = ledger.create_compounding_notice(
            case_number="CMP-2026-CEMENT-09",
            inspection_id="INSP-2026-099",
            offender_name="Deccan Cements & Building Products Ltd",
            gstin="29AAACD9900P1Z8",
            pan_number="AAACD9900P",
            offence_type="Short Weight in 50kg Bag (IS 1489)",
            statutory_section="Section 36(1)",
            date_of_commission=datetime.date(2026, 3, 10),
        )
        assert rec2.status == CompoundingStatus.REJECTED_RECIDIVIST

        # Step 4: Escalate to Criminal Prosecution
        escalated = ledger.escalate_to_court_prosecution(
            case_number="CMP-2026-CEMENT-09",
            reason="Repeat contravention within 36 months barred under Section 48(2)",
        )
        assert escalated.status == CompoundingStatus.ESCALATED_TO_COURT


# =============================================================================
# SCENARIO 4: E-Commerce Dark Store Raid & Form I Director Protection
# =============================================================================

class TestScenario4EcommerceFormINomination:
    """
    Simulates:
    1. Raid on quick-commerce automated warehouse reveals dual MRP sticker violation.
    2. Investigating officer audits Ministry of Corporate Affairs records.
    3. Finds active Form I nomination registered with the Controller under Rule 29.
    4. Evaluator shields Chief Executive Officer / Managing Director and arraigns
       the nominated compliance director under Section 49(2).
    """

    def test_form_i_director_attribution(self):
        nomination = FormINomination(
            nomination_id="FORM-I-BLR-2023",
            nominated_director_din="08123456",
            nominated_director_name="Shri Sandeep Aggarwal",
            residential_address="Penthouse 12, Indiranagar, Bengaluru",
            jurisdiction_scope="PAN_INDIA",
            board_resolution_date=datetime.date(2023, 6, 1),
            filing_date_with_controller=datetime.date(2023, 6, 15),
            acknowledgement_number="CLM/BLR/NOM/2023/881",
            status=NominationStatus.ACTIVE_VALID,
            effective_from=datetime.date(2023, 6, 15),
        )

        company = CorporateEntity(
            cin="U72900KA2020PTC134567",
            company_name="QuickCart Hyperlocal Retail Technologies Pvt Ltd",
            registered_office_address="Tech Village, Outer Ring Road, Bengaluru",
            pan_number="AAACQ7788L",
            gstin="29AAACQ7788L1ZN",
            directors=[
                DirectorRecord(
                    din="00099881",
                    full_name="Shri Bhavish Sharma (CEO & Managing Director)",
                    director_type=DirectorType.MANAGING_DIRECTOR,
                    appointment_date=datetime.date(2020, 1, 1),
                ),
                DirectorRecord(
                    din="08123456",
                    full_name="Shri Sandeep Aggarwal",
                    director_type=DirectorType.NOMINATED_DIRECTOR_FORM_I,
                    appointment_date=datetime.date(2022, 4, 1),
                ),
            ],
            form_i_nominations=[nomination],
        )

        evaluator = CorporateLiabilityEvaluator()
        result = evaluator.evaluate_liability(
            company,
            offence_date=datetime.date(2026, 2, 25),
            manufacturing_unit_location="Dark Store #14, HSR Layout, Bengaluru",
        )

        assert result.has_valid_form_i_nomination is True
        arraigned = [p["name"] for p in result.parties_to_arraign]
        assert "QuickCart Hyperlocal Retail Technologies Pvt Ltd" in arraigned
        assert "Shri Sandeep Aggarwal" in arraigned
        assert "Shri Bhavish Sharma (CEO & Managing Director)" not in arraigned

        # Confirm Managing Director is in protected list
        protected = [p["name"] for p in result.parties_protected_from_prosecution]
        assert "Shri Bhavish Sharma (CEO & Managing Director)" in protected


# =============================================================================
# SCENARIO 5: Unregistered Corporate Packer: Personal Liability of MD
# =============================================================================

class TestScenario5UnregisteredCorporatePackerMDLiable:
    """
    Simulates:
    1. Manufacturing entity commits Section 36 violation.
    2. Company never registered a Form I Director Nomination under Rule 29.
    3. Evaluator applies Section 49(1) proviso, arraigning the Managing Director
       personally as an officer-in-default.
    """

    def test_missing_form_i_holds_managing_director_criminally_liable(self):
        company = CorporateEntity(
            cin="U15200MH2019PTC112233",
            company_name="Apex Dairy & Beverages Pvt Ltd",
            registered_office_address="Plot 8, MIDC, Andheri East, Mumbai",
            pan_number="AAACA3344J",
            gstin="27AAACA3344J1ZK",
            directors=[
                DirectorRecord(
                    din="01234567",
                    full_name="Shri Vikramaditya Singhania",
                    director_type=DirectorType.MANAGING_DIRECTOR,
                    appointment_date=datetime.date(2019, 5, 10),
                ),
                DirectorRecord(
                    din="09876543",
                    full_name="Justice (Retd) R. K. Varma",
                    director_type=DirectorType.INDEPENDENT_DIRECTOR,
                    appointment_date=datetime.date(2020, 1, 15),
                ),
            ],
            form_i_nominations=[],  # No Form I nomination filed!
        )

        evaluator = CorporateLiabilityEvaluator()
        result = evaluator.evaluate_liability(company, offence_date=datetime.date(2026, 3, 1))

        assert result.has_valid_form_i_nomination is False
        arraigned = [p["name"] for p in result.parties_to_arraign]
        assert "Apex Dairy & Beverages Pvt Ltd" in arraigned
        assert "Shri Vikramaditya Singhania" in arraigned  # MD is arraigned!

        # Independent director protected under Companies Act Sec 149(12)
        protected = [p["name"] for p in result.parties_protected_from_prosecution]
        assert "Justice (Retd) R. K. Varma" in protected


# =============================================================================
# SCENARIO 6: Multi-Node Cluster Failover & Event Sourcing Audit Chain Replay
# =============================================================================

class TestScenario6ClusterFailoverAndEventSourcing:
    """
    Simulates:
    1. Primary gateway node `node-01` acquires leadership lease and fencing token.
    2. `node-01` processes inspection event stream into EventStore.
    3. Sudden partition: `node-01` loses heartbeats from peers `node-02` and `node-03`.
    4. `node-01` detects quorum loss and relinquishes leadership.
    5. `node-02` acquires lease with incremented fencing token.
    6. `node-02` replays entire event stream from EventStore and proves 100% cryptographic integrity.
    """

    def test_cluster_failover_and_audit_continuity(self):
        # 1. Primary node acquires leadership
        node1 = LeaderElectionCoordinator(
            local_node_id="node-01",
            cluster_peers=["node-02", "node-03"],
            lease_ttl_seconds=4.0,
            heartbeat_interval_seconds=1.0,
        )
        node1.record_peer_heartbeat("node-02")
        node1.record_peer_heartbeat("node-03")
        acq1, lease1 = node1.try_acquire_or_renew_lease()
        assert acq1 is True
        assert lease1.leader_node_id == "node-01"

        # 2. Ingest domain events via EventStore
        store = EventStore()
        agg = InspectionAggregate(inspection_id="INSP-CLUSTER-FAILOVER-01")
        agg.submit_inspection(raw_image_sha256="A" * 64)
        agg.record_sanitization(sanitized_sha256="B" * 64)
        agg.record_forensics(tamper_score=0.01, is_authentic=True)
        agg.record_ocr(declarations={"mrp": "₹200", "net_qty": "1L"})
        agg.record_rule_evaluation(violations=["Rule 7 font height non-compliant"])

        store.append_events("INSP-CLUSTER-FAILOVER-01", agg.get_uncommitted_events(), expected_version=0)
        agg.mark_events_committed()

        # 3. Simulate network partition for node-01
        stale_time = datetime.datetime.now() - datetime.timedelta(seconds=15)
        node1._nodes["node-02"].last_heartbeat = stale_time
        node1._nodes["node-03"].last_heartbeat = stale_time
        acq_renew, _ = node1.try_acquire_or_renew_lease()
        assert acq_renew is False
        assert node1.get_diagnostics().local_node_role == NodeRole.QUORUM_LOST

        # 4. Standby node-02 acquires leadership
        node2 = LeaderElectionCoordinator(
            local_node_id="node-02",
            cluster_peers=["node-01", "node-03"],
            lease_ttl_seconds=4.0,
            heartbeat_interval_seconds=1.0,
            initial_fencing_token=lease1.fencing_token,
        )
        node2.record_peer_heartbeat("node-03")
        acq2, lease2 = node2.try_acquire_or_renew_lease()
        assert acq2 is True
        assert lease2.leader_node_id == "node-02"
        assert lease2.fencing_token > lease1.fencing_token  # Monotonic fencing token increased!

        # 5. Node-02 verifies and replays aggregate from EventStore
        reloaded = store.load_aggregate("INSP-CLUSTER-FAILOVER-01")
        assert reloaded is not None
        assert reloaded.version == 5
        assert reloaded.state.overall_verdict == "NON_COMPLIANT"

        # Cryptographic Merkle chain remains intact
        intact, msg = store.verify_stream_integrity("INSP-CLUSTER-FAILOVER-01")
        assert intact is True


# =============================================================================
# SCENARIO 7: Full-Spectrum Physical Metrology Inspection Pipeline
# =============================================================================

class TestScenario7FullMetrologyPipeline:
    """
    Simulates:
    1. Input image of cylindrical beverage can with warped text.
    2. GeometricUnwrapper performs reverse cylinder projection.
    3. StrokeProfiler checks Rule 7 font height, width, and stroke thickness.
    4. BarcodeVerifier evaluates ISO 15416 print quality and cross-corroborates MRP/Net Qty.
    5. Merkle event log records full pipeline.
    6. Executive enforcement report is generated for the District Magistrate.
    """

    def test_end_to_end_vision_metrology_and_dossier_pipeline(self):
        # 1. Synthetic cylindrical container image
        h, w = 180, 260
        img = np.full((h, w, 3), 230, dtype=np.uint8)
        # Text line
        cv2.putText(img, "MRP Rs 99", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (20, 20, 20), 2)
        # Barcode strip
        for x in range(30, 200, 6):
            cv2.line(img, (x, 120), (x, 160), (10, 10, 10), 2)

        # 2. Geometric unwrapping
        unwrapper = GeometricUnwrapper()
        cyl_params = CylinderParameters(axis_x=130.0, radius=110.0)
        unwrap_res = unwrapper.unwrap_cylinder(img, cyl_params)
        assert unwrap_res.rectified_image is not None
        assert unwrap_res.surface_type == SurfaceType.CYLINDRICAL

        # 3. Rule 7 Sub-pixel Stroke Profiler
        profiler = StrokeProfiler(min_glyph_pixels=6)
        stroke_report = profiler.analyze_roi(
            roi_image=unwrap_res.rectified_image[60:110, 20:200],
            expected_text="MRP Rs 99",
            pixels_per_mm=10.0,
            statutory_min_height_mm=1.5,
            declaration_key="mrp",
        )
        assert stroke_report.detailed_line_profile.num_glyphs > 0

        # 4. Barcode ISO 15416 Verification
        verifier = BarcodeVerifier(num_scanlines=6)
        barcode_roi = unwrap_res.rectified_image[115:165, 25:210]
        barcode_res = verifier.verify_barcode(
            barcode_roi,
            human_readable_ocr={"mrp": "99.00", "net_quantity": "250 ml"},
        )
        assert barcode_res.iso_grading.symbol_contrast > 0.0

        # 5. Compile Executive District Report
        payload = DistrictEnforcementPayload(
            report_reference_id="REP-SCENARIO-7-BLR",
            reporting_period_start=datetime.date(2026, 1, 1),
            reporting_period_end=datetime.date(2026, 3, 31),
            district_name="Bengaluru Urban",
            state_name="Karnataka",
            controller_division="Southern Zone",
            reporting_officer_name="Shri K. L. Rao",
            reporting_officer_designation="Senior Metrology Inspector",
            total_inspections=10,
            compliant_inspections=8,
            non_compliant_inspections=2,
            statutory_notices_issued=2,
            compounding_cases_concluded=1,
            total_compounding_revenue_inr=25000.0,
            court_prosecutions_filed=1,
            seizures_executed_count=1,
            sector_metrics=[
                SectorMetric(
                    sector_name="Beverages & Canned Foods",
                    inspections_count=10,
                    violations_count=2,
                    compliance_percentage=80.0,
                    compounding_fees_inr=25000.0,
                    prosecutions_count=1,
                )
            ],
            recidivist_entities=[],
            executive_recommendations=["Maintain surveillance on high-volume beverage bottling lines."],
        )
        report_compiler = DistrictEnforcementReportCompiler()
        report_pdf = report_compiler.compile_district_report_pdf(payload)
        assert len(report_pdf) > 2500
        assert report_pdf.startswith(b"%PDF-")
