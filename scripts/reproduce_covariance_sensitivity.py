import argparse
from pathlib import Path
from src.config import read_config
from src.result_writer import write_rows
from scripts.reproduce_baseline import run as baseline
from scripts.reproduce_median_split import run as median_split
from scripts.reproduce_ownership import run as ownership
from scripts.reproduce_auditor_groups import run as auditor_groups
from scripts.reproduce_age_bands import run as age_bands


COVARIANCES = ["robust", "cluster_firm", "cluster_year", "cluster_two_way"]


def run(config):
    cfg = read_config(config)
    rows = []
    for cov in COVARIANCES:
        rows.extend(baseline(config, cov, layer="reproduced_sensitivity"))
        rows.extend(median_split(config, cov, layer="reproduced_sensitivity"))
        rows.extend(ownership(config, cov, layer="reproduced_sensitivity"))
        rows.extend(auditor_groups(config, cov, layer="reproduced_sensitivity"))
        rows.extend(age_bands(config, cov, layer="reproduced_sensitivity"))
    write_rows(Path(cfg["output_dir"]) / "reproduced_sensitivity_results.csv", rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    run(parser.parse_args().config)
