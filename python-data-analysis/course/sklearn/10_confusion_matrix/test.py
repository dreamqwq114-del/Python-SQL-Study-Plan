"""scikit-learn《第 10 节：用混淆矩阵看清四种分类结果》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_10_build_confusion_matrix(module: ModuleType) -> None:
    result = module.build_confusion_matrix(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 0, 1]),
    )
    assert np.array_equal(result, np.array([[1, 1], [1, 1]]))
    one_class = module.build_confusion_matrix(
        np.array([0, 0]),
        np.array([0, 0]),
    )
    assert one_class.shape == (2, 2)

def check_10_confusion_counts(module: ModuleType) -> None:
    result = module.confusion_counts(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 0, 1]),
    )
    assert result == {"tn": 1, "fp": 1, "fn": 1, "tp": 1}
    assert module.confusion_counts(
        np.array([0, 1]),
        np.array([0, 1]),
    ) == {"tn": 1, "fp": 0, "fn": 0, "tp": 1}

def check_10_normalized_confusion_matrix(module: ModuleType) -> None:
    result = module.normalized_confusion_matrix(
        np.array([0, 0, 1, 1]),
        np.array([0, 1, 1, 1]),
    )
    assert np.allclose(result, [[0.5, 0.5], [0.0, 1.0]])
    one_class = module.normalized_confusion_matrix(
        np.array([0, 0]),
        np.array([0, 0]),
    )
    assert np.allclose(one_class, [[1.0, 0.0], [0.0, 0.0]])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_10_build_confusion_matrix", answer, check_10_build_confusion_matrix),
    ("answer_10_confusion_counts", answer, check_10_confusion_counts),
    ("answer_10_normalized_confusion_matrix", answer, check_10_normalized_confusion_matrix),
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
