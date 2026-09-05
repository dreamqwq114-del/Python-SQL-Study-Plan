"""绘制客户年龄与月消费散点图。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR


def save_age_spending_scatter(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> int:
    """保存散点图并返回有效数据对数量。"""
    points = pd.DataFrame(
        {
            "age": pd.to_numeric(dataframe["age"], errors="coerce"),
            "spending": pd.to_numeric(
                dataframe["monthly_spending"],
                errors="coerce",
            ),
        }
    ).dropna()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.scatter(points["age"], points["spending"], alpha=0.7)
    axis.set(
        title="Age vs Monthly Spending",
        xlabel="Age",
        ylabel="Monthly Spending",
    )
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    return len(points)


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "age_spending.png"
        valid_pairs = save_age_spending_scatter(customers, target)
        print(valid_pairs)
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))


if __name__ == "__main__":
    main()
