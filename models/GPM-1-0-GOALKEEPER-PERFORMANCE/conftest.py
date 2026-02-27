"""Pytest configuration for GPM model tests."""

import sys
from pathlib import Path

# Add the model directory to sys.path so gpm_model can be imported directly
sys.path.insert(0, str(Path(__file__).parent))
