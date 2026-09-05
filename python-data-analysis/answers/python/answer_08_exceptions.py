"""第八章四道练习的参考答案。"""

from pathlib import Path


def parse_positive_amount(text: str) -> float:
    """解析严格大于 0 的金额。"""
    amount = float(text)
    if amount <= 0:
        raise ValueError("金额必须大于 0")
    return amount


def parse_optional_score(text: str) -> float | None:
    """解析允许缺失的百分制成绩。"""
    cleaned = text.strip()
    if cleaned == "" or cleaned == "NA":
        return None
    score = float(cleaned)
    if score < 0 or score > 100:
        raise ValueError("成绩必须在 0 到 100 之间")
    return score


def safe_divide(numerator: float, denominator: float) -> float:
    """完成分母不为 0 的除法。"""
    if denominator == 0:
        raise ValueError("分母不能为 0")
    return numerator / denominator


def read_required_text(file_path: Path) -> str:
    """读取必须存在且非空的文本。"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ValueError("必需文件不存在") from error
    cleaned = content.strip()
    if cleaned == "":
        raise ValueError("必需文件不能为空")
    return cleaned
