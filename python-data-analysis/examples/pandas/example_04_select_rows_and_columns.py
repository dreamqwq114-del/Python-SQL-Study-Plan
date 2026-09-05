"""使用 loc 和 iloc 选择客户表的数据块。"""

import pandas as pd

from utils.paths import DATA_DIR


def select_customer_report(dataframe: pd.DataFrame) -> pd.DataFrame:
    """返回前三位客户的编号、城市和消费。"""
    columns = ["customer_id", "city", "monthly_spending"]
    return dataframe.loc[:2, columns].copy()


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    report = select_customer_report(customers)
    print(report.to_dict("records"))
    print(customers.iloc[:2, :2].to_dict("records"))


if __name__ == "__main__":
    main()
