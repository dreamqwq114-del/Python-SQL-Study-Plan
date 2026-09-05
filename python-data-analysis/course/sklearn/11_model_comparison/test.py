"""scikit-learn《第 11 节：公平比较多个分类模型》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._helpers import comparison_split
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_11_compare_models(module: ModuleType) -> None:
    result = module.compare_models(*comparison_split())
    assert result.columns.tolist() == ["model", "accuracy", "roc_auc"]
    assert result["model"].tolist() == ["Logistic", "Tree"]
    assert result[["accuracy", "roc_auc"]].apply(
        lambda column: column.between(0, 1).all()
    ).all()

def check_11_rank_models(module: ModuleType) -> None:
    source = pd.DataFrame(
        {
            "model": ["A", "B", "C"],
            "accuracy": [0.7, 0.9, 0.9],
        }
    )
    original = source.copy()
    result = module.rank_models(source, "accuracy")
    assert result["model"].tolist() == ["B", "C", "A"]
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.rank_models(source, "roc_auc")

def check_11_select_best_model_name(module: ModuleType) -> None:
    results = pd.DataFrame(
        {
            "model": ["Logistic", "Tree"],
            "roc_auc": [0.8, 0.7],
        }
    )
    assert module.select_best_model_name(results, "roc_auc") == "Logistic"
    tied = results.assign(roc_auc=[0.8, 0.8])
    assert module.select_best_model_name(tied, "roc_auc") == "Logistic"
    with pytest.raises(ValueError):
        module.select_best_model_name(results.iloc[:0], "roc_auc")

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_11_compare_models", answer, check_11_compare_models),
    ("answer_11_rank_models", answer, check_11_rank_models),
    ("answer_11_select_best_model_name", answer, check_11_select_best_model_name),
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
