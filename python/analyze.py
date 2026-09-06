"""Reproducible exploratory analysis for the Superstore SQLite database."""

from argparse import ArgumentParser
from pathlib import Path
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def normalise_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = (
        frame.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return frame


def load_data(database: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    with sqlite3.connect(database) as connection:
        orders = pd.read_sql_query("SELECT * FROM orders", connection)
        returns = pd.read_sql_query("SELECT * FROM returns", connection)
        people = pd.read_sql_query("SELECT * FROM people", connection)
    return tuple(map(normalise_columns, (orders, returns, people)))


def prepare_orders(
    orders: pd.DataFrame, returns: pd.DataFrame, people: pd.DataFrame
) -> pd.DataFrame:
    orders["returned"] = orders["order_id"].isin(returns["order_id"]).astype(int)
    orders = orders.merge(people, on="region", how="left")
    date_column = "orderdate_clean" if "orderdate_clean" in orders else "order_date"
    orders["order_date_clean"] = pd.to_datetime(orders[date_column], errors="coerce")
    for column in ["sales", "profit", "quantity", "discount"]:
        orders[column] = pd.to_numeric(orders[column], errors="coerce")
    return orders.dropna(subset=["order_date_clean", "sales"])


def save_heatmap(orders: pd.DataFrame, output_dir: Path) -> None:
    columns = ["sales", "profit", "quantity", "discount", "returned"]
    correlation = orders[columns].corr()
    plt.figure(figsize=(9, 7))
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap="Blues", center=0)
    plt.title("Superstore Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(output_dir / "correlation_heatmap.png", dpi=200)
    plt.close()


def save_outlier_plot(orders: pd.DataFrame, output_dir: Path) -> None:
    plt.figure(figsize=(9, 4))
    sns.boxplot(x=orders["profit"])
    plt.title("Profit Distribution and Outliers")
    plt.xlabel("Profit")
    plt.tight_layout()
    plt.savefig(output_dir / "profit_outliers.png", dpi=200)
    plt.close()


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--database", type=Path, default=Path("data/superstore.db"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    orders, returns, people = load_data(args.database)
    prepared = prepare_orders(orders, returns, people)
    save_heatmap(prepared, args.output_dir)
    save_outlier_plot(prepared, args.output_dir)
    print(f"Analysed {len(prepared):,} order rows.")


if __name__ == "__main__":
    main()
