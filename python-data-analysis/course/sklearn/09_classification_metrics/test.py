"""scikit-learn《第 9 节：用五个指标评价流失模型》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_09_calculate_metrics(module: ModuleType) -> None:
    result = module.calculate_metrics(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 1, 1]),
        np.array([0.1, 0.6, 0.7, 0.9]),
    )
    assert set(result) == {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }
    assert result["accuracy"] == pytest.approx(0.75)
    assert result["recall"] == pytest.approx(1.0)
    with pytest.raises(ValueError):
        module.calculate_metrics(
            np.array([0, 0]),
            np.array([0, 0]),
            np.array([0.1, 0.2]),
        )

def check_09_calculate_threshold_metrics(module: ModuleType) -> None:
    result = module.calculate_threshold_metrics(
        np.array([0, 1, 1]),
        np.array([0.1, 0.4, 0.9]),
        0.5,
    )
    assert result["precision"] == pytest.approx(1.0)
    assert result["recall"] == pytest.approx(0.5)
    zero_result = module.calculate_threshold_metrics(
        np.array([0, 1]),
        np.array([0.1, 0.2]),
        1.0,
    )
    assert zero_result["precision"] == 0.0
    with pytest.raises(ValueError):
        module.calculate_threshold_metrics(
            np.array([0]),
            np.array([0.1]),
            2,
        )

def check_09_calculate_specificity(module: ModuleType) -> None:
    assert module.calculate_specificity(
        np.array([0, 0, 1]),
        np.array([0, 1, 1]),
    ) == pytest.approx(0.5)
    assert module.calculate_specificity(
        np.array([1, 1]),
        np.array([1, 0]),
    ) == 0.0

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_09_calculate_metrics", answer, check_09_calculate_metrics),
    ("answer_09_calculate_threshold_metrics", answer, check_09_calculate_threshold_metrics),
    ("answer_09_calculate_specificity", answer, check_09_calculate_specificity),
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
