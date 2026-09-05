"""绘制客户年龄分布直方图。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR


def save_age_histogram(dataframe: pd.DataFrame, output_path: Path) -> int:
    """保存年龄直方图并返回有效年龄数量。"""
    ages = pd.to_numeric(dataframe["age"], errors="coerce").dropna()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.hist(ages, bins=6, edgecolor="black")
    axis.set(
        title="Customer Age Distribution",
        xlabel="Age",
        ylabel="Customer Count",
    )
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    return len(ages)


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "age_histogram.png"
        valid_count = save_age_histogram(customers, target)
        print(valid_count)
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))


if __name__ == "__main__":
    main()
