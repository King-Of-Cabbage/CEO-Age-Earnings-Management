import pytest
import pandas as pd
from src.config import read_config
from src.load_data import load_project_data
from src.variables import CONTROLS, add_median_split, add_age_bands
from src.model_spec import ModelSpec
from src.estimators import fit_panel


pytestmark = pytest.mark.integration


def test_local_sample_counts(local_config):
    cfg = read_config(local_config)
    df = add_median_split(load_project_data(cfg["data_path"]))
    baseline = df[["id", "year", "AEM_w", "REM", "CEO_age_w"] + CONTROLS].dropna()
    assert df.shape[0] == 13125
    assert df["CEO_age"].isna().sum() == 6
    assert df["CEO_age"].notna().sum() == 13119
    assert baseline.shape[0] == 12529
    assert baseline["id"].nunique() == 2944
    grouped = baseline.merge(df[["id", "year", "Young_CEO_rebuilt"]], on=["id", "year"], how="left")
    assert (grouped["Young_CEO_rebuilt"] == 1).sum() == 5749
    assert (grouped["Young_CEO_rebuilt"] == 0).sum() == 6780


def test_table4_coefficients_within_locked_tolerance(local_config):
    cfg = read_config(local_config)
    df = load_project_data(cfg["data_path"])
    targets = {"AEM_w": 4727401.705, "REM": -0.0020135}
    for dep, target in targets.items():
        spec = ModelSpec("Baseline", dep, ("CEO_age_w",), tuple(CONTROLS), covariance="cluster_firm")
        result, _ = fit_panel(df, spec)
        assert abs(float(result.params["CEO_age_w"]) - target) < max(abs(target) * 0.0005, 1e-7)


def test_age_band_complete_case_counts(local_config):
    cfg = read_config(local_config)
    df = add_age_bands(load_project_data(cfg["data_path"]))
    cols = ["id", "year", "AEM_w", "REM_w", "MidAge", "OldAge"] + CONTROLS
    sample = df[cols].dropna()
    assert sample.shape[0] == 12529
    assert sample["id"].nunique() == 2944
