import argparse
from pathlib import Path
from src.config import read_config
from src.load_data import load_project_data
from src.variables import CONTROLS, add_median_split
from src.result_writer import write_rows


def run(config):
    cfg = read_config(config)
    df = add_median_split(load_project_data(cfg["data_path"]))
    baseline_cols = ["id", "year", "AEM_w", "REM", "CEO_age_w"] + CONTROLS
    baseline = df[baseline_cols].dropna()
    rows = [
        {"metric": "records", "value": int(df.shape[0])},
        {"metric": "ceo_age_missing", "value": int(df["CEO_age"].isna().sum())},
        {"metric": "descriptive_sample", "value": int(df["CEO_age"].notna().sum())},
        {"metric": "baseline_sample", "value": int(baseline.shape[0])},
        {"metric": "baseline_firms", "value": int(baseline["id"].nunique())},
        {"metric": "year_min", "value": int(df["year"].min())},
        {"metric": "year_max", "value": int(df["year"].max())},
        {"metric": "young_ceo_count", "value": int((baseline.merge(df[["id", "year", "Young_CEO_rebuilt"]], on=["id", "year"], how="left")["Young_CEO_rebuilt"] == 1).sum())},
        {"metric": "senior_ceo_count", "value": int((baseline.merge(df[["id", "year", "Young_CEO_rebuilt"]], on=["id", "year"], how="left")["Young_CEO_rebuilt"] == 0).sum())},
        {"metric": "median_split_mismatch", "value": int((df.loc[df["CEO_age_w"].notna(), "Young_CEO"] != df.loc[df["CEO_age_w"].notna(), "Young_CEO_rebuilt"]).sum())},
    ]
    write_rows(Path(cfg["output_dir"]) / "sample_summary.csv", rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    run(parser.parse_args().config)
