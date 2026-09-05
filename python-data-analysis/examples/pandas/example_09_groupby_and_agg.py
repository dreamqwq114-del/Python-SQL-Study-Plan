"""按城市汇总客户数量与平均消费。"""

import pandas as pd

from utils.paths import DATA_DIR


def summarize_by_city(dataframe: pd.DataFrame) -> pd.DataFrame:
    """清理城市和消费字段后生成城市汇总。"""
    result = dataframe.copy()
    result["city"] = result["city"].str.strip().str.lower()
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    return (
        result.groupby("city")
        .agg(
            customer_count=("customer_id", "nunique"),
            average_spending=("monthly_spending", "mean"),
        )
        .reset_index()
    )


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    summary = summarize_by_city(customers)
    print(summary.shape)
    print(summary.round(2).to_dict("records"))


if __name__ == "__main__":
    main()
