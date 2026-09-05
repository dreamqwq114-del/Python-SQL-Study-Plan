"""Python《08. 异常：让错误数据尽早停止》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_parse_positive_amount(module: ModuleType, tmp_path: Path) -> None:
    assert module.parse_positive_amount("12.5") == pytest.approx(12.5)
    assert module.parse_positive_amount(" 1 ") == pytest.approx(1.0)
    for invalid in ("0", "-1", "", "bad"):
        with pytest.raises(ValueError):
            module.parse_positive_amount(invalid)

def check_parse_optional_score(module: ModuleType, tmp_path: Path) -> None:
    assert module.parse_optional_score("88.5") == pytest.approx(88.5)
    assert module.parse_optional_score(" NA ") is None
    assert module.parse_optional_score("") is None
    assert module.parse_optional_score("0") == pytest.approx(0.0)
    assert module.parse_optional_score("100") == pytest.approx(100.0)
    for invalid in ("-1", "101", "bad"):
        with pytest.raises(ValueError):
            module.parse_optional_score(invalid)

def check_safe_divide(module: ModuleType, tmp_path: Path) -> None:
    assert module.safe_divide(10, 2) == pytest.approx(5.0)
    assert module.safe_divide(0, 5) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        module.safe_divide(10, 0)

def check_read_required_text(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "required.txt"
    path.write_text(" customer_id \n", encoding="utf-8")
    assert module.read_required_text(path) == "customer_id"
    empty = tmp_path / "blank.txt"
    empty.write_text(" \n", encoding="utf-8")
    with pytest.raises(ValueError):
        module.read_required_text(empty)
    with pytest.raises(ValueError):
        module.read_required_text(tmp_path / "missing.txt")

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_08_positive_amount", answer, check_parse_positive_amount),
    ("answer_08_optional_score", answer, check_parse_optional_score),
    ("answer_08_safe_divide", answer, check_safe_divide),
    ("answer_08_required_text", answer, check_read_required_text),
]

PRACTICE_CASES: list[tuple[str, ModuleType, Check]] = [
    (name.replace("answer_", "practice_"), practice, check)
    for name, _, check in ANSWER_CASES
]

@pytest.mark.parametrize(
    ("name", "module", "check"),
    ANSWER_CASES,
    ids=[case[0] for case in ANSWER_CASES],
)
def test_answer_contract(
    name: str,
    module: ModuleType,
    check: Check,
    tmp_path: Path,
) -> None:
    check(module, tmp_path)


@pytest.mark.parametrize(
    ("name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    name: str,
    module: ModuleType,
    check: Check,
    tmp_path: Path,
) -> None:
    try:
        check(module, tmp_path)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
