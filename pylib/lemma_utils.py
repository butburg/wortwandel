"""Lemma candidate utilities.

phinx: Sphinx documentation tool.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List

import pandas as pd


def _max_extra_len(base_len: int) -> int:
    """Return the allowed extra length for variants.

    :param base_len: Length of the base token.
    :type base_len: int
    :returns: Maximum allowed extra length.
    :rtype: int
    """
    if base_len <= 3:
        return 1
    if base_len == 4:
        return 2
    return max(1, math.ceil(base_len * 0.25))


def _allowed_small_suffix(extra: str, base_len: int) -> bool:
    """Check if a suffix extension is allowed for the base length.

    :param extra: Extra substring appended to the base token.
    :type extra: str
    :param base_len: Length of the base token.
    :type base_len: int
    :returns: True if the suffix is allowed by the heuristic rules.
    :rtype: bool
    """
    if base_len <= 3:
        return extra == "s"
    if base_len == 4:
        return extra in ("s", "e", "n", "en")
    return len(extra) <= _max_extra_len(base_len)


def _is_blocked_pair(base: str, word: str) -> bool:
    """Return True if a pair should be excluded from merging.

    :param base: Candidate base token.
    :type base: str
    :param word: Candidate variant token.
    :type word: str
    :returns: True if the pair is blocked.
    :rtype: bool
    """
    if base in ("wand", "wande") and word.startswith("wandel"):
        return True
    return False


def _choose_key(words: Iterable[str]) -> str:
    """Pick a deterministic key for a merged group.

    :param words: Collection of candidate words.
    :type words: Iterable[str]
    :returns: Shortest alphabetical token.
    :rtype: str
    """
    return sorted(words, key=lambda w: (len(w), w))[0]


def build_lemma_candidates_from_words(
    words: Iterable[str],
    min_len: int = 3,
) -> Dict[str, List[str]]:
    """Build conservative lemma candidate groups from an iterable of words.

    :param words: Iterable of strings (prefixes and/or suffixes).
    :type words: Iterable[str]
    :param min_len: Minimum base length to consider.
    :type min_len: int
    :returns: Mapping of lemma candidate to its variant group.
    :rtype: dict[str, list[str]]
    """
    words_series = pd.Series(words, dtype="string")
    words_series = words_series.dropna().str.strip().str.lower()
    words_series = words_series[words_series.str.len() >= min_len]

    unique_words = sorted(set(words_series.tolist()), key=lambda w: (len(w), w))
    assigned = set()
    candidates: Dict[str, List[str]] = {}

    for base in unique_words:
        if base in assigned:
            continue
        base_len = len(base)
        group = [base]

        for word in unique_words:
            if word == base:
                continue
            if _is_blocked_pair(base, word) or _is_blocked_pair(word, base):
                continue
            if word.startswith(base):
                extra = word[base_len:]
                if _allowed_small_suffix(extra, base_len):
                    group.append(word)
            elif base.startswith(word):
                extra = base[len(word) :]
                if _allowed_small_suffix(extra, len(word)):
                    group.append(word)

        if len(group) < 2:
            assigned.add(base)
            continue

        group = sorted(set(group), key=lambda w: (len(w), w))
        key = group[0]
        candidates[key] = group
        assigned.update(group)

    return candidates


def build_lemma_candidates(
    prefixes: Iterable[str],
    suffixes: Iterable[str],
    min_len: int = 3,
) -> Dict[str, List[str]]:
    """Build lemma candidates from prefix and suffix series.

    :param prefixes: Prefix tokens.
    :type prefixes: Iterable[str]
    :param suffixes: Suffix tokens.
    :type suffixes: Iterable[str]
    :param min_len: Minimum base length to consider.
    :type min_len: int
    :returns: Mapping of lemma candidate to its variant group.
    :rtype: dict[str, list[str]]
    """
    words = pd.concat(
        [
            pd.Series(prefixes, dtype="string"),
            pd.Series(suffixes, dtype="string"),
        ]
    )
    return build_lemma_candidates_from_words(words, min_len=min_len)


def merge_overlapping_candidates(
    candidates: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    """Merge candidate groups that overlap into connected components.

    :param candidates: Mapping of candidate keys to variant groups.
    :type candidates: dict[str, list[str]]
    :returns: Merged mapping with a deterministic key per component.
    :rtype: dict[str, list[str]]
    """
    unvisited = set(candidates.keys())
    merged: Dict[str, List[str]] = {}

    while unvisited:
        start = unvisited.pop()
        stack = [start]
        component = set()

        while stack:
            key = stack.pop()
            if key in component:
                continue
            component.add(key)
            for word in candidates.get(key, []):
                if word in candidates and word not in component:
                    stack.append(word)
                    unvisited.discard(word)

        all_words = set()
        for key in component:
            all_words.update(candidates.get(key, []))
            all_words.add(key)
        all_words = sorted(all_words)
        merged_key = _choose_key(all_words)
        merged[merged_key] = all_words

    return merged
