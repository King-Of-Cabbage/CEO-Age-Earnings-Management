import argparse
import shutil
from pathlib import Path
from src.config import read_config


RESULT_FILES = [
    "sample_summary.csv",
    "reproduced_primary_results.csv",
    "reproduced_sensitivity_results.csv",
]
FIGURE_FILES = [
    "sample_flow.png",
    "aem_coefficients.png",
    "rem_coefficients.png",
    "aem_age_band_robustness.png",
    "rem_age_band_robustness.png",
    "covariance_sensitivity_aem.png",
    "covariance_sensitivity_rem.png",
]


def run(config):
    cfg = read_config(config)
    output_dir = Path(cfg["output_dir"])
    figure_dir = Path(cfg["figure_dir"])
    repo_root = Path(__file__).resolve().parents[1]
    copied = []
    for name in RESULT_FILES:
        src = output_dir / name
        if not src.exists():
            raise FileNotFoundError(src)
        dst = repo_root / "results" / name
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dst.relative_to(repo_root).as_posix())
    for name in FIGURE_FILES:
        src = figure_dir / name
        if not src.exists():
            raise FileNotFoundError(src)
        dst = repo_root / "figures" / name
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dst.relative_to(repo_root).as_posix())
    return copied


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    for item in run(parser.parse_args().config):
        print(item)
