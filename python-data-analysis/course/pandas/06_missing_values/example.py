"""统计缺失值并填充客户满意度。"""

import pandas as pd

from utils.paths import DATA_DIR


def fill_satisfaction(dataframe: pd.DataFrame) -> pd.DataFrame:
    """用满意度中位数填充缺失值。"""
    result = dataframe.copy()
    median_score = result["satisfaction_score"].median()
    result["satisfaction_score"] = result["satisfaction_score"].fillna(
        median_score
    )
    return result


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    cleaned = fill_satisfaction(customers)
    print(customers.isna().sum().to_dict())
    print(cleaned["satisfaction_score"].isna().sum())
    print(cleaned["satisfaction_score"].median())


if __name__ == "__main__":
    main()
