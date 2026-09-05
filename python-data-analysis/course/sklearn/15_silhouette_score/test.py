"""scikit-learn《第 15 节：用轮廓系数评价聚类》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import pytest

from .._helpers import small_clusters
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_15_calculate_silhouette_scores(module: ModuleType) -> None:
    X = small_clusters()
    scores = module.calculate_silhouette_scores(X, [2, 3, 4])
    assert set(scores) == {2, 3, 4}
    assert all(-1 <= score <= 1 for score in scores.values())
    assert scores[3] > scores[2]
    assert module.calculate_silhouette_scores(X, []) == {}

def check_15_select_best_silhouette_k(module: ModuleType) -> None:
    assert module.select_best_silhouette_k({2: 0.4, 3: 0.6}) == 3
    assert module.select_best_silhouette_k({3: 0.5, 2: 0.5}) == 2
    with pytest.raises(ValueError):
        module.select_best_silhouette_k({})

def check_15_build_cluster_evaluation(module: ModuleType) -> None:
    X = small_clusters()
    result = module.build_cluster_evaluation(X, [2, 3, 4])
    assert result.columns.tolist() == ["k", "inertia", "silhouette"]
    assert result["k"].tolist() == [2, 3, 4]
    assert result["silhouette"].between(-1, 1).all()
    empty = module.build_cluster_evaluation(X, [])
    assert empty.empty
    assert empty.columns.tolist() == ["k", "inertia", "silhouette"]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_15_calculate_silhouette_scores", answer, check_15_calculate_silhouette_scores),
    ("answer_15_select_best_silhouette_k", answer, check_15_select_best_silhouette_k),
    ("answer_15_build_cluster_evaluation", answer, check_15_build_cluster_evaluation),
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
