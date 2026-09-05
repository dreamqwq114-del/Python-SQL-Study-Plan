"""scikit-learn《第 5 节：训练逻辑回归预测客户流失》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
import pytest

from .._helpers import tiny_classification
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_05_train_logistic(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_logistic(X, y)
    assert model.random_state == 42
    assert model.max_iter == 1000
    assert hasattr(model, "coef_")

def check_05_train_logistic_with_strength(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = module.train_logistic_with_strength(X, y, 0.5)
    assert model.C == 0.5
    assert model.random_state == 42
    with pytest.raises(ValueError):
        module.train_logistic_with_strength(X, y, 0)

def check_05_logistic_coefficient_table(module: ModuleType) -> None:
    X, y = tiny_classification()
    model = LogisticRegression(max_iter=1000, random_state=42).fit(X, y)
    result = module.logistic_coefficient_table(
        model,
        ["age", "spending", "orders"],
    )
    assert result.columns.tolist() == [
        "feature",
        "coefficient",
        "absolute_coefficient",
    ]
    assert result["absolute_coefficient"].is_monotonic_decreasing
    with pytest.raises(ValueError):
        module.logistic_coefficient_table(model, ["age"])
    with pytest.raises(NotFittedError):
        module.logistic_coefficient_table(
            LogisticRegression(),
            ["a", "b", "c"],
        )

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_05_train_logistic", answer, check_05_train_logistic),
    ("answer_05_train_logistic_with_strength", answer, check_05_train_logistic_with_strength),
    ("answer_05_logistic_coefficient_table", answer, check_05_logistic_coefficient_table),
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
