"""
Judicial Complaint Docket & BNSS Prosecution Packaging Subsystem
================================================================
Generates court-ready complaint dockets for filing before the Court of the
Judicial Magistrate First Class (JMFC) or Metropolitan Magistrate under Section 190(1)(a)
of the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) / CrPC, 1973.

Statutory Framework:
--------------------
- Legal Metrology Act, 2009 (Act No. 1 of 2010):
    * Section 18: Prohibition on manufacture, packing, sale of non-standard packaged commodities.
    * Section 36(1): Penalty for selling non-standard packaged commodities (up to Rs 25,000 / 50,000 / 1,00,000 or 1 year imprisonment).
    * Section 36(2): Penalty for short weight or measure (imprisonment up to 5 years).
    * Section 48 / 48A: Compounding of offences and repeat offenders.
    * Section 49: Offences by companies and nominated directors under Rule 29.
- Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS):
    * Section 190(1)(a): Cognizance of offences by Magistrates upon receiving a complaint of facts.
    * Section 223: Examination of complainant and witnesses in private complaints.
    * Section 64 / 227: Issue of process / summons against accused.
    * Section 94: Summons to produce document or other thing.
- Bharatiya Sakshya Adhiniyam, 2023 (BSA):
    * Section 63: Admissibility of electronic records and digital certificate of authenticity.

Key Components:
---------------
1. Complainant Inspector credentials, authorization gazette notification, and territorial jurisdiction.
2. Accused party roster (Entity, Managing Director, Nominated Director under Form I, Retailer, Wholesaler).
3. Chronological Statement of Facts & Narrative of Search, Inspection, and Sample Seizure.
4. Panchnama Inventory with independent witness testimony records.
5. Evidentiary Exhibit Schedule with digital forensics audit trail and BSA Section 63 certificate.
6. Formal Prayer to the Court with requested summons and penal sanctions.
7. Cryptographic Tamper-Evident SHA-256 sealing of the complete judicial docket.
"""

from __future__ import annotations

import datetime
import enum
import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("metrolens.judicial.case_docket")


class LegalMetrologyOffence(str, enum.Enum):
    """Categorization of offences under the Legal Metrology Act, 2009."""
    SEC_18_NON_STANDARD_PACKAGE = "Section 18: Sale/Distribution of Non-Standard Package"
    SEC_36_1_PACKAGING_CONTRAVENTION = "Section 36(1): Manufacture, Packing, or Sale in Violation of Rules"
    SEC_36_2_SHORT_WEIGHT_MEASURE = "Section 36(2): Short Weight or Measure Delivery"
    SEC_48_RECIDIVISM_VIOLATION = "Section 48(2): Repeat Offence within 3-Year Prohibition Window"
    SEC_49_CORPORATE_VICARIOUS_LIABILITY = "Section 49: Corporate Liability for In-Default Officers"
    RULE_6_MANDATORY_DECLARATION_OMISSION = "Rule 6(1): Complete Omission of Mandatory Statutory Declaration"
    RULE_6_MRP_INCLUSIVE_TAX_OMISSION = "Rule 6(1)(e): MRP not declared inclusive of all taxes"
    RULE_6_USP_OMISSION = "Rule 6(1)(e): Unit Sale Price (USP) Omitted or Miscalculated"
    RULE_7_FONT_SIZE_CONTRAVENTION = "Rule 7: Font Height, Width, or Stroke Thickness Below Statutory Threshold"
    RULE_18_OVERCHARGING_ABOVE_MRP = "Rule 18(2): Sale at price exceeding Maximum Retail Price"
    RULE_26_EXEMPTION_MISUSE = "Rule 26: Fraudulent claiming of institutional or small package exemption"
    RULE_32_DECEPTIVE_PACKAGING = "Rule 32: Deceptive package size, misleading headspace, or deceptive fill ratio"


