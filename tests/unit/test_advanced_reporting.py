"""
Unit Test Suite for Advanced Statutory Evidentiary Reporting Subsystem
=====================================================================
Tests Section 48 Compounding Agreements, Rule 29 Seizure Memos / Panchnamas,
and District Metrology Enforcement Intelligence reports.
"""

import datetime
import pytest

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


class TestCompoundingAgreementCompiler:
    """Test suite for Section 48 statutory compounding deeds & discharge orders."""

    @pytest.fixture
    def sample_order_payload(self):
        return CompoundingOrderData(
            order_number="DISCHARGE-SEC48-2026-KA-0012",
            case_reference="CASE-LM-2026-778",
            inspection_id="INSP-KA-88990",
            date_of_order=datetime.date(2026, 3, 2),
            state_government_name="Karnataka",
            department_name="Department of Consumer Affairs & Legal Metrology",
            authorized_officer_name="Shri P. B. Patil",
            authorized_officer_designation="Assistant Controller of Legal Metrology",
            authorized_officer_station="Bengaluru South Division",
            offender_entity_name="Sunrise Confectionery Pvt Ltd",
            offender_cin_or_reg="U15122KA2018PTC109876",
            offender_gstin="29AABCS1234F1Z9",
            offender_pan="AABCS1234F",
            offender_address="Plot 10, Bommasandra Industrial Area, Bengaluru",
            director_or_proprietor_name="Shri Ramesh Gupta",
            statutory_offences_compounded=[
                "Rule 6(1)(e): Omission of Unit Sale Price (USP)",
                "Rule 7: Font height below minimum 2.0 mm",
            ],
            date_of_offence_commission=datetime.date(2026, 2, 10),
            inspection_location="Supermarket Mart, Koramangala 4th Block, Bengaluru",
            compounding_fee_inr=20000.0,
            treasury_challan_number="KA-CYBER-TR-2026-445566",
            treasury_payment_date=datetime.date(2026, 2, 28),
            bank_utr_reference="SBIN004455667788",
            panchnama_reference="SEIZURE-2026-091",
        )

    def test_compile_compounding_order_pdf(self, sample_order_payload):
        compiler = CompoundingAgreementCompiler()
        pdf_bytes = compiler.compile_order_pdf(sample_order_payload)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 2000
        assert pdf_bytes.startswith(b"%PDF-")


class TestSeizureMemoCompiler:
    """Test suite for Rule 29 Search & Seizure Memos and Panchnamas."""

    @pytest.fixture
    def sample_seizure_payload(self):
        items = [
            SeizedStockItem(
                item_sno=1,
                commodity_description="Pure Ghee (Carton Pack)",
                brand_name="Gokul Fresh",
                batch_or_lot_no="GKL-2026-01",
                declared_net_quantity="1 Litre",
                test_measured_quantity="945 ml",  # Short measure
                declared_mrp_inr=650.0,
                units_seized_count=12,
                security_seal_number="SEAL-KA-991201",
                contravention_alleged="Section 36(2) - Short Measure of 55 ml",
            ),
            SeizedStockItem(
                item_sno=2,
                commodity_description="Refined Sunflower Oil",
                brand_name="Gold Sun",
                batch_or_lot_no="GS-776",
                declared_net_quantity="5 Litre",
                test_measured_quantity="4.82 Litre",
                declared_mrp_inr=780.0,
                units_seized_count=6,
                security_seal_number="SEAL-KA-991202",
                contravention_alleged="Section 36(2) & Rule 6 - Short Measure & Missing FOPNL",
            ),
        ]

        return SeizureMemoPayload(
            seizure_memo_number="SEIZURE-2026-BLR-042",
            inspection_id="INSP-2026-0042",
            date_of_seizure=datetime.date(2026, 3, 3),
            time_commenced="10:30 AM",
            time_concluded="01:45 PM",
            place_of_search_address="M/s City Wholesale Traders, APMC Yard, Yeshwanthpur, Bengaluru",
            police_station_jurisdiction="Yeshwanthpur Police Station",
            district="Bengaluru Urban",
            state="Karnataka",
            officer_name="Shri V. S. Nayak",
            officer_designation="Inspector of Legal Metrology",
            officer_id_number="LM-INS-KA-441",
            occupier_name="Shri Harish Patel",
            occupier_father_or_spouse="Shri Manilal Patel",
            occupier_designation="Proprietor",
            occupier_firm_name="City Wholesale Traders",
            witness_1_name="Suresh Babu",
            witness_1_age=42,
            witness_1_father="Babu Rao",
            witness_1_address="Shop 14, APMC Yard, Yeshwanthpur",
            witness_1_id="Voter ID: ABC1234567",
            witness_2_name="Dinesh Hegde",
            witness_2_age=36,
            witness_2_father="Ganesh Hegde",
            witness_2_address="Shop 22, APMC Yard, Yeshwanthpur",
            witness_2_id="Aadhaar: XXXX-XXXX-9988",
            working_standard_weight_box_id="WS-KA-2024-BOX-12",
            working_standard_last_verified=datetime.date(2025, 12, 10),
            seized_items=items,
            custodial_malkhana_destination="Central Evidence Locker, O/o Assistant Controller South",
        )

    def test_compile_seizure_memo_pdf(self, sample_seizure_payload):
        compiler = SeizureMemoCompiler()
        pdf_bytes = compiler.compile_seizure_memo_pdf(sample_seizure_payload)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 2500
        assert pdf_bytes.startswith(b"%PDF-")


