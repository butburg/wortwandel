"""Database analysis helpers for notebooks.

phinx: Sphinx documentation tool.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import sqlite3


def monthly_counts_from_db(db_path: Path, source_label: str) -> pd.DataFrame:
    """Load monthly newspaper and context counts from a SQLite database.

    :param db_path: Path to the SQLite database.
    :type db_path: pathlib.Path
    :param source_label: Label assigned to the source.
    :type source_label: str
    :returns: Monthly counts DataFrame.
    :rtype: pandas.DataFrame
    """
    query = """
    WITH monthly_newspapers AS (
        SELECT
            substr(data_published, 1, 7) AS month,
            COUNT(*) AS newspapers_count
        FROM newspapers
        WHERE data_published IS NOT NULL
        GROUP BY substr(data_published, 1, 7)
    ),
    monthly_context AS (
        SELECT
            substr(n.data_published, 1, 7) AS month,
            COUNT(*) AS context_count
        FROM context c
        JOIN newspapers n ON n.newspaper_id = c.newspaper_id
        WHERE n.data_published IS NOT NULL
        GROUP BY substr(n.data_published, 1, 7)
    ),
    all_months AS (
        SELECT month FROM monthly_newspapers
        UNION
        SELECT month FROM monthly_context
    )
    SELECT
        m.month,
        COALESCE(n.newspapers_count, 0) AS newspapers_count,
        COALESCE(c.context_count, 0) AS context_count
    FROM all_months m
    LEFT JOIN monthly_newspapers n ON n.month = m.month
    LEFT JOIN monthly_context c ON c.month = m.month
    ORDER BY m.month
    """

    with sqlite3.connect(str(db_path)) as conn:
        df = pd.read_sql_query(query, conn)

    df["source"] = source_label
    df["month_dt"] = pd.to_datetime(df["month"] + "-01", errors="coerce")
    return df
