"""scikit-learn《第 14 节：用肘部法观察聚类数量》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import pytest

from .._helpers import small_clusters
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_14_calculate_inertias(module: ModuleType) -> None:
    X = small_clusters()
    inertias = module.calculate_inertias(X, [2, 3, 4])
    assert len(inertias) == 3
    assert inertias[0] > inertias[1] > inertias[2]
    assert module.calculate_inertias(X, []) == []

def check_14_calculate_inertia_drops(module: ModuleType) -> None:
    assert module.calculate_inertia_drops([100.0, 60.0, 45.0]) == [
        40.0,
        15.0,
    ]
    assert module.calculate_inertia_drops([]) == []
    assert module.calculate_inertia_drops([100.0]) == []
    with pytest.raises(ValueError):
        module.calculate_inertia_drops([10.0, 20.0])
    with pytest.raises(ValueError):
        module.calculate_inertia_drops([10.0, -1.0])

def check_14_build_elbow_table(module: ModuleType) -> None:
    X = small_clusters()
    result = module.build_elbow_table(X, [2, 3])
    assert result.columns.tolist() == ["k", "inertia"]
    assert result["k"].tolist() == [2, 3]
    empty = module.build_elbow_table(X, [])
    assert empty.empty
    assert empty.columns.tolist() == ["k", "inertia"]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_14_calculate_inertias", answer, check_14_calculate_inertias),
    ("answer_14_calculate_inertia_drops", answer, check_14_calculate_inertia_drops),
    ("answer_14_build_elbow_table", answer, check_14_build_elbow_table),
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
