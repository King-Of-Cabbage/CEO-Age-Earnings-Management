from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_sample_flow(summary_csv, path):
    df = pd.read_csv(summary_csv)
    vals = {row["metric"]: int(float(row["value"])) for _, row in df.iterrows()}
    labels = ["Raw records", "Non-missing age", "Baseline sample"]
    counts = [vals.get("records", 0), vals.get("descriptive_sample", 0), vals.get("baseline_sample", 0)]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(labels, counts, color=["#4C78A8", "#59A14F", "#F28E2B"])
    ax.set_ylabel("Firm-year observations")
    ax.set_title("Sample flow for public reproduction")
    ax.bar_label(bars, fmt="%d", padding=3)
    ax.set_ylim(0, max(counts) * 1.18)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _plot_rows(data, path, title, scale, x_label):
    data = data.copy()
    data["estimate"] = data["coefficient"] / scale
    data["low"] = data["ci_lower"] / scale
    data["high"] = data["ci_upper"] / scale
    labels = (data["analysis"] + " / " + data["sample_group"] + " / " + data["core_variable"]).tolist()
    fig_h = max(3.8, 0.44 * len(data) + 1.4)
    fig, ax = plt.subplots(figsize=(8.2, fig_h))
    ypos = range(len(data))
    ax.errorbar(data["estimate"], ypos, xerr=[data["estimate"] - data["low"], data["high"] - data["estimate"]], fmt="o", color="#2F5597", ecolor="#8FAADC", capsize=3)
    ax.axvline(0, color="#555555", linewidth=0.9)
    ax.set_yticks(list(ypos), labels)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_continuous_age_plot(results_csv, dependent, path, title, scale=1.0, x_label="Coefficient"):
    df = pd.read_csv(results_csv)
    data = df[(df["layer"] == "reproduced_primary") & (df["dependent_variable"] == dependent) & (df["core_variable"] == "CEO_age_w")]
    _plot_rows(data, path, title, scale, x_label)


def save_age_band_plot(results_csv, dependent, path, title, scale=1.0, x_label="Coefficient"):
    df = pd.read_csv(results_csv)
    data = df[(df["layer"] == "reproduced_primary") & (df["dependent_variable"] == dependent) & (df["core_variable"].isin(["MidAge", "OldAge"]))]
    _plot_rows(data, path, title, scale, x_label)


def save_covariance_plot(sensitivity_csv, dependent, path, title, scale=1.0, x_label="Coefficient"):
    df = pd.read_csv(sensitivity_csv)
    data = df[(df["analysis"] == "Baseline") & (df["dependent_variable"] == dependent) & (df["core_variable"] == "CEO_age_w")].copy()
    data["estimate"] = data["coefficient"] / scale
    data["low"] = data["ci_lower"] / scale
    data["high"] = data["ci_upper"] / scale
    labels = data["covariance_label"].tolist()
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ypos = range(len(data))
    ax.errorbar(data["estimate"], ypos, xerr=[data["estimate"] - data["low"], data["high"] - data["estimate"]], fmt="o", color="#7A3E9D", ecolor="#C5A3D8", capsize=3)
    ax.axvline(0, color="#555555", linewidth=0.9)
    ax.set_yticks(list(ypos), labels)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)
