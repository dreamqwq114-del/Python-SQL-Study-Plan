"""统一城市、性别和商品名称文本。"""

import pandas as pd

from utils.paths import DATA_DIR


def clean_customer_text(dataframe: pd.DataFrame) -> pd.DataFrame:
    """去除空格并统一城市和性别的大小写。"""
    result = dataframe.copy()
    result["city"] = result["city"].str.strip().str.lower()
    result["gender"] = result["gender"].str.strip().str.lower()
    return result


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    orders = pd.read_csv(DATA_DIR / "sample_orders.csv")
    cleaned = clean_customer_text(customers)
    usb_orders = orders.loc[
        orders["product_name"].str.contains(
            "usb",
            case=False,
            na=False,
            regex=False,
        )
    ]
    print(sorted(cleaned["city"].dropna().unique().tolist()))
    print(sorted(cleaned["gender"].dropna().unique().tolist()))
    print(usb_orders["product_name"].tolist())


if __name__ == "__main__":
    main()
