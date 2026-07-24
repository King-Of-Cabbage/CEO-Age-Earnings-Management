# Reproducibility

Analysis and publication are separate actions. `python run_all.py --config config.local.yaml` writes outputs only to paths named by the config file. `python scripts/publish_artifacts.py --config config.local.yaml` copies a fixed whitelist of reviewed summaries and PNG figures into `results/` and `figures/`.

The main public result layer is `results/reproduced_primary_results.csv`, which uses firm-clustered standard errors. The sensitivity layer is `results/reproduced_sensitivity_results.csv`, which repeats each public model under heteroskedastic robust, firm-clustered, year-clustered, and firm-year two-way clustered covariance settings.

Local release QA runs the full analysis twice from two empty output directories and compares file sets, CSV row counts, CSV column names, CSV values, JSON content, and PNG SHA-256 hashes.
