"""跨领域综合项目《combined_customer_project》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.errors import MergeError
from sklearn.model_selection import train_test_split
import pytest

from . import answer
from . import practice
from utils.paths import DATA_DIR

Check = Callable[[ModuleType, Path], None]

def check_load_datasets(module: ModuleType, tmp_path: Path) -> None:
    customers, orders = module.load_datasets(
        DATA_DIR / "sample_customers.csv",
        DATA_DIR / "sample_orders.csv",
    )
    assert customers.shape == (31, 9)
    assert orders.shape == (45, 7)
    assert "customer_id" in customers.columns
    assert "order_id" in orders.columns

    with pytest.raises(FileNotFoundError):
        module.load_datasets(
            tmp_path / "missing_customers.csv",
            DATA_DIR / "sample_orders.csv",
        )
def check_clean_customers(module: ModuleType, tmp_path: Path) -> None:
    raw = pd.read_csv(DATA_DIR / "sample_customers.csv")
    original = raw.copy(deep=True)
    cleaned = module.clean_customers(raw)

    assert len(cleaned) == 30
    assert cleaned["customer_id"].is_unique
    assert set(cleaned["gender"]) == {"female", "male"}
    assert {"Suzhou", "Shanghai", "Nanjing", "Wuxi"} == set(cleaned["city"])
    assert set(cleaned["contract_type"]) == {
        "monthly",
        "yearly",
        "two-year",
    }
    assert set(cleaned["churn"]) == {0, 1}
    assert cleaned["churn"].dtype.kind in "iu"
    for column in ["age", "monthly_spending", "satisfaction_score"]:
        assert pd.api.types.is_numeric_dtype(cleaned[column])
        assert int(cleaned[column].isna().sum()) == 1
    assert pd.api.types.is_datetime64_any_dtype(cleaned["join_date"])
    pd.testing.assert_frame_equal(raw, original)

    invalid_churn = original.iloc[:3].copy()
    invalid_churn.loc[0, "churn"] = "Maybe"
    with pytest.raises(ValueError):
        module.clean_customers(invalid_churn)

    no_numeric_values = original.iloc[:2].copy()
    no_numeric_values["age"] = "unknown"
    with pytest.raises(ValueError):
        module.clean_customers(no_numeric_values)

    normalized_duplicates = original.iloc[:2].copy()
    normalized_duplicates.loc[0, "customer_id"] = " C001 "
    normalized_duplicates.loc[1, "customer_id"] = "C001"
    normalized_result = module.clean_customers(normalized_duplicates)
    assert normalized_result["customer_id"].tolist() == ["C001"]

    empty_customer_id = original.iloc[:1].copy()
    empty_customer_id.loc[0, "customer_id"] = "  "
    with pytest.raises(ValueError):
        module.clean_customers(empty_customer_id)

    with pytest.raises(KeyError):
        module.clean_customers(original.drop(columns="city"))
def check_summarize_orders(module: ModuleType, tmp_path: Path) -> None:
    orders = pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3", "O4"],
            "customer_id": ["C1", "C1", "C1", "C2"],
            "quantity": [2, 1, 4, 3],
            "unit_price": [10.0, 30.0, 100.0, 5.0],
            "order_status": [
                "Completed",
                " completed ",
                "Cancelled",
                "Returned",
            ],
        }
    )
    original = orders.copy(deep=True)
    summary = module.summarize_orders(orders)

    assert summary.columns.tolist() == [
        "customer_id",
        "order_count",
        "total_order_spending",
        "average_order_value",
    ]
    assert summary["customer_id"].tolist() == ["C1"]
    assert summary.loc[0, "order_count"] == 2
    assert summary.loc[0, "total_order_spending"] == pytest.approx(50.0)
    assert summary.loc[0, "average_order_value"] == pytest.approx(25.0)
    pd.testing.assert_frame_equal(orders, original)

    no_completed = orders.assign(order_status="Cancelled")
    empty = module.summarize_orders(no_completed)
    assert empty.empty
    assert empty.columns.tolist() == summary.columns.tolist()

    with pytest.raises(ValueError):
        module.summarize_orders(orders.assign(quantity=-1))
    with pytest.raises(ValueError):
        module.summarize_orders(orders.assign(quantity=1.5))
    with pytest.raises(ValueError):
        module.summarize_orders(orders.assign(unit_price="bad"))
    with pytest.raises(ValueError):
        module.summarize_orders(orders.assign(unit_price=None))
    with pytest.raises(ValueError):
        module.summarize_orders(orders.assign(unit_price=np.inf))
def check_merge_customer_summary(module: ModuleType, tmp_path: Path) -> None:
    customers = pd.DataFrame(
        {
            "customer_id": ["C1", "C2"],
            "city": ["Suzhou", "Wuxi"],
        }
    )
    summary = pd.DataFrame(
        {
            "customer_id": ["C1"],
            "order_count": [2],
            "total_order_spending": [50.0],
            "average_order_value": [25.0],
        }
    )
    merged = module.merge_customer_summary(customers, summary)

    assert merged["customer_id"].tolist() == ["C1", "C2"]
    assert merged.loc[1, "order_count"] == 0
    assert merged.loc[1, "total_order_spending"] == pytest.approx(0.0)
    assert merged.loc[1, "average_order_value"] == pytest.approx(0.0)
    assert merged["order_count"].dtype.kind in "iu"
    assert "order_count" not in customers.columns

    duplicate_summary = pd.concat([summary, summary], ignore_index=True)
    with pytest.raises(MergeError):
        module.merge_customer_summary(customers, duplicate_summary)
    with pytest.raises(KeyError):
        module.merge_customer_summary(customers.drop(columns="customer_id"), summary)
def check_create_customer_figure(module: ModuleType, tmp_path: Path) -> None:
    dataframe = pd.DataFrame(
        {
            "city": ["Suzhou", "Suzhou", "Wuxi"],
            "monthly_spending": [100.0, 200.0, 300.0],
            "churn": [0, 1, 0],
        }
    )
    output_path = tmp_path / "nested" / "customer_report.png"
    figures_before = set(plt.get_fignums())
    result = module.create_customer_figure(dataframe, output_path)

    assert result is None
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    assert set(plt.get_fignums()) == figures_before

    with pytest.raises(KeyError):
        module.create_customer_figure(
            dataframe.drop(columns="city"),
            tmp_path / "invalid.png",
        )
def _build_analysis_data(module: ModuleType) -> pd.DataFrame:
    customers, orders = module.load_datasets(
        DATA_DIR / "sample_customers.csv",
        DATA_DIR / "sample_orders.csv",
    )
    cleaned = module.clean_customers(customers)
    summary = module.summarize_orders(orders)
    return module.merge_customer_summary(cleaned, summary)
def check_train_churn_classifier(module: ModuleType, tmp_path: Path) -> None:
    analysis_data = _build_analysis_data(module)
    model, metrics = module.train_churn_classifier(analysis_data)

    assert list(model.named_steps) == ["preprocessor", "classifier"]
    assert set(metrics) == {
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    }
    assert all(isinstance(value, float) for value in metrics.values())
    assert all(0.0 <= value <= 1.0 for value in metrics.values())
    predictions = model.predict(
        analysis_data[
            [
                "age",
                "monthly_spending",
                "satisfaction_score",
                "order_count",
                "total_order_spending",
                "average_order_value",
                "gender",
                "city",
                "contract_type",
            ]
        ].iloc[:2]
    )
    assert predictions.shape == (2,)

    numeric_features = [
        "age",
        "monthly_spending",
        "satisfaction_score",
        "order_count",
        "total_order_spending",
        "average_order_value",
    ]
    categorical_features = ["gender", "city", "contract_type"]
    X_train, _, _, _ = train_test_split(
        analysis_data[numeric_features + categorical_features],
        analysis_data["churn"],
        test_size=0.25,
        stratify=analysis_data["churn"],
        random_state=42,
    )
    learned_medians = (
        model.named_steps["preprocessor"]
        .named_transformers_["numeric"]
        .named_steps["imputer"]
        .statistics_
    )
    expected_train_medians = X_train[numeric_features].median().to_numpy()
    assert np.allclose(learned_medians, expected_train_medians)
    assert not np.allclose(
        learned_medians,
        analysis_data[numeric_features].median().to_numpy(),
    )

    with pytest.raises(ValueError):
        module.train_churn_classifier(analysis_data.assign(churn=0))
    with pytest.raises(ValueError):
        module.train_churn_classifier(analysis_data.assign(churn="Yes"))
    with pytest.raises(KeyError):
        module.train_churn_classifier(
            analysis_data.drop(columns="monthly_spending")
        )

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_load_datasets", answer, check_load_datasets),
    ("answer_clean_customers", answer, check_clean_customers),
    ("answer_summarize_orders", answer, check_summarize_orders),
    ("answer_merge_customer_summary", answer, check_merge_customer_summary),
    ("answer_create_customer_figure", answer, check_create_customer_figure),
    ("answer_train_churn_classifier", answer, check_train_churn_classifier),
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
    tmp_path: Path,
) -> None:
    check(module, tmp_path)

@pytest.mark.parametrize(
    ("name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    name: str,
    module: ModuleType,
    check: Check,
    tmp_path: Path,
) -> None:
    try:
        check(module, tmp_path)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
