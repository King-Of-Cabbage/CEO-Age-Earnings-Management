import pandas as pd


CONTROLS = [
    "Degree_w",
    "Gender_w",
    "OperatingRevenueGrowth_w",
    "Size_w",
    "TotalSalaryln",
    "Separation",
]

MAIN_X = "CEO_age_w"
AEM_DEP = "AEM_w"
REM_DEP = "REM"
REM_AGE_BAND_DEP = "REM_w"


def add_median_split(df):
    out = df.copy()
    out["Young_CEO_rebuilt"] = pd.NA
    valid = out["CEO_age_w"].notna()
    out.loc[valid, "Young_CEO_rebuilt"] = (out.loc[valid, "CEO_age_w"] < 53).astype(int)
    return out


def add_age_bands(df):
    out = df.copy()
    out["MidAge"] = pd.Series(pd.NA, index=out.index, dtype="Float64")
    out["OldAge"] = pd.Series(pd.NA, index=out.index, dtype="Float64")
    valid = out["CEO_age_w"].notna()
    out.loc[valid, "MidAge"] = ((out.loc[valid, "CEO_age_w"] >= 45) & (out.loc[valid, "CEO_age_w"] < 60)).astype(float)
    out.loc[valid, "OldAge"] = (out.loc[valid, "CEO_age_w"] >= 60).astype(float)
    return out
