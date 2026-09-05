"""scikit-learn《第 7 节：让多棵树组成随机森林》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import pytest

from .._helpers import tiny_classification
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_07_train_forest(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_forest(X, y)
    assert model.n_estimators == 50
    assert model.random_state == 42
    assert len(model.estimators_) == 50

def check_07_train_forest_with_estimators(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_forest_with_estimators(X, y, 10)
    assert model.n_estimators == 10
    assert len(model.estimators_) == 10
    with pytest.raises(ValueError):
        module.train_forest_with_estimators(X, y, 0)

def check_07_forest_importance_table(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_forest(X, y)
    result = module.forest_importance_table(model, ["a", "b", "c"])
    assert result.shape == (3, 2)
    assert result["importance"].is_monotonic_decreasing
    assert result["importance"].sum() == pytest.approx(1.0)
    with pytest.raises(ValueError):
        module.forest_importance_table(model, ["a"])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_07_train_forest", answer, check_07_train_forest),
    ("answer_07_train_forest_with_estimators", answer, check_07_train_forest_with_estimators),
    ("answer_07_forest_importance_table", answer, check_07_forest_importance_table),
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
