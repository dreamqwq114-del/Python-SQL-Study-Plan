"""用 map、replace 和 apply 转换客户字段。"""

import pandas as pd

from utils.paths import DATA_DIR


def transform_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """添加流失标签、合同简称、年消费和客户编号长度。"""
    result = dataframe.copy()
    result["churn_label"] = result["churn"].map(
        {"No": "Stayed", "Yes": "Churned"}
    )
    result["contract_type"] = result["contract_type"].replace(
        {"Two-year": "Long-term"}
    )
    spending = pd.to_numeric(result["monthly_spending"], errors="coerce")
    result["annual_spending"] = spending * 12
    result["id_length"] = result["customer_id"].apply(len)
    return result


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    transformed = transform_customers(customers)
    columns = [
        "customer_id",
        "churn_label",
        "contract_type",
        "annual_spending",
        "id_length",
    ]
    print(transformed[columns].head(3).to_dict("records"))


if __name__ == "__main__":
    main()
