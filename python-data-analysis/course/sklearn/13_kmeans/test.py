"""scikit-learn《第 13 节：用 KMeans 给客户分群》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
from sklearn.cluster import KMeans
import pytest

from .._helpers import small_clusters
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_13_fit_kmeans(module: ModuleType) -> None:
    X = small_clusters()
    model = module.fit_kmeans(X, 3)
    assert model.n_clusters == 3
    assert model.random_state == 42
    assert model.n_init == 10
    assert model.labels_.shape == (30,)
    with pytest.raises(ValueError):
        module.fit_kmeans(X, 0)

def check_13_cluster_customers(module: ModuleType) -> None:
    X = small_clusters()
    labels = module.cluster_customers(X, 3)
    assert labels.shape == (30,)
    assert len(np.unique(labels)) == 3
    repeated = module.cluster_customers(X, 3)
    assert np.array_equal(labels, repeated)

def check_13_cluster_centers_table(module: ModuleType) -> None:
    X = small_clusters()
    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
    ).fit(X)
    result = module.cluster_centers_table(
        model,
        ["income", "spending"],
    )
    assert result.shape == (3, 3)
    assert result.columns.tolist() == ["cluster", "income", "spending"]
    assert result["cluster"].tolist() == [0, 1, 2]
    with pytest.raises(ValueError):
        module.cluster_centers_table(model, ["income"])
    with pytest.raises(AttributeError):
        module.cluster_centers_table(
            KMeans(n_clusters=2),
            ["income", "spending"],
        )

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_13_fit_kmeans", answer, check_13_fit_kmeans),
    ("answer_13_cluster_customers", answer, check_13_cluster_customers),
    ("answer_13_cluster_centers_table", answer, check_13_cluster_centers_table),
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
