import argparse
from pathlib import Path
from src.config import read_config
from src.load_data import load_project_data
from src.variables import CONTROLS
from src.model_spec import ModelSpec
from src.estimators import fit_panel, format_result
from src.result_writer import write_rows


def run(config, covariance="cluster_firm", layer="reproduced_primary"):
    cfg = read_config(config)
    df = load_project_data(cfg["data_path"])
    rows = []
    for dependent in ["AEM_w", "REM"]:
        for value, label in [(1, "Young CEO"), (0, "Senior CEO")]:
            spec = ModelSpec("Median split", dependent, ("CEO_age_w",), tuple(CONTROLS), sample=label, covariance=covariance, sample_rule=lambda d, v=value: d["Young_CEO"] == v)
            result, data = fit_panel(df, spec)
            rows.append(format_result(spec, result, data, "CEO_age_w", layer))
    write_rows(Path(cfg["output_dir"]) / f"median_split_{covariance}.csv", rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--covariance", default="cluster_firm")
    args = parser.parse_args()
    run(args.config, args.covariance)
