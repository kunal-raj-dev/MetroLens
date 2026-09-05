"""
Basic unit test ensuring rule schema, verification scripts, and repository integrity pass.
"""

import subprocess
import sys
from pathlib import Path

def test_verify_legal_sources():
    result = subprocess.run([sys.executable, "scripts/verification/verify_legal_sources.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_legal_sources failed:\n{result.stdout}\n{result.stderr}"

def test_verify_rule_registry():
    result = subprocess.run([sys.executable, "scripts/verification/verify_rule_registry.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_rule_registry failed:\n{result.stdout}\n{result.stderr}"

def test_verify_claims():
    result = subprocess.run([sys.executable, "scripts/verification/verify_claims.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_claims failed:\n{result.stdout}\n{result.stderr}"

def test_verify_dataset_manifest():
    result = subprocess.run([sys.executable, "scripts/verification/verify_dataset_manifest.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_dataset_manifest failed:\n{result.stdout}\n{result.stderr}"

def test_verify_repository_integrity():
    result = subprocess.run([sys.executable, "scripts/verification/verify_repository_integrity.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_repository_integrity failed:\n{result.stdout}\n{result.stderr}"
