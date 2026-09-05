"""第 5 节答案：标题、图例与布局。"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_order_status_lines(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    grouped = list(dataframe.groupby("status", sort=True))
    dataframe["order_amount"]
    figure, axis = plt.subplots(figsize=(6, 4))
    for status, group in grouped:
        positions = range(1, len(group) + 1)
        axis.plot(
            positions,
            group["order_amount"],
            marker="o",
            label=str(status),
        )
    axis.set_title("Order Amount by Status")
    axis.set_xlabel("Order Sequence")
    axis.set_ylabel("Order Amount")
    if axis.lines:
        axis.legend()
    axis.grid(alpha=0.3)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_online_and_store_sales(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    ordered = dataframe.sort_values("month")
    online_sales = ordered["online_sales"]
    store_sales = ordered["store_sales"]
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.plot(
        ordered["month"],
        online_sales,
        marker="o",
        label="Online",
    )
    axis.plot(
        ordered["month"],
        store_sales,
        marker="o",
        label="Store",
    )
    axis.set_title("Sales by Channel")
    axis.set_xlabel("Month")
    axis.set_ylabel("Sales")
    axis.legend()
    axis.grid(alpha=0.3)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def plot_customer_dashboard(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    city_counts = dataframe["city"].value_counts().sort_index()
    churn_counts = dataframe["churn"].value_counts().sort_index()
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].bar(city_counts.index.astype(str), city_counts.values)
    axes[0].set_title("Customers by City")
    axes[0].set_xlabel("City")
    axes[0].set_ylabel("Customer Count")
    axes[1].bar(churn_counts.index.astype(str), churn_counts.values)
    axes[1].set_title("Customers by Churn")
    axes[1].set_xlabel("Churn")
    axes[1].set_ylabel("Customer Count")
    figure.suptitle("Customer Overview")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
