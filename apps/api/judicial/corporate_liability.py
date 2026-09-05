"""
Corporate Liability & Form I Director Nomination Engine (Section 49)
===================================================================
Enforces vicarious corporate liability, officer-in-default attribution,
and Form I Director Nomination tracking under Section 49 of the Legal Metrology
Act, 2009 and Rule 29 of the Legal Metrology (Packaged Commodities) Rules, 2011.

Statutory Foundation & Supreme Court Jurisprudence:
---------------------------------------------------
1. Section 49(1) of LM Act, 2009:
   Where an offence is committed by a company, the company and every person in charge
   of and responsible to the company for the conduct of business is deemed guilty.

2. Section 49(2) & Rule 29 (Form I Nomination):
   A company may nominate a specific whole-time Director or Manager by giving notice
   in Form I to the Controller of Legal Metrology. When a valid nomination is in force:
   - Criminal prosecution lies EXCLUSIVELY against the Nominated Director and the Company.
   - Non-executive Directors, Independent Directors, and the Managing Director / Chairman
     are shielded from vicarious criminal liability.

3. Landmark Precedents:
   - *Dayle De\'Souza v. Union of India (2021) 14 SCC 566*: Arraigning other Directors
     when a Form I nomination exists is an abuse of legal process.
   - *Aneeta Hada v. Godfather Travels (2012) 5 SCC 661*: Company is the principal offender;
     prosecution of directors without arraigning the corporate body is fatal to the case.
   - Section 149(12) Companies Act, 2013: Independent and non-executive directors are
     liable only for acts occurring with their knowledge, attributable through board processes.
"""

from __future__ import annotations

import datetime
import enum
import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("metrolens.judicial.corporate_liability")


class NominationStatus(str, enum.Enum):
    """Statutory lifecycle state of Form I Director Nomination."""
    ACTIVE_VALID = "active_valid"
    PENDING_ACKNOWLEDGEMENT = "pending_controller_acknowledgement"
    EXPIRED = "expired"
    REVOKED_BY_COMPANY = "revoked_by_company"
    REJECTED_BY_CONTROLLER = "rejected_by_controller"
    NOT_FILED = "not_filed"


class DirectorType(str, enum.Enum):
    """Categorization of corporate officers under the Companies Act, 2013."""
    MANAGING_DIRECTOR = "managing_director"
    WHOLE_TIME_DIRECTOR = "whole_time_director"
    NOMINATED_DIRECTOR_FORM_I = "nominated_director_form_i"
    INDEPENDENT_DIRECTOR = "independent_director"
    NOMINEE_DIRECTOR = "nominee_director"
    CHIEF_EXECUTIVE_OFFICER = "chief_executive_officer"
    PLANT_MANAGER = "plant_manager"


@dataclass
class FormINomination:
    """
    Statutory Notice of Nomination under Section 49(2) and Rule 29.
    
    Attributes:
        nomination_id: Unique tracking reference.
        nominated_director_din: 8-digit Director Identification Number.
        nominated_director_name: Full legal name.
        residential_address: Official address of the nominated officer.
        jurisdiction_scope: "PAN_INDIA" or specific manufacturing establishment / plant.
        board_resolution_date: Date on which Board of Directors authorized nomination.
        filing_date_with_controller: Date Form I was submitted.
        acknowledgement_number: Controller's official receipt reference.
        status: Nomination validity status.
        effective_from: Start date of legal immunity for other directors.
        effective_until: Expiration or revocation date (None if ongoing).
    """
    nomination_id: str
    nominated_director_din: str
    nominated_director_name: str
    residential_address: str
    jurisdiction_scope: str = "PAN_INDIA"
    board_resolution_date: datetime.date = field(default_factory=datetime.date.today)
    filing_date_with_controller: datetime.date = field(default_factory=datetime.date.today)
    acknowledgement_number: Optional[str] = None
    status: NominationStatus = NominationStatus.ACTIVE_VALID
    effective_from: datetime.date = field(default_factory=datetime.date.today)
    effective_until: Optional[datetime.date] = None

    def is_active_on(self, target_date: datetime.date, location: str = "") -> bool:
        """Determines whether this Form I nomination was legally valid on the date and at locus."""
        if self.status != NominationStatus.ACTIVE_VALID:
            return False
        if target_date < self.effective_from:
            return False
        if self.effective_until and target_date > self.effective_until:
            return False
        if self.jurisdiction_scope != "PAN_INDIA" and location:
            if self.jurisdiction_scope.lower() not in location.lower():
                return False
        return True


