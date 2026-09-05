"""检查客户表的行列、类型与类别数量。"""

import pandas as pd

from utils.paths import DATA_DIR


def inspect_customers(dataframe: pd.DataFrame) -> dict[str, object]:
    """返回客户表的结构摘要。"""
    return {
        "rows": dataframe.shape[0],
        "columns": dataframe.shape[1],
        "column_names": dataframe.columns.tolist(),
        "city_counts": dataframe["city"].value_counts().head(3).to_dict(),
    }


def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    print(customers.head(3).to_dict("records"))
    print(inspect_customers(customers))


if __name__ == "__main__":
    main()
