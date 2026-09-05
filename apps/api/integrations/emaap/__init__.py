"""
National Legal Metrology Portal (eMaap) Integration Package
===========================================================
Provides client adapters, stateful mock servers, and case prosecution
lifecycle management conforming to Government of India Legal Metrology
e-Governance portal specifications (eMaap / e-Pramit).
"""

from .emaap_client import EMaapClient, EMaapClientConfig, EMaapResponse
from .emaap_mock_server import StatefulEMaapMockServer, EMaapCaseRecord
from .case_filing import (
    ProsecutionCaseManager,
    ProsecutionCaseDossier,
    CaseStage,
)

__all__ = [
    "EMaapClient",
    "EMaapClientConfig",
    "EMaapResponse",
    "StatefulEMaapMockServer",
    "EMaapCaseRecord",
    "ProsecutionCaseManager",
    "ProsecutionCaseDossier",
    "CaseStage",
]
