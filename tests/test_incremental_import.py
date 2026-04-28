import sqlite3
from pathlib import Path

import pytest

import handle_data_processing as hdp


class _SequentialPool:
    """Small multiprocessing.Pool substitute for deterministic fast tests."""

    def __init__(self, *_args, **_kwargs):
        pass

    def starmap(self, func, args_list):
        return [func(*args) for args in args_list]

    def close(self):
        pass

    def join(self):
        pass


@pytest.fixture
def sequential_pool(monkeypatch):
    monkeypatch.setattr(hdp.multiprocessing, "Pool", _SequentialPool)


def _write_html(path: Path, body_text: str) -> None:
    html = f"""<!doctype html>
<html lang=\"de\">
  <head><meta charset=\"utf-8\"><title>Test</title></head>
  <body>{body_text}</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def _write_html_bytes(path: Path, body_text: str, encoding: str = "cp1252") -> None:
    html = f"""<!doctype html>
<html lang=\"de\">
    <head><meta charset=\"utf-8\"><title>Test</title></head>
    <body>{body_text}</body>
</html>
"""
    path.write_bytes(html.encode(encoding))


def _count_rows(db_path: Path, table: str) -> int:
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
        return int(cur.fetchone()[0])
    finally:
        conn.close()


def test_incremental_import_only_appends_new_day(tmp_path, sequential_pool):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    day1_filename = "2025-01-01-source.html"
    day2_filename = "2025-01-02-source.html"

    _write_html(
        input_dir / day1_filename,
        "Heute ist Klimawandel wichtig. Klimakrise betrifft alle.",
    )
    _write_html(input_dir / day2_filename, "Klimaschutz ist notwendig.")

    db_path = tmp_path / "dwh_test.db"

    first_batch = [
        {
            "name": "source",
            "date": "2025-01-01",
            "file_name": day1_filename,
            "encoding": "utf-8",
        }
    ]

    hdp.batch_process_newspapers(
        newspapers=first_batch,
        batch_size=1,
        num_workers=1,
        db_path=str(db_path),
        input_path_prefix=str(input_dir),
    )

    newspapers_after_first = _count_rows(db_path, "newspapers")
    context_after_first = _count_rows(db_path, "context")

    assert newspapers_after_first == 1
    assert context_after_first > 0

    hdp.batch_process_newspapers(
        newspapers=first_batch,
        batch_size=1,
        num_workers=1,
        db_path=str(db_path),
        input_path_prefix=str(input_dir),
    )

    newspapers_after_rerun = _count_rows(db_path, "newspapers")
    context_after_rerun = _count_rows(db_path, "context")

    assert newspapers_after_rerun == newspapers_after_first
    assert context_after_rerun == context_after_first

    second_batch = [
        {
            "name": "source",
            "date": "2025-01-02",
            "file_name": day2_filename,
            "encoding": "utf-8",
        }
    ]

    hdp.batch_process_newspapers(
        newspapers=second_batch,
        batch_size=1,
        num_workers=1,
        db_path=str(db_path),
        input_path_prefix=str(input_dir),
    )

    newspapers_after_new_day = _count_rows(db_path, "newspapers")
    context_after_new_day = _count_rows(db_path, "context")

    assert newspapers_after_new_day == newspapers_after_first + 1
    assert context_after_new_day > context_after_first


def test_import_handles_non_utf8_html(tmp_path, sequential_pool):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    filename = "2021-10-07-dhv.html"
    _write_html_bytes(
        input_dir / filename,
        '<div data-note="fluggelãndekarte">Klimakrise betrifft alle.</div>',
        encoding="cp1252",
    )

    db_path = tmp_path / "dwh_test_non_utf8.db"
    batch = [
        {
            "name": "dhv",
            "date": "2021-10-07",
            "file_name": filename,
            "encoding": "utf-8",
        }
    ]

    hdp.batch_process_newspapers(
        newspapers=batch,
        batch_size=1,
        num_workers=1,
        db_path=str(db_path),
        input_path_prefix=str(input_dir),
    )

    assert _count_rows(db_path, "newspapers") == 1
    assert _count_rows(db_path, "context") > 0
