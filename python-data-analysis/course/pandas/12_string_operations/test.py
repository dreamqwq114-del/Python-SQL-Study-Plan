"""Pandas《Pandas 12：批量清理文本列》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType, Path], None]

def check_12_clean_text_fields(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"city": [" Suzhou ", None], "contract_type": [" Monthly ", None]}
    )
    original = source.copy()
    result = module.clean_text_fields(source)
    assert result.loc[0, "city"] == "suzhou"
    assert result.loc[0, "contract_type"] == "Monthly"
    assert pd.isna(result.loc[1, "city"])
    pd.testing.assert_frame_equal(source, original)

def check_12_filter_products_by_keyword(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"product_name": ["USB Cable", "Phone Case", "Mouse", None]}
    )
    result = module.filter_products_by_keyword(source, "CASE")
    assert result["product_name"].tolist() == ["Phone Case"]
    result_literal = module.filter_products_by_keyword(source, ".")
    assert result_literal.empty
    assert len(module.filter_products_by_keyword(source, "")) == 3

def check_12_add_product_key(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"product_name": [" USB Cable ", "Phone   Case", None]}
    )
    result = module.add_product_key(source)
    assert result["product_key"].iloc[:2].tolist() == [
        "usb_cable",
        "phone_case",
    ]
    assert pd.isna(result.loc[2, "product_key"])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_12_clean_text_fields", answer, check_12_clean_text_fields),
    ("answer_12_filter_products_by_keyword", answer, check_12_filter_products_by_keyword),
    ("answer_12_add_product_key", answer, check_12_add_product_key),
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
