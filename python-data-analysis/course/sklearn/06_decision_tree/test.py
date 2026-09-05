"""scikit-learn《第 6 节：用决策树学习判断规则》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
from sklearn.exceptions import NotFittedError
from sklearn.tree import DecisionTreeClassifier
import pytest

from .._helpers import tiny_classification
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_06_train_tree(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_tree(X, y)
    assert model.max_depth == 3
    assert model.random_state == 42
    assert hasattr(model, "tree_")

def check_06_train_tree_with_depth(module: ModuleType) -> None:
    X, y = tiny_classification()
    assert module.train_tree_with_depth(X, y, 1).max_depth == 1
    assert module.train_tree_with_depth(X, y, 5).max_depth == 5
    with pytest.raises(ValueError):
        module.train_tree_with_depth(X, y, 0)

def check_06_tree_importance_table(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    ).fit(X, y)
    result = module.tree_importance_table(model, ["a", "b", "c"])
    assert result.shape == (3, 2)
    assert result["importance"].is_monotonic_decreasing
    assert result["importance"].sum() == pytest.approx(1.0)
    with pytest.raises(ValueError):
        module.tree_importance_table(model, ["a"])
    with pytest.raises(NotFittedError):
        module.tree_importance_table(DecisionTreeClassifier(), ["a", "b", "c"])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_06_train_tree", answer, check_06_train_tree),
    ("answer_06_train_tree_with_depth", answer, check_06_train_tree_with_depth),
    ("answer_06_tree_importance_table", answer, check_06_tree_importance_table),
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
