"""
Legal Metrology Administrative Hierarchy & Jurisdiction Boundaries
===================================================================
Models the three-tier administrative jurisdiction structure of Indian Legal Metrology:
    Level 1: Central Directorate (Government of India) - Nationwide scope
    Level 2: State Controllerates (State Governments) - State-wide scope
    Level 3: District Inspectorates - Local district enforcement scope
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


class JurisdictionLevel(enum.IntEnum):
    """Hierarchical rank of legal metrology authority."""

    CENTRAL = 1  # Central Directorate of Legal Metrology (All-India)
    STATE = 2    # State Controller of Legal Metrology
    DISTRICT = 3 # Assistant Controller / Inspector of Legal Metrology


@dataclass(frozen=True)
class JurisdictionNode:
    """Represents an administrative node in the legal metrology hierarchy."""

    code: str
    name: str
    level: JurisdictionLevel
    state_name: str
    parent_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "level": self.level.name,
            "state_name": self.state_name,
            "parent_code": self.parent_code,
        }


class JurisdictionRegistry:
    """
    Authoritative registry and boundary validator for Indian Legal Metrology zones.
    """

    CENTRAL_CODE = "IN-CENTRAL"

    def __init__(self) -> None:
        self._nodes: Dict[str, JurisdictionNode] = {}
        self._initialize_canonical_jurisdictions()

    def register(self, node: JurisdictionNode) -> None:
        self._nodes[node.code] = node

    def get(self, code: str) -> Optional[JurisdictionNode]:
        return self._nodes.get(code)

    def is_authorized(self, officer_jurisdiction_code: str, target_jurisdiction_code: str) -> bool:
        """
        Determine whether an officer stationed at `officer_jurisdiction_code`
        has administrative authority over an inspection in `target_jurisdiction_code`.
        """
        # Central officers have nationwide authority
        if officer_jurisdiction_code == self.CENTRAL_CODE:
            return True

        if officer_jurisdiction_code == target_jurisdiction_code:
            return True

        officer_node = self._nodes.get(officer_jurisdiction_code)
        target_node = self._nodes.get(target_jurisdiction_code)

        if not officer_node or not target_node:
            # If unrecognized, fail-safe: allow only exact match
            return officer_jurisdiction_code == target_jurisdiction_code

        # State controller has authority over all districts in their state
        if officer_node.level == JurisdictionLevel.STATE:
            return officer_node.state_name.lower() == target_node.state_name.lower()

        # District inspectors cannot enforce outside their designated district
        if officer_node.level == JurisdictionLevel.DISTRICT:
            return officer_node.code == target_node.code

        return False

    def _initialize_canonical_jurisdictions(self) -> None:
        """Pre-populate canonical Indian administrative tree."""
        # Level 1: Central
        self.register(
            JurisdictionNode(
                code=self.CENTRAL_CODE,
                name="Central Directorate of Legal Metrology, New Delhi",
                level=JurisdictionLevel.CENTRAL,
                state_name="India",
                parent_code=None,
            )
        )

        # Level 2 & 3: Delhi
        self.register(
            JurisdictionNode(
                code="IN-DL",
                name="Controllerate of Legal Metrology, Delhi",
                level=JurisdictionLevel.STATE,
                state_name="Delhi",
                parent_code=self.CENTRAL_CODE,
            )
        )
        for d_code, d_name in [
            ("IN-DL-CENTRAL", "Central Delhi Inspectorate"),
            ("IN-DL-SOUTH", "South Delhi Inspectorate"),
            ("IN-DL-NORTH", "North Delhi Inspectorate"),
            ("IN-DL-WEST", "West Delhi Inspectorate"),
        ]:
            self.register(
                JurisdictionNode(
                    code=d_code,
                    name=d_name,
                    level=JurisdictionLevel.DISTRICT,
                    state_name="Delhi",
                    parent_code="IN-DL",
                )
            )

        # Level 2 & 3: Maharashtra
        self.register(
            JurisdictionNode(
                code="IN-MH",
                name="Controllerate of Legal Metrology, Maharashtra",
                level=JurisdictionLevel.STATE,
                state_name="Maharashtra",
                parent_code=self.CENTRAL_CODE,
            )
        )
        for d_code, d_name in [
            ("IN-MH-MUMBAI-CITY", "Mumbai City Inspectorate"),
            ("IN-MH-MUMBAI-SUB", "Mumbai Suburban Inspectorate"),
            ("IN-MH-PUNE", "Pune District Inspectorate"),
            ("IN-MH-NAGPUR", "Nagpur District Inspectorate"),
        ]:
            self.register(
                JurisdictionNode(
                    code=d_code,
                    name=d_name,
                    level=JurisdictionLevel.DISTRICT,
                    state_name="Maharashtra",
                    parent_code="IN-MH",
                )
            )

        # Level 2 & 3: Karnataka
        self.register(
            JurisdictionNode(
                code="IN-KA",
                name="Controllerate of Legal Metrology, Karnataka",
                level=JurisdictionLevel.STATE,
                state_name="Karnataka",
                parent_code=self.CENTRAL_CODE,
            )
        )
        self.register(
            JurisdictionNode(
                code="IN-KA-BLR-URBAN",
                name="Bengaluru Urban Inspectorate",
                level=JurisdictionLevel.DISTRICT,
                state_name="Karnataka",
                parent_code="IN-KA",
            )
        )
