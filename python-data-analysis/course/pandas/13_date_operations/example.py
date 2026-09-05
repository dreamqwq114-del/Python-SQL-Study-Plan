"""解析混合日期并按订单月份汇总金额。"""

import pandas as pd

from utils.paths import DATA_DIR


def monthly_order_totals(dataframe: pd.DataFrame) -> pd.DataFrame:
    """按月份汇总有效订单日期对应的金额。"""
    result = dataframe.copy()
    result["order_date"] = pd.to_datetime(
        result["order_date"],
        errors="coerce",
        format="mixed",
    )
    result["order_total"] = result["quantity"] * result["unit_price"]
    result = result.dropna(subset=["order_date"]).copy()
    result["order_month"] = result["order_date"].dt.strftime("%Y-%m")
    return (
        result.groupby("order_month", as_index=False)["order_total"]
        .sum()
        .sort_values("order_month")
    )


def main() -> None:
    orders = pd.read_csv(DATA_DIR / "sample_orders.csv")
    summary = monthly_order_totals(orders)
    print(summary.to_dict("records"))
    print(summary["order_total"].sum())


if __name__ == "__main__":
    main()
