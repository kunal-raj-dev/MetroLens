"""
Unit Test Suite for Judicial Case Management, Compounding & Corporate Liability
================================================================================
Tests BNSS complaint dockets, cryptographic docket seals, Section 48 compounding ledger,
3-year recidivism bars, Cyber Treasury reconciliation, and Section 49 Form I corporate liability.
"""

import datetime
import pytest

from apps.api.judicial.case_docket import (
    DocketBuilder,
    LegalMetrologyOffence,
    PartyRole,
    ProsecutionDocket,
)
from apps.api.judicial.compounding_ledger import (
    CompoundingLedger,
    CompoundingRecord,
    CompoundingStatus,
    EligibilityAssessment,
    OffenceRecidivismLevel,
    TreasuryChallanReceipt,
)
from apps.api.judicial.corporate_liability import (
    CorporateEntity,
    CorporateLiabilityEvaluator,
    DirectorRecord,
    DirectorType,
    FormINomination,
    LiabilityAttributionResult,
    NominationStatus,
)


# =============================================================================
# 1. Judicial Prosecution Docket & Sealing Tests
# =============================================================================

class TestJudicialDocket:
    """Test suite for BNSS Section 190 complaint dockets and SHA-256 integrity."""

    @pytest.fixture
    def basic_docket(self):
        builder = DocketBuilder(
            docket_id="DOCKET-2026-KA-001",
            district="Bengaluru Urban",
            state="Karnataka",
        )
        builder.set_investigating_officer(
            name="Shri R. V. Kulkarni",
            designation="Senior Inspector of Legal Metrology",
            gazette_no="GAZ-BLR-2022-901",
        )
        builder.add_accused_corporate(
            party_id="ACCUSED-CORP-1",
            company_name="M/s Apex Packaged Foods Pvt Ltd",
            cin="U15400KA2015PTC081234",
            pan="AAACA1234F",
            gstin="29AAACA1234F1Z5",
            registered_office="Plot 42, Peenya Industrial Area, Bengaluru - 560058",
            charges=[
                LegalMetrologyOffence.SEC_18_NON_STANDARD_PACKAGE,
                LegalMetrologyOffence.RULE_6_MANDATORY_DECLARATION_OMISSION,
            ],
            prior_convictions=0,
        )
        builder.add_accused_individual(
            party_id="ACCUSED-IND-1",
            role=PartyRole.ACCUSED_NOMINATED_DIRECTOR,
            full_name="Shri S. R. Deshmukh",
            designation="Whole-Time Director (Quality & Compliance)",
            din="08451234",
            residential_address="Flat 4B, Richmond Towers, Bengaluru",
            charges=[LegalMetrologyOffence.SEC_36_1_PACKAGING_CONTRAVENTION],
        )
        builder.set_facts_and_chronology(
            synopsis="During a surprise inspection on 12-Feb-2026, packages were found without Unit Sale Price.",
            events=[
                ("2026-02-12T11:30:00", "Locus Search Initiated", "Search conducted at retail premises"),
                ("2026-02-12T13:00:00", "Samples Seized", "10 units seized under Rule 29"),
            ],
        )
        builder.add_panchnama_witness(
            witness_no=1,
            name="Mahesh Kumar",
            age=38,
            father_or_spouse="Ram Kumar",
            address="12, 4th Cross, Malleshwaram, Bengaluru",
            phone="9876543210",
            id_type="Aadhaar",
            id_masked="XXXX-XXXX-1234",
            statement="I witnessed the inspection and seizure of 10 biscuit packets.",
        )
        builder.add_seized_exhibit(
            exhibit_id="Ex-P1",
            commodity="Digestive Biscuits",
            brand="Apex Gold",
            batch="APX-2026-02",
            declared_qty="200 g",
            measured_qty="182 g",  # Short measure
            mrp=45.0,
            mfg_date="2026-01-15",
            origin="India",
            seal_tag="SEAL-KA-77890",
            custody_loc="Malkhana South",
            photo_hashes=["A" * 64],
        )
        return builder.build_and_seal()

    def test_docket_creation_and_fields(self, basic_docket):
        assert isinstance(basic_docket, ProsecutionDocket)
        assert basic_docket.metadata.docket_id == "DOCKET-2026-KA-001"
        assert len(basic_docket.accused_parties) == 2
        assert len(basic_docket.panchnama_witnesses) == 1
        assert len(basic_docket.seized_exhibits) == 1
        assert basic_docket.docket_sha256_seal is not None
        assert len(basic_docket.docket_sha256_seal) == 64

    def test_docket_cryptographic_seal_integrity(self, basic_docket):
        # Verification passes on untouched docket
        assert basic_docket.verify_integrity() is True

        # Mutating any field breaks cryptographic seal verification
        original_synopsis = basic_docket.factual_synopsis
        basic_docket.factual_synopsis = "TAMPERED: Facts modified post sealing."
        assert basic_docket.verify_integrity() is False

        # Restoring original data restores validity
        basic_docket.factual_synopsis = original_synopsis
        assert basic_docket.verify_integrity() is True


