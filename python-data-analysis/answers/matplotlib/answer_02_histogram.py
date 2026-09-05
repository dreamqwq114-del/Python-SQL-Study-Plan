"""第 2 节答案：直方图。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_age_histogram(dataframe: pd.DataFrame, output_path: Path) -> None:
    ages = pd.to_numeric(dataframe["age"], errors="coerce").dropna()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.hist(ages, bins=5, edgecolor="black")
    axis.set_title("Customer Age Distribution")
    axis.set_xlabel("Age")
    axis.set_ylabel("Customer Count")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_spending_histogram(
    dataframe: pd.DataFrame,
    output_path: Path,
    bins: int,
) -> None:
    if bins <= 0:
        raise ValueError("bins 必须大于 0")
    spending = pd.to_numeric(
        dataframe["monthly_spending"],
        errors="coerce",
    ).dropna()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.hist(spending, bins=bins, edgecolor="black")
    axis.set_title("Monthly Spending Distribution")
    axis.set_xlabel("Monthly Spending")
    axis.set_ylabel("Customer Count")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_age_histograms_by_churn(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    ages = pd.to_numeric(dataframe["age"], errors="coerce")
    stayed = ages.loc[dataframe["churn"] == 0].dropna()
    churned = ages.loc[dataframe["churn"] == 1].dropna()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.hist(stayed, bins=5, alpha=0.6, label="Stayed")
    axis.hist(churned, bins=5, alpha=0.6, label="Churned")
    axis.set_title("Age Distribution by Churn")
    axis.set_xlabel("Age")
    axis.set_ylabel("Customer Count")
    axis.legend()
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
