"""用 Series 和 DataFrame 表示订单数量与客户记录。"""

import pandas as pd


def create_customer_data() -> tuple[pd.Series, pd.DataFrame]:
    """创建订单数量 Series 和客户 DataFrame。"""
    quantities = pd.Series(
        [1, 2, 3],
        index=["O001", "O002", "O003"],
        name="quantity",
    )
    customers = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "city": ["Suzhou", "Shanghai"],
            "monthly_spending": [188.5, 420.0],
        }
    )
    return quantities, customers


def main() -> None:
    quantities, customers = create_customer_data()
    print(quantities.to_dict())
    print(customers.to_dict("records"))
    print(customers.shape)


if __name__ == "__main__":
    main()
