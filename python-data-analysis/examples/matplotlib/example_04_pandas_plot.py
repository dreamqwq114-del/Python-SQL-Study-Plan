"""先用 pandas 聚合，再通过 pandas 绘图入口保存柱状图。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR


def save_city_average_plot(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> pd.Series:
    """保存城市平均消费图并返回聚合结果。"""
    result = dataframe.copy()
    result["city"] = result["city"].str.strip().str.lower()
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    summary = (
        result.groupby("city")["monthly_spending"]
        .mean()
        .sort_index()
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 4))
    summary.plot.bar(ax=axis)
    axis.set(
        title="Average Spending by City",
        xlabel="City",
        ylabel="Average Monthly Spending",
    )
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    return summary


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "city_average.png"
        summary = save_city_average_plot(customers, target)
        print(summary.round(2).to_dict())
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))


if __name__ == "__main__":
    main()
