"""scikit-learn《第 4 节：用 StandardScaler 统一数值尺度》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_04_scale_features(module: ModuleType) -> None:
    train = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    test = np.array([[4.0, 40.0]])
    train_scaled, test_scaled = module.scale_features(train, test)
    assert np.allclose(train_scaled.mean(axis=0), 0.0)
    assert np.allclose(train_scaled.std(axis=0), 1.0)
    assert test_scaled.shape == (1, 2)
    assert not np.allclose(test_scaled, 0.0)

def check_04_scale_dataframe_columns(module: ModuleType) -> None:
    train = pd.DataFrame(
        {"age": [10.0, 20.0, 30.0], "city": ["A", "B", "C"]}
    )
    test = pd.DataFrame({"age": [40.0], "city": ["D"]})
    original = train.copy()
    train_scaled, test_scaled = module.scale_dataframe_columns(
        train,
        test,
        ["age"],
    )
    assert train_scaled["age"].mean() == pytest.approx(0.0)
    assert train_scaled["city"].tolist() == ["A", "B", "C"]
    assert test_scaled["city"].tolist() == ["D"]
    pd.testing.assert_frame_equal(train, original)
    empty_train, empty_test = module.scale_dataframe_columns(train, test, [])
    pd.testing.assert_frame_equal(empty_train, train)
    pd.testing.assert_frame_equal(empty_test, test)

def check_04_summarize_scaled_training(module: ModuleType) -> None:
    data = np.array([[-1.0, -1.0], [1.0, 1.0]])
    result = module.summarize_scaled_training(data)
    assert np.allclose(result["mean"], [0.0, 0.0])
    assert np.allclose(result["std"], [1.0, 1.0])
    with pytest.raises(ValueError):
        module.summarize_scaled_training(np.array([]))
    with pytest.raises(ValueError):
        module.summarize_scaled_training(np.array([1.0, 2.0]))

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_04_scale_features", answer, check_04_scale_features),
    ("answer_04_scale_dataframe_columns", answer, check_04_scale_dataframe_columns),
    ("answer_04_summarize_scaled_training", answer, check_04_summarize_scaled_training),
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
