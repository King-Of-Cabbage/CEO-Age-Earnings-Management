# Data Dictionary

The repository does not include real observations. Users must provide a licensed local file matching `../data/required_schema.csv`.

## Core Explanatory Variable

`CEO_age_w` is the winsorized CEO age used in all public regressions. The raw `CEO_age` field is retained for validation and missingness checks.

## Dependent Variables

`AEM_w` is the winsorized accrual-based earnings management measure retained from the project data. The public reconstruction does not assign a monetary unit or scaling denominator to this field because that scale cannot be verified from the available project materials. `REM` is the real earnings management measure used in baseline, median split, ownership, and auditor-group models. `REM_w` is used for the fixed age-band robustness model.

## Controls

Controls are `Degree_w`, `Gender_w`, `OperatingRevenueGrowth_w`, `Size_w`, `TotalSalaryln`, and `Separation`. `Separation` means the difference between the controlling shareholder's control rights and ownership rights, measured in percentage points.

## Group Variables

`Young_CEO = 1` means `CEO_age_w < 53`; age 53 belongs to the senior group. `G = 0` indicates non-state-owned enterprises and `G = 1` indicates state-owned enterprises. `BIGFour = 1` indicates Big Four auditor and `BIGFour = 2` indicates non-Big Four auditor.

## Winsorized Fields

Variables ending in `_w` are winsorized versions used for the public reproducible models.

## License Boundary

The source data are license-restricted. This repository provides schema and aggregate outputs only, not row-level company records.
