"""连接客户与订单，并拼接订单批次。"""

import pandas as pd

from utils.paths import DATA_DIR


def merge_customer_orders(
    customers: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    """按 customer_id 左连接客户与订单。"""
    unique_customers = customers.drop_duplicates("customer_id")
    return unique_customers.merge(
        orders,
        on="customer_id",
        how="left",
        validate="one_to_many",
    )


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    orders = pd.read_csv(DATA_DIR / "sample_orders.csv")
    merged = merge_customer_orders(customers, orders)
    combined = pd.concat([orders.head(2), orders.tail(2)], ignore_index=True)
    print((customers.shape, orders.shape, merged.shape))
    print(merged[["customer_id", "order_id"]].head(4).to_dict("records"))
    print(combined["order_id"].tolist())


if __name__ == "__main__":
    main()
