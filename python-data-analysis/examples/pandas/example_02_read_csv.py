"""从项目 data 目录读取客户 CSV。"""

from pathlib import Path

import pandas as pd

from utils.paths import DATA_DIR


def load_customer_columns(path: Path) -> pd.DataFrame:
    """读取分析需要的客户列。"""
    columns = ["customer_id", "city", "monthly_spending", "churn"]
    return pd.read_csv(path, usecols=columns, encoding="utf-8")


def main() -> None:
    customers = load_customer_columns(DATA_DIR / "sample_customers.csv")
    print(customers.shape)
    print(customers.columns.tolist())
    print(customers.head(2).to_dict("records"))


if __name__ == "__main__":
    main()
