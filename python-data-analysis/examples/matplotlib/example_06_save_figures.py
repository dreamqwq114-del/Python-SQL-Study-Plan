"""把同一张图保存为 PNG 和 PDF，并关闭 Figure。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR


def save_city_formats(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> list[Path]:
    """把城市客户数图保存为 PNG 和 PDF。"""
    city = dataframe["city"].str.strip().str.lower()
    counts = city.value_counts().sort_index()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.bar(counts.index, counts.values)
    axis.set(
        title="Customers by City",
        xlabel="City",
        ylabel="Customer Count",
    )
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


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        paths = save_city_formats(customers, Path(directory))
        print([path.suffix for path in paths])
        print(all(path.exists() and path.stat().st_size > 0 for path in paths))
        print(len(plt.get_fignums()))


if __name__ == "__main__":
    main()
