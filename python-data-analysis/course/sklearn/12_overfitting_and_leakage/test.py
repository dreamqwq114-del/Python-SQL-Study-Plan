"""scikit-learn《第 12 节：识别过拟合和数据泄漏》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
from sklearn.linear_model import LogisticRegression
import pytest

from .._helpers import comparison_split
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_12_compare_train_test_accuracy(module: ModuleType) -> None:
    X_train, X_test, y_train, y_test = comparison_split()
    model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    train_score, test_score = module.compare_train_test_accuracy(
        model,
        X_train,
        X_test,
        y_train,
        y_test,
    )
    assert 0 <= train_score <= 1
    assert 0 <= test_score <= 1

def check_12_detect_overfitting(module: ModuleType) -> None:
    assert module.detect_overfitting(0.95, 0.75, 0.1) is True
    assert module.detect_overfitting(0.85, 0.80, 0.1) is False
    assert module.detect_overfitting(0.9, 0.8, 0.1) is False
    with pytest.raises(ValueError):
        module.detect_overfitting(1.1, 0.8, 0.1)

def check_12_scale_without_leakage(module: ModuleType) -> None:
    train = np.array([[1.0], [2.0], [3.0]])
    test = np.array([[100.0]])
    train_scaled, test_scaled = module.scale_without_leakage(train, test)
    assert train_scaled.mean() == pytest.approx(0.0)
    assert train_scaled.std() == pytest.approx(1.0)
    assert test_scaled[0, 0] > 10

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_12_compare_train_test_accuracy", answer, check_12_compare_train_test_accuracy),
    ("answer_12_detect_overfitting", answer, check_12_detect_overfitting),
    ("answer_12_scale_without_leakage", answer, check_12_scale_without_leakage),
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