@dataclass
class DirectorRecord:
    """Individual director or managerial officer entry in MCA corporate register."""
    din: str
    full_name: str
    director_type: DirectorType
    appointment_date: datetime.date
    cessation_date: Optional[datetime.date] = None
    is_resident_in_india: bool = True
    residential_address: str = ""


@dataclass
class CorporateEntity:
    """Corporate manufacturer, packer, or importer legal profile."""
    cin: str  # Corporate Identification Number: e.g. U74999KA2018PTC115000
    company_name: str
    registered_office_address: str
    pan_number: str
    gstin: str
    directors: List[DirectorRecord] = field(default_factory=list)
    form_i_nominations: List[FormINomination] = field(default_factory=list)
    manufacturing_plants: List[str] = field(default_factory=list)

    def validate_cin(self) -> bool:
        """Validates standard 21-character MCA CIN regex format."""
        cin_regex = re.compile(r"^[LU][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$")
        return bool(cin_regex.match(self.cin.strip().upper()))

    def get_managing_directors(self) -> List[DirectorRecord]:
        return [
            d for d in self.directors
            if d.director_type in (DirectorType.MANAGING_DIRECTOR, DirectorType.CHIEF_EXECUTIVE_OFFICER)
            and (d.cessation_date is None or d.cessation_date >= datetime.date.today())
        ]


@dataclass
class LiabilityAttributionResult:
    """Legal evaluation determining who must be arraigned as accused."""
    corporate_entity_cin: str
    company_name: str
    has_valid_form_i_nomination: bool
    nominated_director: Optional[FormINomination]
    parties_to_arraign: List[Dict[str, str]]
    parties_protected_from_prosecution: List[Dict[str, str]]
    statutory_averment_text: str
    legal_precedents_cited: List[str] = field(default_factory=list)


