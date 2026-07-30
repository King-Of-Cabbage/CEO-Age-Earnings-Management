import csv
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

from src.config import read_config
from scripts.copy_public_summaries import RESULT_FILES, FIGURE_FILES


ROOT = Path(__file__).resolve().parents[1]


def test_relative_config_paths_resolve_from_config_directory(tmp_path):
    data_dir = tmp_path / "data" / "private"
    data_dir.mkdir(parents=True)
    data_path = data_dir / "sample.csv"
    data_path.write_text("x\n1\n", encoding="utf-8")
    cfg = tmp_path / "config.yaml"
    cfg.write_text('data_path: "data/private/sample.csv"\noutput_dir: "output_local"\nfigure_dir: "output_local/figures"\n', encoding="utf-8")
    parsed = read_config(cfg)
    assert Path(parsed["data_path"]) == data_path.resolve()
    assert Path(parsed["output_dir"]) == (tmp_path / "output_local").resolve()
    assert Path(parsed["figure_dir"]) == (tmp_path / "output_local" / "figures").resolve()


def test_demo_run_from_outside_repo_does_not_touch_public_artifacts(tmp_path):
    before = {p: (ROOT / p).read_bytes() for p in ["results/reproduced_primary_results.csv", "figures/sample_flow.png"]}
    out = tmp_path / "out"
    figs = tmp_path / "figs"
    cfg = tmp_path / "config.yaml"
    data = ROOT / "tests" / "fixtures" / "synthetic_panel.csv"
    cfg.write_text(f'data_path: "{data.as_posix()}"\noutput_dir: "{out.as_posix()}"\nfigure_dir: "{figs.as_posix()}"\n', encoding="utf-8")
    proc = subprocess.run([sys.executable, str(ROOT / "run_all.py"), "--config", str(cfg)], cwd=tmp_path, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stderr
    assert (out / "reproduced_primary_results.csv").exists()
    assert (figs / "sample_flow.png").exists()
    for rel, content in before.items():
        assert (ROOT / rel).read_bytes() == content


def test_public_summary_copy_uses_whitelists():
    assert set(RESULT_FILES) == {"sample_summary.csv", "reproduced_primary_results.csv", "reproduced_sensitivity_results.csv"}
    assert "aem_age_band_robustness.png" in set(FIGURE_FILES)
    assert "rem_age_band_robustness.png" in set(FIGURE_FILES)


def test_result_layers_and_counts():
    primary = pd.read_csv(ROOT / "results" / "reproduced_primary_results.csv")
    sens = pd.read_csv(ROOT / "results" / "reproduced_sensitivity_results.csv")
    assert len(primary) == 18
    assert len(sens) == 72
    assert set(primary["layer"]) == {"reproduced_primary"}
    assert set(sens["layer"]) == {"reproduced_sensitivity"}
    assert set(sens["covariance"]) == {"robust", "cluster_firm", "cluster_year", "cluster_two_way"}
    counts = sens.groupby(["analysis", "dependent_variable", "core_variable", "sample_group"])["covariance"].nunique()
    assert counts.eq(4).all()


def test_figure_variable_scopes_and_schema_terms():
    assert (ROOT / "figures" / "aem_age_band_robustness.png").exists()
    assert (ROOT / "figures" / "rem_age_band_robustness.png").exists()
    plotting = (ROOT / "src" / "plotting.py").read_text(encoding="utf-8")
    assert 'core_variable"] == "CEO_age_w"' in plotting
    assert 'isin(["MidAge", "OldAge"])' in plotting
    schema = (ROOT / "data" / "required_schema.csv").read_text(encoding="utf-8-sig")
    docs = (ROOT / "docs" / "data_dictionary.md").read_text(encoding="utf-8")
    assert "CEO-chair separation" not in schema + docs
    assert "control rights and ownership rights" in schema
    assert "G = 0" in docs and "BIGFour = 1" in docs


def test_public_text_has_no_local_paths_or_blocked_terms():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
    forbidden = ["C:" + "\\" * 2 + "Users" + "\\" * 2, "Admin" + "istrator", "Desktop" + "\\" + "AFA", "api" + " key", "access" + " token", "pass" + "word"]
    for rel in tracked:
        path = ROOT / rel
        if path.suffix.lower() not in {".py", ".md", ".csv", ".yaml", ".yml", ".toml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for item in forbidden:
            assert item.lower() not in text.lower(), f"{item} in {rel}"


def test_markdown_links_are_valid_and_workflow_yaml_parses():
    yaml.safe_load((ROOT / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8"))
    for md in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")), ROOT / "data" / "README.md"]:
        text = md.read_text(encoding="utf-8")
        for target in re.findall(r"!?\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            assert (md.parent / target).resolve().exists(), f"{target} from {md}"


def test_readme_baseline_numbers_match_public_csv():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    primary = pd.read_csv(ROOT / "results" / "reproduced_primary_results.csv")
    base = primary[(primary["analysis"] == "Baseline") & (primary["core_variable"] == "CEO_age_w")]
    for _, row in base.iterrows():
        if row["dependent_variable"] == "AEM_w":
            assert f"{row['coefficient']:,.3f}" in readme
            assert f"{row['p_value']:.4f}" in readme
            assert "RMB" not in readme
        if row["dependent_variable"] == "REM":
            assert f"{row['coefficient']:.7f}" in readme
            assert f"{row['p_value']:.4f}" in readme
