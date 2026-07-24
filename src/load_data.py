import re
from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "id", "year", "CEO_age", "CEO_age_w", "Young_CEO", "AEM_w", "REM", "REM_w",
    "Degree_w", "Gender_w", "OperatingRevenueGrowth_w", "Size_w",
    "TotalSalaryln", "Separation", "G", "BIGFour",
]


def normalize_id(value):
    if pd.isna(value):
        return pd.NA
    text = str(value).strip()
    if re.fullmatch(r"\d+(\.0)?", text):
        text = str(int(float(text)))
    return text.zfill(6)


def normalize_year(value):
    if pd.isna(value):
        return pd.NA
    return int(float(value))


def load_project_data(path):
    path = Path(path)
    if path.suffix.lower() in {".xls", ".xlsx"}:
        df = pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported data format: {path.suffix}")
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    out = df.copy()
    out["id"] = out["id"].map(normalize_id)
    out["year"] = out["year"].map(normalize_year)
    numeric = [c for c in REQUIRED_COLUMNS if c != "id"]
    for col in numeric:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def baseline_sample(df, depvar):
    from src.variables import CONTROLS
    cols = ["id", "year", depvar, "CEO_age_w"] + CONTROLS
    return df[cols].dropna()
