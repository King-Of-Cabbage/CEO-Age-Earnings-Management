from pathlib import Path
import subprocess
import sys


def test_run_all_with_synthetic_fixture(tmp_path):
    cfg = tmp_path / "config.yaml"
    out = tmp_path / "out"
    figs = tmp_path / "figures"
    data = Path(__file__).parent / "fixtures" / "synthetic_panel.csv"
    cfg.write_text(f'data_path: "{data.as_posix()}"\noutput_dir: "{out.as_posix()}"\nfigure_dir: "{figs.as_posix()}"\n', encoding="utf-8")
    proc = subprocess.run([sys.executable, "run_all.py", "--config", str(cfg)], text=True, capture_output=True)
    assert proc.returncode == 0, proc.stderr
    assert (out / "reproduced_primary_results.csv").exists()
    assert (out / "reproduced_sensitivity_results.csv").exists()
    assert (figs / "sample_flow.png").exists()
