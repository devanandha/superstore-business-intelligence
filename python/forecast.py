"""Create a transparent six-month linear-trend sales forecast."""

from argparse import ArgumentParser
from pathlib import Path
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--database", type=Path, default=Path("data/superstore.db"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(args.database) as connection:
        orders = pd.read_sql_query('SELECT "Order Date", Sales FROM orders', connection)

    orders["Order Date"] = pd.to_datetime(
        orders["Order Date"], format="%m-%d-%y", errors="coerce"
    )
    orders["Sales"] = pd.to_numeric(orders["Sales"], errors="coerce")
    orders = orders.dropna()
    monthly = orders.set_index("Order Date")["Sales"].resample("ME").sum()

    x = np.arange(len(monthly), dtype=float)
    trend = np.poly1d(np.polyfit(x, monthly.to_numpy(dtype=float), 1))
    horizon = 6
    future_dates = pd.date_range(
        monthly.index[-1] + pd.offsets.MonthEnd(1), periods=horizon, freq="ME"
    )
    forecast = pd.Series(trend(np.arange(len(monthly), len(monthly) + horizon)), index=future_dates)

    plt.figure(figsize=(11, 5))
    plt.plot(monthly.index, monthly.values, label="Historical monthly sales")
    plt.plot(forecast.index, forecast.values, "--", label="Linear-trend forecast")
    plt.title("Superstore Sales: Six-Month Trend Forecast")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output_dir / "sales_forecast.png", dpi=200)
    plt.close()

    forecast.rename("forecast_sales").to_csv(args.output_dir / "forecast_values.csv")
    print(f"Generated a {horizon}-month illustrative trend forecast.")


if __name__ == "__main__":
    main()