class TestDistrictEnforcementReportCompiler:
    """Test suite for District Metrology Intelligence and Recidivism dossiers."""

    @pytest.fixture
    def sample_district_payload(self):
        sectors = [
            SectorMetric(
                sector_name="Packaged Food & Edible Oils",
                inspections_count=150,
                violations_count=22,
                compliance_percentage=85.3,
                compounding_fees_inr=275000.0,
                prosecutions_count=4,
            ),
            SectorMetric(
                sector_name="Cement & Building Materials (IS 1489/IS 269)",
                inspections_count=60,
                violations_count=12,
                compliance_percentage=80.0,
                compounding_fees_inr=350000.0,
                prosecutions_count=3,
            ),
            SectorMetric(
                sector_name="E-Commerce Dark Stores & Warehouses",
                inspections_count=45,
                violations_count=18,
                compliance_percentage=60.0,
                compounding_fees_inr=180000.0,
                prosecutions_count=6,
            ),
        ]

        recidivists = [
            RecidivistEntityRecord(
                entity_name="Apex Logistics & Retail Mart Ltd",
                cin_or_gstin="U74999KA2019PLC098123 / 29AAACA9988F1Z2",
                registered_district="Bengaluru Urban",
                prior_violations_count=3,
                most_recent_offence_date=datetime.date(2026, 2, 18),
                statutory_sections_violated=["Section 36(1)", "Rule 18(2)"],
                has_valid_form_i_nomination=False,
                status_action_taken="BNSS Sec 190 Complaint Filed (JMFC-3)",
            ),
            RecidivistEntityRecord(
                entity_name="South Coast Cement Packaging Works",
                cin_or_gstin="U26940KA2015PTC071234 / 29AAACS4455K1Z1",
                registered_district="Bengaluru Rural",
                prior_violations_count=2,
                most_recent_offence_date=datetime.date(2026, 1, 25),
                statutory_sections_violated=["Section 36(2) - Short Weight 1.2kg"],
                has_valid_form_i_nomination=True,
                status_action_taken="Summons Issued under Sec 64 BNSS",
            ),
        ]

        return DistrictEnforcementPayload(
            report_reference_id="REP-INTEL-2026-Q1-BLR",
            reporting_period_start=datetime.date(2026, 1, 1),
            reporting_period_end=datetime.date(2026, 3, 31),
            district_name="Bengaluru Urban",
            state_name="Karnataka",
            controller_division="Southern Metrological Zone",
            reporting_officer_name="Shri A. N. Murthy",
            reporting_officer_designation="Joint Controller of Legal Metrology",
            total_inspections=255,
            compliant_inspections=203,
            non_compliant_inspections=52,
            statutory_notices_issued=52,
            compounding_cases_concluded=39,
            total_compounding_revenue_inr=805000.0,
            court_prosecutions_filed=13,
            seizures_executed_count=8,
            sector_metrics=sectors,
            recidivist_entities=recidivists,
            executive_recommendations=[
                "Intensify raid operations at automated quick-commerce dark stores across South Bengaluru.",
                "Serve show-cause notices to 8 corporate entities lacking Form I nominations.",
                "Expedite prosecution trial hearings in JMFC Court No. 2 for repeat cement short-weighters.",
            ],
        )

    def test_compile_district_report_pdf(self, sample_district_payload):
        compiler = DistrictEnforcementReportCompiler()
        pdf_bytes = compiler.compile_district_report_pdf(sample_district_payload)

        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 3000
        assert pdf_bytes.startswith(b"%PDF-")
