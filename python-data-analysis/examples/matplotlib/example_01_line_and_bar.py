"""在两个子图中展示销售趋势和城市客户数量。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def create_sales_dashboard(
    sales: pd.DataFrame,
    customers: pd.DataFrame,
    output_path: Path,
) -> None:
    """创建折线图与柱状图组成的报告。"""
    ordered = sales.sort_values("month")
    city_counts = customers["city"].value_counts().sort_index()
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(ordered["month"], ordered["sales"], marker="o")
    axes[0].set(
        title="Monthly Sales",
        xlabel="Month",
        ylabel="Sales",
    )
    axes[1].bar(city_counts.index, city_counts.values)
    axes[1].set(
        title="Customers by City",
        xlabel="City",
        ylabel="Customer Count",
    )
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)


def main() -> None:
    sales = pd.DataFrame(
        {"month": [3, 1, 2], "sales": [135, 120, 150]}
    )
    customers = pd.DataFrame({"city": ["Suzhou", "Wuxi", "Suzhou"]})
    with TemporaryDirectory() as directory:
        target = Path(directory) / "line_and_bar.png"
        create_sales_dashboard(sales, customers, target)
        print(target.name)
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))


if __name__ == "__main__":
    main()
