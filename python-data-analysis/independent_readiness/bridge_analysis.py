"""Python–SQL 桥接任务起始模板。

将 SQL 端导出的 project_analysis.csv 放入本目录后，复制本文件为 submission_bridge.py 作答。
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "project_id",
    "project_name",
    "department_name",
    "project_status",
    "budget",
    "participant_count",
    "total_working_hours",
}


def load_project_export(path: Path) -> pd.DataFrame:
    """读取 SQL 导出的项目分析结果并检查列契约。"""
    # TODO: 读取 CSV、验证列和关键数值字段，不要去重掩盖 SQL 重复。
    raise NotImplementedError("TODO: 实现 load_project_export")


def compare_python_summary(projects: pd.DataFrame) -> pd.DataFrame:
    """生成按项目状态的 Python 汇总，供与 SQL 结果核对。"""
    # TODO: 返回 project_status、project_count、total_budget 等可解释字段。
    raise NotImplementedError("TODO: 实现 compare_python_summary")


def main() -> None:
    projects = load_project_export(Path(__file__).with_name("project_analysis.csv"))
    summary = compare_python_summary(projects)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

