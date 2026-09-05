"""Python 独立实践测评起始模板。

复制为 submission.py 后作答。本文件故意没有参考实现；不要把答案写回本模板。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "independent_readiness" / "output"


def load_sources(
    customer_path: Path, order_path: Path
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """读取两张 CSV，并验证各自必需列。"""
    # TODO: 读取 CSV；不要在这里清洗或修改数据。
    raise NotImplementedError("TODO: 实现 load_sources")


def build_customer_report(
    customers: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    """清洗、汇总并返回一行一客户的分析表。"""
    # TODO: 按 README 的数据契约完成清洗、Completed 订单汇总和左连接。
    raise NotImplementedError("TODO: 实现 build_customer_report")


def summarize_quality(
    raw_customers: pd.DataFrame,
    clean_report: pd.DataFrame,
    raw_orders: pd.DataFrame,
) -> dict[str, Any]:
    """返回可解释的数据质量摘要，不要只返回一个总数。"""
    # TODO: 至少返回 README 中列出的五个质量指标。
    raise NotImplementedError("TODO: 实现 summarize_quality")


def save_analysis_figure(report: pd.DataFrame, output_path: Path) -> None:
    """保存两个子图并确保 Figure 被关闭。"""
    # TODO: 绘图、创建父目录、保存 PNG，并在成功或失败后关闭 Figure。
    raise NotImplementedError("TODO: 实现 save_analysis_figure")


def main() -> None:
    customers, orders = load_sources(
        DATA_DIR / "sample_customers.csv",
        DATA_DIR / "sample_orders.csv",
    )
    report = build_customer_report(customers, orders)
    quality = summarize_quality(customers, report, orders)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT_DIR / "customer_report.csv", index=False)
    save_analysis_figure(report, OUTPUT_DIR / "customer_analysis.png")
    print(report.head().to_string(index=False))
    print(quality)


if __name__ == "__main__":
    main()

