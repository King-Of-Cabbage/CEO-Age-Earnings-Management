import csv
import hashlib
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".py", ".md", ".csv", ".yaml", ".yml", ".toml", ".txt"}
PUBLIC_CSV_ROWS = {
    "results/reproduced_primary_results.csv": 18,
    "results/reproduced_sensitivity_results.csv": 72,
    "results/sample_summary.csv": 10,
}


def git_files():
    return subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()


def is_text(path):
    return path.name in {".gitignore", ".gitattributes"} or path.suffix.lower() in TEXT_EXTENSIONS


def test_all_public_text_files_use_lf_only():
    for rel in git_files():
        path = ROOT / rel
        if not is_text(path):
            continue
        data = path.read_bytes()
        assert b"\r\n" not in data, rel
        assert b"\r" not in data, rel


def test_csv_files_are_readable_and_public_result_shapes_are_stable():
    expected_columns = {
        rel: list(pd.read_csv(ROOT / rel).columns)
        for rel in PUBLIC_CSV_ROWS
    }
    for rel in git_files():
        path = ROOT / rel
        if path.suffix.lower() == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as f:
                list(csv.reader(f))
    for rel, row_count in PUBLIC_CSV_ROWS.items():
        df = pd.read_csv(ROOT / rel)
        assert len(df) == row_count
        assert list(df.columns) == expected_columns[rel]


def test_public_file_register_hashes_match_lf_worktree():
    rows = {r["path"]: r for r in csv.DictReader((ROOT / "qa/PUBLIC_FILE_REGISTER.csv").open(encoding="utf-8-sig", newline=""))}
    files = set(git_files())
    assert set(rows) == files
    for rel in files:
        if rel == "qa/PUBLIC_FILE_REGISTER.csv":
            assert rows[rel]["sha256"] == "self_hash_excluded"
            continue
        path = ROOT / rel
        assert int(rows[rel]["size_bytes"]) == path.stat().st_size
        assert rows[rel]["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
