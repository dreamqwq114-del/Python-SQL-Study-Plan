"""scikit-learn《第 2 节：划分训练集和测试集》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_02_split_data(module: ModuleType) -> None:
    X = pd.DataFrame({"x": range(40)})
    y = pd.Series([0, 1] * 20)
    result = module.split_data(X, y)
    X_train, X_test, y_train, y_test = result
    assert (len(X_train), len(X_test)) == (30, 10)
    assert y_train.mean() == pytest.approx(0.5)
    assert y_test.mean() == pytest.approx(0.5)
    repeated = module.split_data(X, y)
    pd.testing.assert_frame_equal(X_train, repeated[0])
    pd.testing.assert_frame_equal(X_test, repeated[1])

def check_02_split_with_test_size(module: ModuleType) -> None:
    X = pd.DataFrame({"x": range(20)})
    y = pd.Series([0, 1] * 10)
    assert len(module.split_with_test_size(X, y, 0.2)[1]) == 4
    assert len(module.split_with_test_size(X, y, 0.5)[1]) == 10
    with pytest.raises(ValueError):
        module.split_with_test_size(X, y, 0)
    with pytest.raises(ValueError):
        module.split_with_test_size(X, y, 1)

def check_02_summarize_split_balance(module: ModuleType) -> None:
    result = module.summarize_split_balance(
        pd.Series([0, 1]),
        pd.Series([0, 1, 1, 0]),
    )
    assert result == {
        "train_positive_rate": 0.5,
        "test_positive_rate": 0.5,
    }
    with pytest.raises(ValueError):
        module.summarize_split_balance(
            pd.Series([], dtype=int),
            pd.Series([0, 1]),
        )

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_02_split_data", answer, check_02_split_data),
    ("answer_02_split_with_test_size", answer, check_02_split_with_test_size),
    ("answer_02_summarize_split_balance", answer, check_02_summarize_split_balance),
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
