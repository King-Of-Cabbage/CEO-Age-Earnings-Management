import argparse
from pathlib import Path
from src.config import read_config
from src.plotting import save_sample_flow, save_continuous_age_plot, save_age_band_plot, save_covariance_plot


def run(config):
    cfg = read_config(config)
    out = Path(cfg["output_dir"])
    figs = Path(cfg["figure_dir"])
    save_sample_flow(out / "sample_summary.csv", figs / "sample_flow.png")
    save_continuous_age_plot(out / "reproduced_primary_results.csv", "AEM_w", figs / "aem_coefficients.png", "CEO_age_w coefficients for AEM models", 1_000_000, "Coefficient on AEM measure, x10^6 units")
    save_continuous_age_plot(out / "reproduced_primary_results.csv", "REM", figs / "rem_coefficients.png", "CEO_age_w coefficients for REM models", 1.0, "Coefficient per one-year increase")
    save_age_band_plot(out / "reproduced_primary_results.csv", "AEM_w", figs / "aem_age_band_robustness.png", "AEM age-band differences relative to CEOs below 45", 1_000_000, "Coefficient difference on AEM measure, x10^6 units")
    save_age_band_plot(out / "reproduced_primary_results.csv", "REM_w", figs / "rem_age_band_robustness.png", "REM age-band differences relative to CEOs below 45", 1.0, "Coefficient difference")
    save_covariance_plot(out / "reproduced_sensitivity_results.csv", "AEM_w", figs / "covariance_sensitivity_aem.png", "Baseline AEM covariance sensitivity", 1_000_000, "Coefficient on AEM measure, x10^6 units")
    save_covariance_plot(out / "reproduced_sensitivity_results.csv", "REM", figs / "covariance_sensitivity_rem.png", "Baseline REM covariance sensitivity", 1.0, "Coefficient per one-year increase")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    run(parser.parse_args().config)
