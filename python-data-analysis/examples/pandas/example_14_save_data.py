"""把客户城市汇总保存为 CSV 并重新读取验证。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from utils.paths import DATA_DIR


def save_city_summary(dataframe: pd.DataFrame, path: Path) -> None:
    """生成城市客户数汇总并保存为 UTF-8 CSV。"""
    summary = (
        dataframe.assign(city=dataframe["city"].str.strip().str.lower())
        .groupby("city")
        .size()
        .reset_index(name="customer_count")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False, encoding="utf-8")


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "reports" / "city_summary.csv"
        save_city_summary(customers, target)
        reloaded = pd.read_csv(target)
        print(target.exists())
        print(reloaded.shape)
        print(reloaded.to_dict("records"))


if __name__ == "__main__":
    main()
