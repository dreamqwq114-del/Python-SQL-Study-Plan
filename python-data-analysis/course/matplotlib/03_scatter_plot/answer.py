"""第 3 节答案：散点图。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_age_spending(dataframe: pd.DataFrame, output_path: Path) -> None:
    points = pd.DataFrame(
        {
            "age": pd.to_numeric(dataframe["age"], errors="coerce"),
            "spending": pd.to_numeric(
                dataframe["monthly_spending"],
                errors="coerce",
            ),
        }
    ).dropna()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.scatter(points["age"], points["spending"])
    axis.set_title("Age vs Monthly Spending")
    axis.set_xlabel("Age")
    axis.set_ylabel("Monthly Spending")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_quantity_unit_price(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    quantities = dataframe["quantity"]
    prices = dataframe["unit_price"]
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.scatter(quantities, prices)
    axis.set_title("Quantity vs Unit Price")
    axis.set_xlabel("Quantity")
    axis.set_ylabel("Unit Price")
    axis.grid(alpha=0.3)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_income_spending_by_cluster(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    clusters = sorted(dataframe["cluster"].dropna().unique())
    incomes = dataframe["annual_income"]
    scores = dataframe["spending_score"]
    figure, axis = plt.subplots(figsize=(6, 4))
    for cluster in clusters:
        mask = dataframe["cluster"] == cluster
        axis.scatter(
            incomes.loc[mask],
            scores.loc[mask],
            label=f"Cluster {cluster}",
        )
    axis.set_title("Customer Segments")
    axis.set_xlabel("Annual Income")
    axis.set_ylabel("Spending Score")
    if clusters:
        axis.legend()
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