class CorporateLiabilityEvaluator:
    """
    Evaluates corporate vicarious liability and formats statutory prosecution
    averments for Legal Metrology complaint petitions.
    """

    def evaluate_liability(
        self,
        entity: CorporateEntity,
        offence_date: datetime.date,
        manufacturing_unit_location: str = "",
    ) -> LiabilityAttributionResult:
        """
        Determines the exact roster of accused parties to be named in the BNSS complaint.
        """
        # 1. Search for active Form I nomination covering the offence date & location
        active_nomination: Optional[FormINomination] = None
        for nom in entity.form_i_nominations:
            if nom.is_active_on(offence_date, manufacturing_unit_location):
                active_nomination = nom
                break

        arraign_list: List[Dict[str, str]] = []
        protect_list: List[Dict[str, str]] = []

        # Always arraign the corporate entity as Accused No. 1 (per Aneeta Hada mandate)
        arraign_list.append({
            "role": "Accused No. 1 (Corporate Entity)",
            "name": entity.company_name,
            "identification": entity.cin,
            "legal_basis": "Principal corporate entity under Section 49(1) of Legal Metrology Act, 2009",
        })

        if active_nomination:
            # Shielding in effect: Prosecute Nominated Director ONLY
            arraign_list.append({
                "role": "Accused No. 2 (Nominated Director under Section 49(2))",
                "name": active_nomination.nominated_director_name,
                "identification": f"DIN: {active_nomination.nominated_director_din}",
                "legal_basis": (
                    f"Authorized officer nominated under Section 49(2) and Rule 29 Form I "
                    f"(Ack No: {active_nomination.acknowledgement_number or 'Filed'})."
                ),
            })

            # All other directors are protected
            for d in entity.directors:
                if d.din != active_nomination.nominated_director_din:
                    protect_list.append({
                        "name": d.full_name,
                        "din": d.din,
                        "designation": d.director_type.value,
                        "immunity_ground": (
                            "Statutory immunity under Section 49(2) proviso and Dayle De'Souza v. UOI (2021) "
                            "due to active Form I nomination."
                        ),
                    })

            averment = (
                f"That the Accused No. 1 is a body corporate and Accused No. 2 has been duly nominated "
                f"by the Accused No. 1 Company under Section 49(2) of the Legal Metrology Act, 2009 read with "
                f"Rule 29 of the Legal Metrology (Packaged Commodities) Rules, 2011 to exercise all powers "
                f"and take all necessary steps to prevent the commission of offences under the said Act. "
                f"Accordingly, in terms of the proviso to Section 49(2) and the law declared by the Hon'ble "
                f"Supreme Court of India in Dayle De'Souza v. Union of India (2021), Accused No. 1 and Accused No. 2 "
                f"alone are vicariously and criminally liable for the contravention of Section 18 / 36."
            )
        else:
            # No valid Form I nomination: Managing Director & Executive Directors are arraigned
            md_list = entity.get_managing_directors()
            if md_list:
                for idx, md in enumerate(md_list, start=2):
                    arraign_list.append({
                        "role": f"Accused No. {idx} ({md.director_type.value.replace('_', ' ').title()})",
                        "name": md.full_name,
                        "identification": f"DIN: {md.din}",
                        "legal_basis": (
                            "Officer in default in charge of and responsible to the company for the conduct of its "
                            "business under Section 49(1) of the Legal Metrology Act, 2009."
                        ),
                    })
            else:
                # Arraign all whole-time directors
                for idx, d in enumerate([dir for dir in entity.directors if dir.director_type == DirectorType.WHOLE_TIME_DIRECTOR], start=2):
                    arraign_list.append({
                        "role": f"Accused No. {idx} (Whole-Time Director)",
                        "name": d.full_name,
                        "identification": f"DIN: {d.din}",
                        "legal_basis": "Executive director in charge of business under Section 49(1).",
                    })

            # Independent and Nominee directors are protected under Section 149(12) Companies Act
            for d in entity.directors:
                if d.director_type in (DirectorType.INDEPENDENT_DIRECTOR, DirectorType.NOMINEE_DIRECTOR):
                    protect_list.append({
                        "name": d.full_name,
                        "din": d.din,
                        "designation": d.director_type.value,
                        "immunity_ground": "Non-executive status protected under Section 149(12) of Companies Act, 2013.",
                    })

            averment = (
                f"That the Accused No. 1 Company has failed to nominate any Director under Section 49(2) "
                f"of the Legal Metrology Act, 2009 read with Rule 29 of the Legal Metrology (Packaged Commodities) "
                f"Rules, 2011, and no valid Form I nomination was registered with the Controller of Legal Metrology. "
                f"Therefore, in terms of Section 49(1) and the proviso to Section 49(2), every person who was in charge "
                f"of and responsible to the company for the conduct of its business at the time of commission of the "
                f"offence is vicariously liable. The named executive directors were actively running day-to-day operations "
                f"and are arraigned as co-accused."
            )

        return LiabilityAttributionResult(
            corporate_entity_cin=entity.cin,
            company_name=entity.company_name,
            has_valid_form_i_nomination=(active_nomination is not None),
            nominated_director=active_nomination,
            parties_to_arraign=arraign_list,
            parties_protected_from_prosecution=protect_list,
            statutory_averment_text=averment,
            legal_precedents_cited=[
                "Aneeta Hada v. Godfather Travels & Tours Pvt. Ltd. (2012) 5 SCC 661",
                "Dayle De'Souza v. Union of India (2021) 14 SCC 566",
                "Standard Chartered Bank v. Directorate of Enforcement (2005) 4 SCC 530",
            ],
        )
