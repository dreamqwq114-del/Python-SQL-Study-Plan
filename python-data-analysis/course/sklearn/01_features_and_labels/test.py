"""scikit-learn《第 1 节：把客户表拆成特征 X 和标签 y》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_01_select_features_and_label(module: ModuleType) -> None:
    source = pd.DataFrame(
        {
            "city": ["A", "B"],
            "churn": [0, 1],
            "monthly_spending": [100.0, 150.0],
            "age": [20, 30],
        }
    )
    original = source.copy()
    X, y = module.select_features_and_label(source)
    assert X.columns.tolist() == ["age", "monthly_spending"]
    assert y.tolist() == [0, 1]
    X.loc[0, "age"] = 99
    y.loc[0] = 1
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.select_features_and_label(source.drop(columns="age"))

def check_01_select_mixed_features(module: ModuleType) -> None:
    source = pd.DataFrame(
        {
            "age": [20, 30],
            "monthly_spending": [100.0, 150.0],
            "city": ["A", "B"],
            "churn": [0, 1],
        }
    )
    X, y = module.select_mixed_features(source)
    assert X.columns.tolist() == ["age", "monthly_spending", "city"]
    assert X["city"].tolist() == ["A", "B"]
    assert y.name == "churn"

def check_01_count_target_classes(module: ModuleType) -> None:
    assert module.count_target_classes(pd.Series([0, 1, 0])) == {0: 2, 1: 1}
    assert module.count_target_classes(pd.Series([0, 0])) == {0: 2, 1: 0}
    assert module.count_target_classes(pd.Series([], dtype=int)) == {0: 0, 1: 0}
    with pytest.raises(ValueError):
        module.count_target_classes(pd.Series([0, 2]))
    with pytest.raises(ValueError):
        module.count_target_classes(pd.Series([0, None]))

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_select_features_and_label", answer, check_01_select_features_and_label),
    ("answer_01_select_mixed_features", answer, check_01_select_mixed_features),
    ("answer_01_count_target_classes", answer, check_01_count_target_classes),
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
) -> None:
    check(module)


@pytest.mark.parametrize(
    ("name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    name: str,
    module: ModuleType,
    check: Check,
) -> None:
    try:
        check(module)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
