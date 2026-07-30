# Methodology

The public analysis uses panel regressions with firm and year fixed effects. The core explanatory variable is `CEO_age_w`. Baseline dependent variables are `AEM_w` and `REM`; the fixed age-band REM specification uses `REM_w`.

`AEM_w` is the winsorized accrual-based earnings-management measure used in the project. Its original scaling denominator or monetary unit cannot be reliably recovered from the retained project materials, so coefficients are reported in the variable's stored scale without a monetary or percentage-point interpretation.

Controls are `Degree_w`, `Gender_w`, `OperatingRevenueGrowth_w`, `Size_w`, `TotalSalaryln`, and `Separation`. The median split uses `Young_CEO == 1` as equivalent to `CEO_age_w < 53`, with age 53 assigned to the senior group. Fixed age bands use age below 45 as the omitted group, `MidAge` for ages 45 to 59, and `OldAge` for ages 60 and above. Missing age records remain missing and do not enter age-group models.
