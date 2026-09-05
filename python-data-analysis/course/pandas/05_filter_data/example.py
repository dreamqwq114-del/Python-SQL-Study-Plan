"""筛选指定年龄、城市与流失状态的客户。"""

import pandas as pd

from utils.paths import DATA_DIR


def select_retention_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """筛选 25 至 45 岁、苏州或上海、已流失的客户。"""
    city = dataframe["city"].str.strip().str.lower()
    mask = (
        dataframe["age"].between(25, 45)
        & city.isin(["suzhou", "shanghai"])
        & (dataframe["churn"] == "Yes")
    )
    return dataframe.loc[mask].copy()


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    selected = select_retention_customers(customers)
    print(selected.shape)
    print(selected["customer_id"].tolist())
    print(selected[["age", "city", "churn"]].to_dict("records"))


if __name__ == "__main__":
    main()