class PartyRole(str, enum.Enum):
    """Accused and witness procedural designations in court proceedings."""
    COMPLAINANT = "Complainant (Inspector of Legal Metrology)"
    ACCUSED_COMPANY = "Accused No. 1 (Manufacturer / Packer Entity)"
    ACCUSED_MANAGING_DIRECTOR = "Accused No. 2 (Managing Director / CEO)"
    ACCUSED_NOMINATED_DIRECTOR = "Accused (Nominated Director under Section 49 / Form I)"
    ACCUSED_RETAILER = "Accused (Retail Establishment Owner / Proprietor)"
    ACCUSED_DISTRIBUTOR = "Accused (C&F Agent / Wholesale Distributor)"
    INDEPENDENT_WITNESS = "Panch Witness (Panchnama Attestation)"
    OFFICIAL_ANALYST = "Government Approved Test Center / Metrologist"


@dataclass
class PanchnamaWitness:
    """Independent panch witness who attested the inspection and seizure at locus."""
    witness_number: int  # 1 or 2
    full_name: str
    age_years: int
    father_or_spouse_name: str
    residential_address: str
    phone_number: str
    national_id_type: str  # "Aadhaar", "Voter ID", "Driving License"
    national_id_masked: str
    statement_summary: str
    attestation_timestamp: datetime.datetime


@dataclass
class SeizedExhibitItem:
    """Individual sample container seized during search under Rule 29."""
    exhibit_number: str  # e.g., "Exhibit P-1", "Exhibit P-2"
    commodity_name: str
    brand_name: str
    batch_or_lot_number: str
    declared_net_quantity: str
    actual_measured_quantity: Optional[str]
    declared_mrp_inr: float
    mfg_or_packing_date: str
    country_of_origin: str
    seal_tag_number: str
    custody_location: str  # e.g. "Malkhana, O/o Assistant Controller Legal Metrology, South Division"
    photograph_hashes: List[str] = field(default_factory=list)


@dataclass
class AccusedParty:
    """Formal identification of party being prosecuted."""
    party_id: str
    role: PartyRole
    entity_name_or_person: str
    designation: Optional[str]
    cin_or_din: Optional[str]
    pan_number: Optional[str]
    gstin: Optional[str]
    registered_address: str
    is_corporate_entity: bool
    statutory_sections_charged: List[LegalMetrologyOffence] = field(default_factory=list)
    prior_convictions_count: int = 0


@dataclass
class PrayerToCourt:
    """Statutory prayers addressed to the Judicial Magistrate First Class."""
    issue_summons: bool = True
    summon_production_of_records: bool = True
    records_to_produce: List[str] = field(default_factory=list)
    impose_maximum_statutory_penalty: bool = True
    request_forfeiture_of_seized_stock: bool = True
    request_publication_of_conviction: bool = False
    specific_penal_clauses: List[str] = field(default_factory=list)


@dataclass
class JudicialDocketMetadata:
    """Administrative and court registry identifiers."""
    docket_id: str
    jurisdiction_district: str
    jurisdiction_state: str
    competent_court_name: str  # e.g. "Court of Chief Judicial Magistrate, Bengaluru Urban"
    police_station_jurisdiction: str
    inspection_reference_id: str
    filing_date: datetime.date
    investigating_officer_name: str
    investigating_officer_designation: str
    gazette_notification_number: str
    case_tracking_qr_payload: str
    created_at_utc: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


@dataclass
class ProsecutionDocket:
    """
    Complete, self-contained Judicial Prosecution Complaint Docket ready for
    formal filing before a criminal court.
    """
    metadata: JudicialDocketMetadata
    complainant: AccusedParty
    accused_parties: List[AccusedParty]
    offences_charged: List[LegalMetrologyOffence]
    factual_synopsis: str
    chronological_events: List[Dict[str, str]]
    panchnama_witnesses: List[PanchnamaWitness]
    seized_exhibits: List[SeizedExhibitItem]
    evidence_inventory: List[Dict[str, Any]]
    bsa_section_63_certificate_id: str
    digital_forensic_evidence_hash: str
    prayer: PrayerToCourt
    docket_sha256_seal: Optional[str] = None

    def seal_docket(self) -> str:
        """Computes immutable cryptographic SHA-256 seal across all docket fields."""
        serialized = json.dumps(asdict(self), sort_keys=True, default=str)
        # Exclude existing seal if present
        cleaned = json.loads(serialized)
        cleaned["docket_sha256_seal"] = None
        re_encoded = json.dumps(cleaned, sort_keys=True)
        seal = hashlib.sha256(re_encoded.encode("utf-8")).hexdigest().upper()
        self.docket_sha256_seal = seal
        return seal

    def verify_integrity(self) -> bool:
        """Verifies whether the docket contents have been tampered with since sealing."""
        if not self.docket_sha256_seal:
            return False
        existing_seal = self.docket_sha256_seal
        calculated_seal = self.seal_docket()
        self.docket_sha256_seal = existing_seal
        return existing_seal == calculated_seal