# =============================================================================
# 2. Section 48 Compounding Ledger & 3-Year Recidivism Tests
# =============================================================================

class TestCompoundingLedger:
    """Test suite for Section 48 compounding, 3-year bar, and Cyber Treasury reconciliation."""

    @pytest.fixture
    def ledger(self):
        return CompoundingLedger()

    def test_first_offence_eligibility_and_lifecycle(self, ledger):
        # 1. Eligibility evaluation for first-time offender
        eligibility = ledger.assess_eligibility(
            gstin="29AAACA1234F1Z5",
            pan="AAACA1234F",
            statutory_section="Rule 6",
            date_of_commission=datetime.date(2026, 3, 1),
        )

        assert isinstance(eligibility, EligibilityAssessment)
        assert eligibility.is_compoundable is True
        assert eligibility.recidivism_level == OffenceRecidivismLevel.FIRST_OFFENCE
        assert eligibility.suggested_compounding_fee_inr == 10000.0

        # 2. Issue compounding notice
        record = ledger.create_compounding_notice(
            case_number="CMP-2026-001",
            inspection_id="INSP-991",
            offender_name="Apex Packaged Foods Pvt Ltd",
            gstin="29AAACA1234F1Z5",
            pan_number="AAACA1234F",
            offence_type="Omission of Mandatory Declarations",
            statutory_section="Rule 6",
            date_of_commission=datetime.date(2026, 3, 1),
        )

        assert record.status == CompoundingStatus.NOTICE_ISSUED
        assert record.compounding_fee_inr == 10000.0

        # 3. Pay via Cyber Treasury e-Challan
        challan = TreasuryChallanReceipt(
            challan_number="KA-TR-2026-998811",
            bank_reference_utr="HDFCN0099887711",
            amount_inr=10000.0,
            remitter_name="Apex Packaged Foods Pvt Ltd",
            cyber_treasury_auth_code="AUTH-CT-44321",
        )
        updated = ledger.record_treasury_challan("CMP-2026-001", challan)
        assert updated.status == CompoundingStatus.PAYMENT_VERIFIED
        assert updated.treasury_challan is not None

        # 4. Issue Section 48(3) Discharge Order
        discharged = ledger.issue_discharge_order("CMP-2026-001", authorized_officer="Controller of LM")
        assert discharged.status == CompoundingStatus.DISCHARGE_ORDER_ISSUED
        assert discharged.discharge_order_number is not None
        assert "DISCHARGE-SEC48" in discharged.discharge_order_number

    def test_strict_3_year_recidivism_bar(self, ledger):
        # First offence compounded in Jan 2025
        rec1 = ledger.create_compounding_notice(
            case_number="CMP-2025-010",
            inspection_id="INSP-100",
            offender_name="Global Cement Works Ltd",
            gstin="27AABCG7788P1Z1",
            pan_number="AABCG7788P",
            offence_type="Non-standard package size",
            statutory_section="Section 36(1)",
            date_of_commission=datetime.date(2025, 1, 10),
        )
        challan = TreasuryChallanReceipt(
            challan_number="MH-TR-2025-001",
            bank_reference_utr="SBIN00112233",
            amount_inr=25000.0,
        )
        ledger.record_treasury_challan("CMP-2025-010", challan)
        rec1_discharged = ledger.issue_discharge_order("CMP-2025-010")
        rec1_discharged.discharge_date = datetime.date(2025, 1, 20)

        # Second offence committed within 14 months (March 2026) -> Within 3-year lookback
        assessment = ledger.assess_eligibility(
            gstin="27AABCG7788P1Z1",
            pan="AABCG7788P",
            statutory_section="Section 36(1)",
            date_of_commission=datetime.date(2026, 3, 15),
        )

        assert assessment.is_compoundable is False
        assert assessment.recidivism_level == OffenceRecidivismLevel.REPEAT_WITHIN_3_YEARS
        assert "STRICTLY NON-COMPOUNDABLE" in assessment.statutory_reasoning
        assert len(assessment.prior_compounded_cases) == 1

        # Attempting to issue compounding notice auto-rejects
        rec2 = ledger.create_compounding_notice(
            case_number="CMP-2026-088",
            inspection_id="INSP-888",
            offender_name="Global Cement Works Ltd",
            gstin="27AABCG7788P1Z1",
            pan_number="AABCG7788P",
            offence_type="Non-standard package size",
            statutory_section="Section 36(1)",
            date_of_commission=datetime.date(2026, 3, 15),
        )
        assert rec2.status == CompoundingStatus.REJECTED_RECIDIVIST


