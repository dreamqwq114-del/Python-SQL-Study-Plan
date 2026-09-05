"""第 1 节答案：折线图与柱状图。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_city_counts(dataframe: pd.DataFrame, output_path: Path) -> None:
    counts = dataframe["city"].value_counts().sort_index()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.bar(counts.index.astype(str), counts.values)
    axis.set_title("Customers by City")
    axis.set_xlabel("City")
    axis.set_ylabel("Customer Count")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_monthly_sales(dataframe: pd.DataFrame, output_path: Path) -> None:
    ordered = dataframe.sort_values("month")
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.plot(ordered["month"], ordered["sales"], marker="o")
    axis.set_title("Monthly Sales Trend")
    axis.set_xlabel("Month")
    axis.set_ylabel("Sales")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_sales_and_city_counts(
    sales: pd.DataFrame,
    customers: pd.DataFrame,
    output_path: Path,
) -> None:
    ordered = sales.sort_values("month")
    counts = customers["city"].value_counts().sort_index()
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(ordered["month"], ordered["sales"], marker="o")
    axes[0].set_title("Monthly Sales")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Sales")
    axes[1].bar(counts.index.astype(str), counts.values)
    axes[1].set_title("Customers by City")
    axes[1].set_xlabel("City")
    axes[1].set_ylabel("Customer Count")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
