"""排序客户并计算消费统计。"""

import pandas as pd

from utils.paths import DATA_DIR


def prepare_spending_report(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """返回高消费客户和三项消费统计。"""
    result = dataframe.copy()
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    result = result.sort_values(
        "monthly_spending",
        ascending=False,
    )
    spending = result["monthly_spending"]
    statistics = {
        "mean": round(float(spending.mean()), 2),
        "median": round(float(spending.median()), 2),
        "max": round(float(spending.max()), 2),
    }
    return result.head(3), statistics


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    top_customers, statistics = prepare_spending_report(customers)
    print(top_customers["customer_id"].tolist())
    print(top_customers["monthly_spending"].tolist())
    print(statistics)


if __name__ == "__main__":
    main()
