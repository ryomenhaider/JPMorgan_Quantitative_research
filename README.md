# JPMorgan Quantitative Research Virtual Internship

This repository contains solutions for the JPMorgan Chase quantitative research virtual internship program.

## Project Structure

```
.
├── data/
│   ├── Loan_Data.csv          # Loan data for default prediction
│   ├── Nat_Gas.csv            # Historical natural gas prices
│   └── Nat_Gas_fortask2.csv   # Data for contract valuation
├── notebooks/
│   ├── step1.ipynb           # Initial exploration
│   ├── task2.ipynb           # Contract analysis notebook
│   ├── task3.ipynb           # Loan default prediction
│   └── task4.ipynb           # Credit rating bucketing
├── task1.py                  # Natural gas price interpolation
├── task2.py                  # Storage contract valuation
└── README.md
```

## Tasks

### Task 1: Natural Gas Price Interpolation
Uses cubic spline interpolation to estimate natural gas prices for any date (past or future).

**Usage:**
```python
from task1 import get_price
price = get_price("2023-06-15")   # Past date (interpolation)
price = get_price("2025-03-01")   # Future date (extrapolation)
```

### Task 2: Storage Contract Valuation
Evaluates natural gas storage contracts by calculating the value of injection/withdrawal schedules.

**Usage:**
```python
from task2 import price_contract
value = price_contract(
    injection_dates=["2023-06-01", "2023-06-15"],
    withdrawal_dates=["2023-12-01", "2023-12-15"],
    injection_rate=1000,
    withdrawal_rate=1000,
    max_storage=5000,
    storage_cost_rate=10,
    get_price=get_price
)
```

### Task 3: Loan Default Prediction
Credit risk modeling using machine learning to predict loan defaults.

### Task 4: Credit Rating Bucketing
Optimal FICO score bucketing using log-likelihood optimization to maximize prediction accuracy.

