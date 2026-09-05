"""用完整标题、轴标签、图例和布局绘制订单状态折线。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR


def save_status_lines(dataframe: pd.DataFrame, output_path: Path) -> list[str]:
    """保存订单状态折线并返回图例标签。"""
    result = dataframe.copy()
    result["order_amount"] = result["quantity"] * result["unit_price"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(7, 4))
    labels = []
    for status, group in result.groupby("order_status", sort=True):
        labels.append(str(status))
        axis.plot(
            range(1, len(group) + 1),
            group["order_amount"],
            marker="o",
            label=str(status),
        )
    axis.set(
        title="Order Amount by Status",
        xlabel="Order Sequence",
        ylabel="Order Amount",
    )
    axis.legend()
    axis.grid(alpha=0.3)
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    return labels


def main() -> None:
    orders = pd.read_csv(DATA_DIR / "sample_orders.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "status_lines.png"
        labels = save_status_lines(orders, target)
        print(labels)
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))


if __name__ == "__main__":
    main()
