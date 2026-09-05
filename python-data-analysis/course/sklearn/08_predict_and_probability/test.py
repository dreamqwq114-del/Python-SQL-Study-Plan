"""scikit-learn《第 8 节：输出类别、概率和客户预测表》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
from sklearn.linear_model import LogisticRegression
import pytest

from .._helpers import tiny_classification
from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_08_predict_labels_and_probabilities(module: ModuleType) -> None:
    model, X, _ = fitted_logistic()
    labels, probabilities = module.predict_labels_and_probabilities(
        model,
        X[:5],
    )
    assert labels.shape == (5,)
    assert probabilities.shape == (5,)
    assert np.all((probabilities >= 0) & (probabilities <= 1))

def check_08_predict_with_threshold(module: ModuleType) -> None:
    model, X, _ = fitted_logistic()
    probabilities = model.predict_proba(X[:5])[:, 1]
    result = module.predict_with_threshold(model, X[:5], 0.5)
    assert np.array_equal(result, (probabilities >= 0.5).astype(int))
    assert set(result).issubset({0, 1})
    with pytest.raises(ValueError):
        module.predict_with_threshold(model, X[:2], -0.1)
    with pytest.raises(ValueError):
        module.predict_with_threshold(model, X[:2], 1.1)

def check_08_build_prediction_table(module: ModuleType) -> None:
    result = module.build_prediction_table(
        ["C1", "C2"],
        np.array([0, 1]),
        np.array([0.2, 0.8]),
    )
    assert result.columns.tolist() == [
        "customer_id",
        "predicted_churn",
        "churn_probability",
    ]
    assert result.to_dict("records")[1] == {
        "customer_id": "C2",
        "predicted_churn": 1,
        "churn_probability": 0.8,
    }
    with pytest.raises(ValueError):
        module.build_prediction_table(
            ["C1"],
            np.array([0, 1]),
            np.array([0.2, 0.8]),
        )

def fitted_logistic() -> tuple[LogisticRegression, np.ndarray, np.ndarray]:
    X, y = tiny_classification()
    model = LogisticRegression(max_iter=1000, random_state=42).fit(X, y)
    return model, X, y

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_08_predict_labels_and_probabilities", answer, check_08_predict_labels_and_probabilities),
    ("answer_08_predict_with_threshold", answer, check_08_predict_with_threshold),
    ("answer_08_build_prediction_table", answer, check_08_build_prediction_table),
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
