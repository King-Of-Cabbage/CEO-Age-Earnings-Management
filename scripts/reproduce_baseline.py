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
    specs = [
        ModelSpec("Baseline", "AEM_w", ("CEO_age_w",), tuple(CONTROLS), covariance=covariance),
        ModelSpec("Baseline", "REM", ("CEO_age_w",), tuple(CONTROLS), covariance=covariance),
    ]
    rows = []
    for spec in specs:
        result, data = fit_panel(df, spec)
        rows.append(format_result(spec, result, data, "CEO_age_w", layer))
    write_rows(Path(cfg["output_dir"]) / f"baseline_{covariance}.csv", rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--covariance", default="cluster_firm")
    run(parser.parse_args().config, parser.parse_args().covariance)