class DocketBuilder:
    """
    Fluent builder for assembling statutory prosecution complaint dockets.
    """

    def __init__(self, docket_id: str, district: str, state: str):
        self.metadata = JudicialDocketMetadata(
            docket_id=docket_id,
            jurisdiction_district=district,
            jurisdiction_state=state,
            competent_court_name=f"Court of Chief Judicial Magistrate, {district}, {state}",
            police_station_jurisdiction="Central Commercial Division",
            inspection_reference_id=f"INSP-{docket_id}",
            filing_date=datetime.date.today(),
            investigating_officer_name="Shri K. R. Sharma",
            investigating_officer_designation="Senior Inspector of Legal Metrology",
            gazette_notification_number="No. LM/GAZ/2021/774",
            case_tracking_qr_payload=f"https://metrolens.nic.in/court/dockets/{docket_id}",
        )
        self.complainant = AccusedParty(
            party_id="COMPLAINANT-01",
            role=PartyRole.COMPLAINANT,
            entity_name_or_person="Inspector of Legal Metrology, Sub-Division A",
            designation="Authorized Officer under Section 13(1) of LM Act, 2009",
            cin_or_din=None,
            pan_number=None,
            gstin=None,
            registered_address="Department of Consumer Affairs, Legal Metrology Wing, Administrative Complex",
            is_corporate_entity=False,
        )
        self.accused_parties: List[AccusedParty] = []
        self.offences_charged: List[LegalMetrologyOffence] = []
        self.factual_synopsis: str = ""
        self.chronological_events: List[Dict[str, str]] = []
        self.panchnama_witnesses: List[PanchnamaWitness] = []
        self.seized_exhibits: List[SeizedExhibitItem] = []
        self.evidence_inventory: List[Dict[str, Any]] = []
        self.bsa_section_63_certificate_id: str = ""
        self.digital_forensic_evidence_hash: str = ""
        self.prayer = PrayerToCourt(
            issue_summons=True,
            summon_production_of_records=True,
            records_to_produce=[
                "Batch Manufacturing Records (BMR)",
                "Quality Assurance Check-Weigher Log",
                "Rule 29 Form I Nomination Register",
                "GST GSTR-1 Sales Invoices for Seized Batch",
            ],
            impose_maximum_statutory_penalty=True,
            request_forfeiture_of_seized_stock=True,
            request_publication_of_conviction=True,
            specific_penal_clauses=[
                "Conviction under Section 36(1) of Legal Metrology Act, 2009",
                "Punishment under Section 49(1) for Officers in Default",
            ],
        )

    def set_court_details(self, court_name: str, police_station: str) -> DocketBuilder:
        self.metadata.competent_court_name = court_name
        self.metadata.police_station_jurisdiction = police_station
        return self

    def set_investigating_officer(self, name: str, designation: str, gazette_no: str) -> DocketBuilder:
        self.metadata.investigating_officer_name = name
        self.metadata.investigating_officer_designation = designation
        self.metadata.gazette_notification_number = gazette_no
        self.complainant.entity_name_or_person = name
        self.complainant.designation = designation
        return self

    def add_accused_corporate(
        self,
        party_id: str,
        company_name: str,
        cin: str,
        pan: str,
        gstin: str,
        registered_office: str,
        charges: List[LegalMetrologyOffence],
        prior_convictions: int = 0,
    ) -> DocketBuilder:
        accused = AccusedParty(
            party_id=party_id,
            role=PartyRole.ACCUSED_COMPANY,
            entity_name_or_person=company_name,
            designation="Corporate Manufacturer / Packer",
            cin_or_din=cin,
            pan_number=pan,
            gstin=gstin,
            registered_address=registered_office,
            is_corporate_entity=True,
            statutory_sections_charged=charges,
            prior_convictions_count=prior_convictions,
        )
        self.accused_parties.append(accused)
        for c in charges:
            if c not in self.offences_charged:
                self.offences_charged.append(c)
        return self

    def add_accused_individual(
        self,
        party_id: str,
        role: PartyRole,
        full_name: str,
        designation: str,
        din: Optional[str],
        residential_address: str,
        charges: List[LegalMetrologyOffence],
        prior_convictions: int = 0,
    ) -> DocketBuilder:
        accused = AccusedParty(
            party_id=party_id,
            role=role,
            entity_name_or_person=full_name,
            designation=designation,
            cin_or_din=din,
            pan_number=None,
            gstin=None,
            registered_address=residential_address,
            is_corporate_entity=False,
            statutory_sections_charged=charges,
            prior_convictions_count=prior_convictions,
        )
        self.accused_parties.append(accused)
        for c in charges:
            if c not in self.offences_charged:
                self.offences_charged.append(c)
        return self

    def set_facts_and_chronology(
        self,
        synopsis: str,
        events: List[Tuple[str, str, str]],  # (timestamp_str, event_title, details)
    ) -> DocketBuilder:
        self.factual_synopsis = synopsis
        self.chronological_events = [
            {"timestamp": t, "title": title, "details": desc}
            for t, title, desc in events
        ]
        return self

    def add_panchnama_witness(
        self,
        witness_no: int,
        name: str,
        age: int,
        father_or_spouse: str,
        address: str,
        phone: str,
        id_type: str,
        id_masked: str,
        statement: str,
        timestamp: Optional[datetime.datetime] = None,
    ) -> DocketBuilder:
        w = PanchnamaWitness(
            witness_number=witness_no,
            full_name=name,
            age_years=age,
            father_or_spouse_name=father_or_spouse,
            residential_address=address,
            phone_number=phone,
            national_id_type=id_type,
            national_id_masked=id_masked,
            statement_summary=statement,
            attestation_timestamp=timestamp or datetime.datetime.now(),
        )
        self.panchnama_witnesses.append(w)
        return self

    def add_seized_exhibit(
        self,
        exhibit_id: str,
        commodity: str,
        brand: str,
        batch: str,
        declared_qty: str,
        measured_qty: Optional[str],
        mrp: float,
        mfg_date: str,
        origin: str,
        seal_tag: str,
        custody_loc: str,
        photo_hashes: List[str],
    ) -> DocketBuilder:
        exhibit = SeizedExhibitItem(
            exhibit_number=exhibit_id,
            commodity_name=commodity,
            brand_name=brand,
            batch_or_lot_number=batch,
            declared_net_quantity=declared_qty,
            actual_measured_quantity=measured_qty,
            declared_mrp_inr=mrp,
            mfg_or_packing_date=mfg_date,
            country_of_origin=origin,
            seal_tag_number=seal_tag,
            custody_location=custody_loc,
            photograph_hashes=photo_hashes,
        )
        self.seized_exhibits.append(exhibit)
        return self

    def set_forensics_and_bsa_certificates(
        self,
        bsa_cert_id: str,
        evidence_hash: str,
        inventory: List[Dict[str, Any]],
    ) -> DocketBuilder:
        self.bsa_section_63_certificate_id = bsa_cert_id
        self.digital_forensic_evidence_hash = evidence_hash
        self.evidence_inventory = inventory
        return self

    def build_and_seal(self) -> ProsecutionDocket:
        """Constructs docket and applies cryptographic seal."""
        docket = ProsecutionDocket(
            metadata=self.metadata,
            complainant=self.complainant,
            accused_parties=self.accused_parties,
            offences_charged=self.offences_charged,
            factual_synopsis=self.factual_synopsis,
            chronological_events=self.chronological_events,
            panchnama_witnesses=self.panchnama_witnesses,
            seized_exhibits=self.seized_exhibits,
            evidence_inventory=self.evidence_inventory,
            bsa_section_63_certificate_id=self.bsa_section_63_certificate_id,
            digital_forensic_evidence_hash=self.digital_forensic_evidence_hash,
            prayer=self.prayer,
        )
        docket.seal_docket()
        return docket
