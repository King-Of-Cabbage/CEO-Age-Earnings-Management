from linearmodels.panel import PanelOLS


COVARIANCE_LABELS = {
    "robust": "heteroskedastic robust",
    "cluster_firm": "firm clustered",
    "cluster_year": "year clustered",
    "cluster_two_way": "firm and year two-way clustered",
}


def fit_panel(df, spec):
    if "CEO_age" in spec.xvars and "CEO_age_w" in spec.xvars:
        raise ValueError("A model cannot include both CEO_age and CEO_age_w")
    data = df.copy()
    if spec.sample_rule is not None:
        data = data[spec.sample_rule(data)]
    cols = ["id", "year", spec.dependent] + list(spec.xvars) + list(spec.controls)
    data = data[cols].dropna().set_index(["id", "year"]).sort_index()
    if data.empty:
        raise ValueError(f"Empty model sample for {spec.analysis} / {spec.sample}")
    model = PanelOLS(
        data[spec.dependent],
        data[list(spec.xvars) + list(spec.controls)],
        entity_effects=spec.entity_effects,
        time_effects=spec.time_effects,
        drop_absorbed=True,
        check_rank=False,
    )
    if spec.covariance == "cluster_firm":
        result = model.fit(cov_type="clustered", cluster_entity=True)
    elif spec.covariance == "cluster_year":
        result = model.fit(cov_type="clustered", cluster_time=True)
    elif spec.covariance == "cluster_two_way":
        result = model.fit(cov_type="clustered", cluster_entity=True, cluster_time=True)
    elif spec.covariance == "robust":
        result = model.fit(cov_type="robust")
    else:
        raise ValueError(f"Unknown covariance setting: {spec.covariance}")
    return result, data


def stars(p_value):
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


def format_result(spec, result, data, xvar, layer):
    p_value = float(result.pvalues[xvar])
    coef = float(result.params[xvar])
    ci = result.conf_int().loc[xvar]
    return {
        "layer": layer,
        "analysis": spec.analysis,
        "dependent_variable": spec.dependent,
        "core_variable": xvar,
        "sample_group": spec.sample,
        "observations": int(data.shape[0]),
        "firms": int(data.reset_index()["id"].nunique()),
        "coefficient": coef,
        "coefficient_million_rmb": coef / 1_000_000 if spec.dependent == "AEM_w" else "",
        "standard_error": float(result.std_errors[xvar]),
        "t_statistic": float(result.tstats[xvar]),
        "p_value": p_value,
        "significance": stars(p_value),
        "covariance": spec.covariance,
        "covariance_label": COVARIANCE_LABELS[spec.covariance],
        "ci_lower": float(ci.iloc[0]),
        "ci_upper": float(ci.iloc[1]),
        "within_r_squared": float(getattr(result, "rsquared_within", float("nan"))),
    }
