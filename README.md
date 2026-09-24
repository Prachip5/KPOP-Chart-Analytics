# K-POP Chart Analytics — Final Notebook Package

## Main notebook
`KPOP_Chart_Analytics_Final.ipynb`

The notebook is built from the supplied main dataset and executes end-to-end.

## Dataset
`KPOP_Main_Dataset.csv`

## Run
1. Open the project folder in Jupyter Notebook / JupyterLab.
2. Open `KPOP_Chart_Analytics_Final.ipynb`.
3. Select Python 3.
4. Use **Kernel → Restart Kernel and Run All**.
5. The notebook creates an `outputs/` folder automatically.

## Cleaning rule for the supplied data
The supplied dataset contains:
- 27,800 raw rows
- 16 exact duplicate rows
- one date (`2025-03-01`) with 100 records instead of 50
- remaining duplicate date-position records on that date

The notebook removes exact duplicates, then keeps the first source record for duplicate date-position pairs, and validates that the cleaned dataset has exactly 50 rows for every chart date.

## Main analytical outputs
- chart re-entry events
- comeback momentum
- fandom intensity
- sustainability
- artist sustainability
- integrated performance
- dashboard-ready song data
- dashboard-ready all-song data
- album-cover URLs
- KPI export
