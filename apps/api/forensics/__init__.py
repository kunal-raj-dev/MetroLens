"""
MetroLens AI - Media Forensics & Steganography Defense Package
==============================================================
Provides digital image forensic analysis, error level analysis (ELA),
steganography and polyglot payload scanning, ICC color profile sanitization,
and perceptual hashing algorithms for packaged commodity inspections.
"""

from .ela import ErrorLevelAnalyzer, ELAResult
from .steganography import (
    SteganographyScanner,
    SteganographyScanResult,
    ChunkSanitizationResult,
)
from .icc_sanitizer import ICCProfileSanitizer, ICCSanitizationResult
from .perceptual_hash import PerceptualHasher, PerceptualHashResult
from .copy_move import CopyMoveDetector, CopyMoveDetectionResult
from .cfa_artifacts import CFADemosaicAnalyzer, CFADemosaicingResult, BayerPatternType
from .double_compression import DoubleCompressionDetector, DoubleCompressionResult
from .sensor_prnu import PRNUSensorFingerprintVerifier, PRNUCrossCorrelationResult

__all__ = [
    "ErrorLevelAnalyzer",
    "ELAResult",
    "SteganographyScanner",
    "SteganographyScanResult",
    "ChunkSanitizationResult",
    "ICCProfileSanitizer",
    "ICCSanitizationResult",
    "PerceptualHasher",
    "PerceptualHashResult",
    "CopyMoveDetector",
    "CopyMoveDetectionResult",
    "CFADemosaicAnalyzer",
    "CFADemosaicingResult",
    "BayerPatternType",
    "DoubleCompressionDetector",
    "DoubleCompressionResult",
    "PRNUSensorFingerprintVerifier",
    "PRNUCrossCorrelationResult",
]

