from pathlib import Path
import yaml


PATH_KEYS = {"data_path", "output_dir", "figure_dir"}


def read_config(path):
    config_path = Path(path).expanduser().resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    required = ["data_path", "output_dir", "figure_dir"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")
    config_dir = config_path.parent
    out = {
        "config_path": str(config_path),
        "config_dir": str(config_dir),
    }
    for key, value in data.items():
        if key in PATH_KEYS:
            raw = Path(str(value)).expanduser()
            out[key] = str(raw if raw.is_absolute() else (config_dir / raw).resolve())
        else:
            out[key] = str(value)
    return out
