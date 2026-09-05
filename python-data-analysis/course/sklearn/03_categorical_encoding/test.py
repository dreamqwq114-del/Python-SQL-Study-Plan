"""scikit-learn《第 3 节：把城市等分类文字变成独热编码》练习与参考答案的契约测试。"""

from types import ModuleType
from typing import Callable
import numpy as np
import pandas as pd
import pytest

from . import answer
from . import practice

Check = Callable[[ModuleType], None]

def check_03_encode_city_feature(module: ModuleType) -> None:
    train = pd.DataFrame({"city": ["A", "B", "A"]})
    test = pd.DataFrame({"city": ["B", "C"]})
    train_encoded, test_encoded = module.encode_city_feature(train, test)
    assert train_encoded.shape == (3, 2)
    assert test_encoded.shape == (2, 2)
    assert np.array_equal(test_encoded[0], np.array([0.0, 1.0]))
    assert np.array_equal(test_encoded[1], np.array([0.0, 0.0]))

def check_03_encode_categorical_features(module: ModuleType) -> None:
    train = pd.DataFrame(
        {
            "city": ["A", "B"],
            "contract": ["Monthly", "Yearly"],
        }
    )
    test = pd.DataFrame(
        {"city": ["C"], "contract": ["Monthly"]}
    )
    train_encoded, test_encoded = module.encode_categorical_features(
        train,
        test,
        ["city", "contract"],
    )
    assert train_encoded.shape == (2, 4)
    assert test_encoded.shape == (1, 4)
    with pytest.raises(ValueError):
        module.encode_categorical_features(train, test, [])
    with pytest.raises(KeyError):
        module.encode_categorical_features(train, test, ["unknown"])

def check_03_get_encoded_feature_names(module: ModuleType) -> None:
    train = pd.DataFrame(
        {
            "city": ["A", "B"],
            "contract": ["Monthly", "Yearly"],
        }
    )
    names = module.get_encoded_feature_names(
        train,
        ["city", "contract"],
    )
    assert names == [
        "city_A",
        "city_B",
        "contract_Monthly",
        "contract_Yearly",
    ]
    with pytest.raises(ValueError):
        module.get_encoded_feature_names(train, [])

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_03_encode_city_feature", answer, check_03_encode_city_feature),
    ("answer_03_encode_categorical_features", answer, check_03_encode_categorical_features),
    ("answer_03_get_encoded_feature_names", answer, check_03_get_encoded_feature_names),
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
