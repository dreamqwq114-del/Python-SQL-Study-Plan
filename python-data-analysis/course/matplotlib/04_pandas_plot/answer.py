"""第 4 节答案：Pandas 绘图入口。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_city_average(dataframe: pd.DataFrame, output_path: Path) -> None:
    summary = (
        dataframe.groupby("city")["monthly_spending"]
        .mean()
        .sort_index()
    )
    figure, axis = plt.subplots(figsize=(6, 4))
    summary.plot.bar(ax=axis)
    axis.set_title("Average Spending by City")
    axis.set_xlabel("City")
    axis.set_ylabel("Average Monthly Spending")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_contract_churn_rate(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    summary = (
        dataframe.groupby("contract_type")["churn"]
        .mean()
        .sort_values(ascending=False)
    )
    figure, axis = plt.subplots(figsize=(6, 4))
    summary.plot.bar(ax=axis)
    axis.set_title("Churn Rate by Contract")
    axis.set_xlabel("Contract Type")
    axis.set_ylabel("Churn Rate")
    axis.set_ylim(0, 1)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_monthly_order_totals(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    result = dataframe.copy()
    result["order_date"] = pd.to_datetime(
        result["order_date"],
        errors="coerce",
        format="mixed",
    )
    result["order_total"] = result["quantity"] * result["unit_price"]
    result = result.dropna(subset=["order_date"]).copy()
    result["order_month"] = result["order_date"].dt.strftime("%Y-%m")
    summary = (
        result.groupby("order_month")["order_total"]
        .sum()
        .sort_index()
    )
    figure, axis = plt.subplots(figsize=(6, 4))
    if summary.empty:
        axis.plot([], [], marker="o")
    else:
        summary.plot(ax=axis, marker="o")
    axis.set_title("Monthly Order Totals")
    axis.set_xlabel("Month")
    axis.set_ylabel("Order Total")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
