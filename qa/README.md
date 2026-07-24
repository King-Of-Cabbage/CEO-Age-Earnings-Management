# Public QA Summary

This directory contains public release checks only. Detailed local command logs are kept outside the repository and are not included here because they can contain local machine paths.

Public commands summarized by this QA layer:

- `python run_all.py --config config.local.yaml`
- `pytest -m "not integration"`
- `pytest -m integration --config config.local.yaml`
- `python scripts/publish_artifacts.py --config config.local.yaml`
