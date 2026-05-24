"""Shared analysis helpers for notebook refactors.

phinx: Sphinx documentation tool.
"""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd


def map_term_category(term: str, mapping: Dict[str, str]) -> Optional[str]:
    """Map a term to a category using a mapping dict.

    :param term: Term to map.
    :type term: str
    :param mapping: Term to category mapping.
    :type mapping: dict[str, str]
    :returns: Category name or None.
    :rtype: str | None
    """
    if term is None:
        return None
    return mapping.get(term)


def map_suffix_to_term(suffix: str, mapping: Dict[str, str]) -> Optional[str]:
    """Map an exact suffix to a term using a mapping dict.

    :param suffix: Suffix value.
    :type suffix: str
    :param mapping: Suffix-to-term mapping.
    :type mapping: dict[str, str]
    :returns: Term name or None.
    :rtype: str | None
    """
    if pd.isna(suffix):
        return None
    value = str(suffix).lower().strip()
    return mapping.get(value)


def map_suffix_by_prefix(suffix: str, mapping: Dict[str, str]) -> Optional[str]:
    """Map a suffix to a term using prefix matching.

    :param suffix: Suffix value.
    :type suffix: str
    :param mapping: Prefix-to-term mapping.
    :type mapping: dict[str, str]
    :returns: Term name or None.
    :rtype: str | None
    """
    if pd.isna(suffix):
        return None
    value = str(suffix).lower().strip()
    for prefix, term in mapping.items():
        if value.startswith(prefix):
            return term
    return None


def normalize_suffix_row(
    row: pd.Series,
    lemma_col: str = "suffix_lemma",
    suffix_col: str = "suffix",
) -> pd.NA | str:
    """Normalize suffix values with a lemma-first preference.

    :param row: DataFrame row containing suffix values.
    :type row: pandas.Series
    :param lemma_col: Column name for lemma values.
    :type lemma_col: str
    :param suffix_col: Column name for raw suffix values.
    :type suffix_col: str
    :returns: Normalized suffix or pandas.NA.
    :rtype: str | pandas.NA
    """
    lemma_value = row.get(lemma_col, None)
    suffix_value = row.get(suffix_col, None)

    if pd.notna(lemma_value):
        text = str(lemma_value).strip().lower()
        if text:
            return text

    if pd.notna(suffix_value):
        text = str(suffix_value).strip().lower()
        if text:
            return text

    return pd.NA
