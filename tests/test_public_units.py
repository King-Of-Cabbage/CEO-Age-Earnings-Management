from pathlib import Path
import pandas as pd
from src.load_data import load_project_data
from src.variables import add_median_split, add_age_bands, CONTROLS
from src.model_spec import ModelSpec
from src.estimators import fit_panel
from src.result_writer import write_rows


FIXTURE = Path(__file__).parent / "fixtures" / "synthetic_panel.csv"


def test_fixture_schema_and_index_normalization():
    df = load_project_data(FIXTURE)
    assert df["id"].str.len().eq(6).all()
    assert df["year"].between(2018, 2023).all()


def test_median_split_boundary_keeps_53_in_senior_group():
    df = add_median_split(load_project_data(FIXTURE))
    row_52 = df[df["CEO_age_w"] == 52].iloc[0]
    row_53 = df[df["CEO_age_w"] == 53].iloc[0]
    assert row_52["Young_CEO_rebuilt"] == 1
    assert row_53["Young_CEO_rebuilt"] == 0


def test_age_band_boundaries_and_missingness():
    df = add_age_bands(load_project_data(FIXTURE))
    assert df[df["CEO_age_w"] == 44]["MidAge"].eq(0).all()
    assert df[df["CEO_age_w"] == 45]["MidAge"].eq(1).all()
    assert df[df["CEO_age_w"] == 59]["OldAge"].eq(0).all()
    assert df[df["CEO_age_w"] == 60]["OldAge"].eq(1).all()
    missing = df["CEO_age_w"].isna()
    assert df.loc[missing, "MidAge"].isna().all()
    assert df.loc[missing, "OldAge"].isna().all()


def test_model_rejects_raw_and_winsorized_age_together():
    df = load_project_data(FIXTURE)
    spec = ModelSpec("bad", "AEM_w", ("CEO_age", "CEO_age_w"), tuple(CONTROLS), entity_effects=False, time_effects=False)
    try:
        fit_panel(df, spec)
    except ValueError as exc:
        assert "cannot include both" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_result_writer_format(tmp_path):
    path = tmp_path / "rows.csv"
    write_rows(path, [{"a": 1, "b": "x"}])
    assert "a,b" in path.read_text(encoding="utf-8-sig")