# =============================================================================
# 3. Section 49 Corporate Liability & Form I Nomination Tests
# =============================================================================

class TestCorporateLiability:
    """Test suite for Form I Director Nomination under Section 49 and Rule 29."""

    @pytest.fixture
    def evaluator(self):
        return CorporateLiabilityEvaluator()

    @pytest.fixture
    def corporate_entity_with_nomination(self):
        nomination = FormINomination(
            nomination_id="FORM-I-2024-001",
            nominated_director_din="07112233",
            nominated_director_name="Shri Anil V. Mehta",
            residential_address="14, Marine Drive, Mumbai",
            jurisdiction_scope="PAN_INDIA",
            board_resolution_date=datetime.date(2024, 1, 10),
            filing_date_with_controller=datetime.date(2024, 1, 15),
            acknowledgement_number="CLM/NOM/2024/4412",
            status=NominationStatus.ACTIVE_VALID,
            effective_from=datetime.date(2024, 1, 15),
            effective_until=None,
        )

        return CorporateEntity(
            cin="U24230MH2010PTC201234",
            company_name="Sun Pharma Retail Consumer Care Pvt Ltd",
            registered_office_address="Sun House, CTS No. 201, Goregaon (E), Mumbai",
            pan_number="AAACS9988K",
            gstin="27AAACS9988K1ZV",
            directors=[
                DirectorRecord(
                    din="00012345",
                    full_name="Shri Dilip Shanghvi",
                    director_type=DirectorType.MANAGING_DIRECTOR,
                    appointment_date=datetime.date(2010, 1, 1),
                ),
                DirectorRecord(
                    din="07112233",
                    full_name="Shri Anil V. Mehta",
                    director_type=DirectorType.NOMINATED_DIRECTOR_FORM_I,
                    appointment_date=datetime.date(2020, 5, 1),
                ),
                DirectorRecord(
                    din="09988776",
                    full_name="Dr. K. S. Rao",
                    director_type=DirectorType.INDEPENDENT_DIRECTOR,
                    appointment_date=datetime.date(2021, 8, 1),
                ),
            ],
            form_i_nominations=[nomination],
        )

    def test_valid_form_i_shields_managing_director(self, evaluator, corporate_entity_with_nomination):
        res = evaluator.evaluate_liability(
            corporate_entity_with_nomination,
            offence_date=datetime.date(2026, 2, 20),
            manufacturing_unit_location="Baddi Plant, Himachal Pradesh",
        )

        assert isinstance(res, LiabilityAttributionResult)
        assert res.has_valid_form_i_nomination is True
        assert res.nominated_director is not None

        # Accused should contain ONLY Company and Nominated Director
        arraigned_names = [p["name"] for p in res.parties_to_arraign]
        assert "Sun Pharma Retail Consumer Care Pvt Ltd" in arraigned_names
        assert "Shri Anil V. Mehta" in arraigned_names
        assert "Shri Dilip Shanghvi" not in arraigned_names  # MD is protected!

        # Managing director and Independent director must be in protected list
        protected_names = [p["name"] for p in res.parties_protected_from_prosecution]
        assert "Shri Dilip Shanghvi" in protected_names
        assert "Dr. K. S. Rao" in protected_names

    def test_absent_form_i_arraigns_managing_director(self, evaluator, corporate_entity_with_nomination):
        # Remove Form I nomination
        corporate_entity_with_nomination.form_i_nominations.clear()

        res = evaluator.evaluate_liability(
            corporate_entity_with_nomination,
            offence_date=datetime.date(2026, 2, 20),
        )

        assert res.has_valid_form_i_nomination is False
        assert res.nominated_director is None

        # Managing Director must now be arraigned as co-accused under Section 49(1)
        arraigned_names = [p["name"] for p in res.parties_to_arraign]
        assert "Sun Pharma Retail Consumer Care Pvt Ltd" in arraigned_names
        assert "Shri Dilip Shanghvi" in arraigned_names  # MD is now held personally liable!
