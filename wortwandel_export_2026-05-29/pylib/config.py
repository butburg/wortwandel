"""Shared configuration values for notebooks.

phinx: Sphinx documentation tool.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_INPUT_DIR = PROJECT_ROOT / "data_input"
DATA_OUTPUT_DIR = PROJECT_ROOT / "data_output"
PLOTS_DIR = DATA_OUTPUT_DIR / "plots"

DWH_DB_PATH = DATA_OUTPUT_DIR / "dwh_data.db"
DWH_FAULTY_DB_PATH = DATA_OUTPUT_DIR / "dwh_data_faulty.db"

SCRAPER_CUTOFF = pd.Timestamp("2022-04-21")
DEFAULT_START_DATE = SCRAPER_CUTOFF

DEFAULT_END_DATE = pd.Timestamp("2025-01-31")
QUALITY_END_DATE = pd.Timestamp("2025-02-08")

ANOMALY_START = pd.Timestamp("2025-01-01")
ANOMALY_END = pd.Timestamp("2025-02-01")
