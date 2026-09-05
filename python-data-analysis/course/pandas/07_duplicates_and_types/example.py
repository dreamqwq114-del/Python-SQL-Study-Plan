"""按客户编号去重并修正消费金额类型。"""

import pandas as pd

from utils.paths import DATA_DIR


def clean_customer_types(dataframe: pd.DataFrame) -> pd.DataFrame:
    """去除重复客户，并把消费金额安全转换为数字。"""
    result = dataframe.drop_duplicates(
        subset="customer_id",
        keep="first",
    ).copy()
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    return result.reset_index(drop=True)


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    cleaned = clean_customer_types(customers)
    print((customers.shape, cleaned.shape))
    print(str(cleaned["monthly_spending"].dtype))
    print(cleaned["monthly_spending"].isna().sum())


if __name__ == "__main__":
    main()
