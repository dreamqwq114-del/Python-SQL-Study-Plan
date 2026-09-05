"""第 6 节答案：保存并关闭图像。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_churn_figure(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    counts = dataframe["churn"].value_counts().sort_index()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.bar(counts.index.astype(str), counts.values)
    axis.set_title("Churn Category Distribution")
    axis.set_xlabel("Churn")
    axis.set_ylabel("Customer Count")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)


def save_transparent_spending_scatter(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    ages = dataframe["age"]
    spending = dataframe["monthly_spending"]
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.scatter(ages, spending)
    axis.set_title("Spending by Age")
    axis.set_xlabel("Age")
    axis.set_ylabel("Monthly Spending")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_path,
        dpi=200,
        transparent=True,
        bbox_inches="tight",
    )
    plt.close(figure)


def save_city_figure_formats(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> list[Path]:
    counts = dataframe["city"].value_counts().sort_index()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.bar(counts.index.astype(str), counts.values)
    axis.set_title("Customers by City")
    axis.set_xlabel("City")
    axis.set_ylabel("Customer Count")
    figure.tight_layout()
    output_directory.mkdir(parents=True, exist_ok=True)
    paths = [
        output_directory / "city_counts.png",
        output_directory / "city_counts.pdf",
    ]
    for path in paths:
        figure.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    return paths
