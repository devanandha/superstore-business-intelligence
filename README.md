# End-to-End Superstore Business Intelligence Solution

An end-to-end portfolio project demonstrating how sales data can move from ETL and storage through analysis, forecasting and interactive reporting.

## Project overview

The solution combines:

- **SSIS** for extracting, cleaning and loading order data
- **SQLite and SQL** for storage, validation and KPI analysis
- **Python** for exploratory analysis, correlation analysis and an illustrative sales forecast
- **Power BI** for interactive reporting and stakeholder-facing insights

## Key findings

- The dataset contains **9,994 order-line records**, **5,009 orders** and **793 customers** between 2014 and 2017.
- Total recorded sales were approximately **2.30 million**, with profit of approximately **286,397**.
- **Technology** generated the highest sales of the three categories.
- **Technology** also showed the highest return rate in the Power BI analysis, highlighting a commercial risk behind the strong revenue result.
- Profit was strongest in the **West** region.
- Discount had a negative relationship with profit, while sales and profit were positively correlated.

These findings are descriptive results from a sample dataset and should not be interpreted as production forecasts or causal conclusions.

## Repository structure

```text
data/       Source CSV files and SQLite database
etl/        Sanitised SSIS package and setup guidance
sql/        Clean, reproducible KPI queries
python/     Analysis and forecasting scripts
powerbi/    Power BI dashboard
outputs/    Generated charts and forecast values
docs/       Supporting screenshots
```

## Run the Python analysis

```bash
python -m venv .venv
```

On Windows:

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
python python/analyze.py
python python/forecast.py
```

The generated files are written to `outputs/`.

## Evaluation notes

The six-month forecast is a transparent linear-trend baseline. It demonstrates the forecasting workflow but does not model seasonality, uncertainty or external drivers. A production version should use time-aware validation and compare multiple forecasting methods.

The row-level return calculation differs from an order-level or dashboard-filtered return measure. The metric definition should therefore be stated whenever results are reported.

## Tools

Python, pandas, NumPy, Matplotlib, Seaborn, SQLite, SQL, SSIS and Power BI.

## Author

Devanandha VS
