import argparse
from pathlib import Path
import pandas as pd
from src.config import read_config
from src.result_writer import write_json
from scripts import validate_data, reproduce_baseline, reproduce_median_split, reproduce_ownership, reproduce_auditor_groups, reproduce_age_bands, reproduce_covariance_sensitivity, build_figures


def run(config):
    cfg = read_config(config)
    out = Path(cfg["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    steps = []
    validate_data.run(config); steps.append("validate_data")
    primary = []
    primary.extend(reproduce_baseline.run(config, "cluster_firm", layer="reproduced_primary"))
    primary.extend(reproduce_median_split.run(config, "cluster_firm", layer="reproduced_primary"))
    primary.extend(reproduce_ownership.run(config, "cluster_firm", layer="reproduced_primary"))
    primary.extend(reproduce_auditor_groups.run(config, "cluster_firm", layer="reproduced_primary"))
    primary.extend(reproduce_age_bands.run(config, "cluster_firm", layer="reproduced_primary"))
    pd.DataFrame(primary).to_csv(out / "reproduced_primary_results.csv", index=False, encoding="utf-8-sig", lineterminator="\n")
    steps.extend(["baseline", "median_split", "ownership", "auditor_groups", "age_bands"])
    reproduce_covariance_sensitivity.run(config); steps.append("covariance_sensitivity")
    build_figures.run(config); steps.append("build_figures")
    write_json(out / "run_manifest.json", {"steps": steps, "step_count": len(steps)})
    return steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    run(args.config)
