import csv
import hashlib
import subprocess
import sys
from pathlib import Path


TEXT_EXTENSIONS = {".py", ".md", ".csv", ".yaml", ".yml", ".toml", ".txt"}

FILE_TYPE_PURPOSE = {
    ".py": ("code", "reproducible analysis or test code"),
    ".md": ("documentation", "public project documentation or QA summary"),
    ".csv": ("summary data", "public schema, QA register, or generated summary results"),
    ".yaml": ("configuration", "example configuration or workflow"),
    ".yml": ("configuration", "example configuration or workflow"),
    ".toml": ("configuration", "Python project and test configuration"),
    ".txt": ("text", "small public text metadata"),
    ".png": ("figure", "public generated figure"),
    "": ("text", "repository metadata"),
}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_text(path):
    return path.name in {".gitignore", ".gitattributes"} or path.suffix.lower() in TEXT_EXTENSIONS


def assert_lf_only(root, tracked):
    offenders = []
    for rel in tracked:
        path = root / rel
        if not path.exists() or not is_text(path):
            continue
        data = path.read_bytes()
        if b"\r\n" in data or b"\r" in data:
            offenders.append(rel)
    if offenders:
        raise SystemExit("CRLF or CR line endings found: " + ", ".join(offenders))


def build():
    root = Path(__file__).resolve().parents[1]
    tracked = subprocess.run(["git", "ls-files"], cwd=root, text=True, capture_output=True, check=True).stdout.splitlines()
    assert_lf_only(root, tracked)
    rows = []
    for rel in tracked:
        if rel == "qa/PUBLIC_FILE_REGISTER.csv":
            rows.append({
                "path": rel,
                "size_bytes": "self_hash_excluded",
                "sha256": "self_hash_excluded",
                "file_type": "summary data",
                "public_purpose": "this register; self hash excluded to avoid a non-convergent hash cycle",
            })
            continue
        path = root / rel
        kind, purpose = FILE_TYPE_PURPOSE.get(path.suffix.lower(), ("other", "public repository file"))
        rows.append({
            "path": rel,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "file_type": kind,
            "public_purpose": purpose,
        })
    out = root / "qa" / "PUBLIC_FILE_REGISTER.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "size_bytes", "sha256", "file_type", "public_purpose"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    build()
