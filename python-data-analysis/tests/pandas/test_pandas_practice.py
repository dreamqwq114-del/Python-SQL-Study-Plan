"""Pandas 14 节练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable

import pandas as pd
import pytest

from answers.pandas import answer_01_series_and_dataframe as answer_01
from answers.pandas import answer_02_read_csv as answer_02
from answers.pandas import answer_03_view_and_inspect as answer_03
from answers.pandas import answer_04_select_rows_and_columns as answer_04
from answers.pandas import answer_05_filter_data as answer_05
from answers.pandas import answer_06_missing_values as answer_06
from answers.pandas import answer_07_duplicates_and_types as answer_07
from answers.pandas import answer_08_sort_and_statistics as answer_08
from answers.pandas import answer_09_groupby_and_agg as answer_09
from answers.pandas import answer_10_merge_and_concat as answer_10
from answers.pandas import answer_11_map_replace_apply as answer_11
from answers.pandas import answer_12_string_operations as answer_12
from answers.pandas import answer_13_date_operations as answer_13
from answers.pandas import answer_14_save_data as answer_14
from practice.pandas import practice_01_series_and_dataframe as practice_01
from practice.pandas import practice_02_read_csv as practice_02
from practice.pandas import practice_03_view_and_inspect as practice_03
from practice.pandas import practice_04_select_rows_and_columns as practice_04
from practice.pandas import practice_05_filter_data as practice_05
from practice.pandas import practice_06_missing_values as practice_06
from practice.pandas import practice_07_duplicates_and_types as practice_07
from practice.pandas import practice_08_sort_and_statistics as practice_08
from practice.pandas import practice_09_groupby_and_agg as practice_09
from practice.pandas import practice_10_merge_and_concat as practice_10
from practice.pandas import practice_11_map_replace_apply as practice_11
from practice.pandas import practice_12_string_operations as practice_12
from practice.pandas import practice_13_date_operations as practice_13
from practice.pandas import practice_14_save_data as practice_14


Check = Callable[[ModuleType, Path], None]


def check_01_build_customer_frame(module: ModuleType, _: Path) -> None:
    result = module.build_customer_frame()
    expected = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "city": ["Suzhou", "Shanghai"],
            "monthly_spending": [188.5, 420.0],
        }
    )
    pd.testing.assert_frame_equal(result, expected)
    result.loc[0, "city"] = "Changed"
    assert module.build_customer_frame().loc[0, "city"] == "Suzhou"


def check_01_build_order_series(module: ModuleType, _: Path) -> None:
    result = module.build_order_series()
    expected = pd.Series(
        [1, 2, 3],
        index=["O001", "O002", "O003"],
        name="quantity",
    )
    pd.testing.assert_series_equal(result, expected)


def check_01_add_order_total(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"quantity": [2, 0, 3], "unit_price": [50, 99, 10]})
    original = source.copy()
    result = module.add_order_total(source)
    assert result["order_total"].tolist() == [100, 0, 30]
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.add_order_total(pd.DataFrame({"quantity": [1]}))


def check_02_load_customers(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame({"customer_id": ["C1", "C2"], "city": ["A", "B"]})
    path = tmp_path / "customers.csv"
    source.to_csv(path, index=False)
    pd.testing.assert_frame_equal(module.load_customers(path), source)
    with pytest.raises(FileNotFoundError):
        module.load_customers(tmp_path / "missing.csv")


def check_02_load_customer_columns(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", "C2"], "age": [20, 30], "city": ["A", "B"]}
    )
    path = tmp_path / "customers.csv"
    source.to_csv(path, index=False)
    result = module.load_customer_columns(path, ["age", "customer_id"])
    pd.testing.assert_frame_equal(result, source[["age", "customer_id"]])
    empty_columns = module.load_customer_columns(path, [])
    assert empty_columns.shape == (2, 0)
    with pytest.raises(KeyError):
        module.load_customer_columns(path, ["unknown"])


def check_02_load_orders_with_dates(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame(
        {"order_id": ["O1", "O2"], "order_date": ["2025-01-15", "wrong"]}
    )
    path = tmp_path / "orders.csv"
    source.to_csv(path, index=False)
    result = module.load_orders_with_dates(path)
    assert result.loc[0, "order_date"] == pd.Timestamp("2025-01-15")
    assert pd.isna(result.loc[1, "order_date"])
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])


def check_03_summarize_structure(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"age": [20, 30], "city": ["A", "B"]})
    result = module.summarize_structure(source)
    assert result == {
        "rows": 2,
        "columns": ["age", "city"],
        "dtypes": {
            "age": str(source["age"].dtype),
            "city": str(source["city"].dtype),
        },
    }
    assert module.summarize_structure(source.iloc[:0])["rows"] == 0


def check_03_preview_rows(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"value": [10, 20, 30]})
    pd.testing.assert_frame_equal(module.preview_rows(source, 2), source.head(2))
    assert module.preview_rows(source, 0).empty
    assert len(module.preview_rows(source, 10)) == 3
    with pytest.raises(ValueError):
        module.preview_rows(source, -1)


def check_03_count_column_values(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"contract": ["A", "A", "B", None]})
    result = module.count_column_values(source, "contract")
    assert result.to_dict() == {"A": 2, "B": 1}
    result_with_missing = module.count_column_values(
        source, "contract", include_missing=True
    )
    assert result_with_missing.sum() == 4
    assert result_with_missing[result_with_missing.index.isna()].iloc[0] == 1
    with pytest.raises(KeyError):
        module.count_column_values(source, "unknown")


def check_04_select_customer_columns(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "city": ["A"],
            "monthly_spending": [100.0],
            "customer_id": ["C1"],
        }
    )
    original = source.copy()
    result = module.select_customer_columns(source)
    assert result.columns.tolist() == ["customer_id", "monthly_spending"]
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.select_customer_columns(pd.DataFrame({"customer_id": ["C1"]}))


def check_04_select_rows_by_labels(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"value": [10, 20]}, index=["C1", "C2"])
    result = module.select_rows_by_labels(source, ["C2", "C1"])
    assert result.index.tolist() == ["C2", "C1"]
    assert module.select_rows_by_labels(source, []).empty
    with pytest.raises(KeyError):
        module.select_rows_by_labels(source, ["C9"])


def check_04_select_data_block(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"city": ["A", "B", "C"], "age": [20, 30, 40]})
    result = module.select_data_block(source, ["age"], 2)
    pd.testing.assert_frame_equal(result, source[["age"]].head(2))
    assert module.select_data_block(source, ["city"], 0).shape == (0, 1)
    with pytest.raises(ValueError):
        module.select_data_block(source, ["city"], -1)
    with pytest.raises(KeyError):
        module.select_data_block(source, ["unknown"], 1)


def check_05_filter_customers(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3", "C4"],
            "age": [35, 35, 29, 30],
            "churn": [1, 0, 1, 1],
        }
    )
    result = module.filter_customers(source)
    assert result["customer_id"].tolist() == ["C1", "C4"]
    assert module.filter_customers(source.assign(churn=0)).empty


def check_05_filter_by_cities(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"city": ["Suzhou", "Wuxi", "Shanghai"]})
    result = module.filter_by_cities(source, ["Wuxi", "Suzhou"])
    assert result["city"].tolist() == ["Suzhou", "Wuxi"]
    assert module.filter_by_cities(source, []).empty


def check_05_filter_spending_range(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"monthly_spending": [100.0, 200.0, 300.0, float("nan")]}
    )
    result = module.filter_spending_range(source, 100, 200)
    assert result["monthly_spending"].tolist() == [100.0, 200.0]
    with pytest.raises(ValueError):
        module.filter_spending_range(source, 300, 100)


def check_06_count_missing(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"age": [20, None], "city": ["A", "B"]})
    result = module.count_missing(source)
    assert result.to_dict() == {"age": 1, "city": 0}
    assert module.count_missing(source.iloc[:0]).to_dict() == {"age": 0, "city": 0}


def check_06_fill_missing_scores(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"satisfaction_score": [5.0, None, 2.0]})
    original = source.copy()
    result = module.fill_missing_scores(source, 3.0)
    assert result["satisfaction_score"].tolist() == [5.0, 3.0, 2.0]
    pd.testing.assert_frame_equal(source, original)


def check_06_drop_incomplete_rows(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", None, "C3"], "city": ["A", "B", None]}
    )
    result = module.drop_incomplete_rows(source, ["customer_id", "city"])
    assert result.to_dict("records") == [{"customer_id": "C1", "city": "A"}]
    pd.testing.assert_frame_equal(
        module.drop_incomplete_rows(source, []),
        source.reset_index(drop=True),
    )
    with pytest.raises(KeyError):
        module.drop_incomplete_rows(source, ["unknown"])


def check_07_clean_duplicates_and_spending(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C1", "C2"],
            "monthly_spending": ["100", "120", "bad"],
        }
    )
    original = source.copy()
    result = module.clean_duplicates_and_spending(source)
    assert result["customer_id"].tolist() == ["C1", "C2"]
    assert result.loc[0, "monthly_spending"] == 100
    assert pd.isna(result.loc[1, "monthly_spending"])
    pd.testing.assert_frame_equal(source, original)


def check_07_convert_customer_types(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"age": ["21", "bad"], "monthly_spending": ["19.5", "bad"]}
    )
    result = module.convert_customer_types(source)
    assert str(result["age"].dtype) == "Int64"
    assert result["age"].tolist()[0] == 21
    assert pd.isna(result["age"].tolist()[1])
    assert result.loc[0, "monthly_spending"] == 19.5
    assert pd.isna(result.loc[1, "monthly_spending"])


def check_07_keep_latest_customer_records(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C1"],
            "monthly_spending": [100, 200, 120],
        }
    )
    result = module.keep_latest_customer_records(source)
    assert result.to_dict("records") == [
        {"customer_id": "C2", "monthly_spending": 200},
        {"customer_id": "C1", "monthly_spending": 120},
    ]
    assert result.index.tolist() == [0, 1]


def check_08_spending_statistics(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"monthly_spending": [100.0, None, 300.0]})
    result = module.spending_statistics(source)
    assert result == {"mean": 200.0, "median": 200.0, "max": 300.0}
    empty_result = module.spending_statistics(source.iloc[:0])
    assert all(pd.isna(value) for value in empty_result.values())


def check_08_sort_customers_by_spending(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", "C2", "C3"], "monthly_spending": [100, 300, 200]}
    )
    original = source.copy()
    assert module.sort_customers_by_spending(source)["customer_id"].tolist() == [
        "C2",
        "C3",
        "C1",
    ]
    assert module.sort_customers_by_spending(
        source, ascending=True
    )["customer_id"].tolist() == ["C1", "C3", "C2"]
    pd.testing.assert_frame_equal(source, original)


def check_08_top_spending_customers(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1", "C2", "C3"], "monthly_spending": [100, 300, 200]}
    )
    result = module.top_spending_customers(source, 2)
    assert result["customer_id"].tolist() == ["C2", "C3"]
    assert module.top_spending_customers(source, 0).empty
    assert len(module.top_spending_customers(source, 10)) == 3
    with pytest.raises(ValueError):
        module.top_spending_customers(source, -1)


def check_09_summarize_by_city(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C2", "C3"],
            "city": ["A", "A", "A", "B"],
            "monthly_spending": [100.0, 300.0, 300.0, 50.0],
        }
    )
    result = module.summarize_by_city(source)
    assert result.to_dict("records") == [
        {"city": "A", "customer_count": 2, "average_spending": 700 / 3},
        {"city": "B", "customer_count": 1, "average_spending": 50.0},
    ]


def check_09_summarize_orders_by_customer(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3"],
            "customer_id": ["C1", "C1", "C2"],
            "quantity": [2, 1, 3],
            "unit_price": [50, 60, 10],
        }
    )
    result = module.summarize_orders_by_customer(source)
    assert result.to_dict("records") == [
        {"customer_id": "C1", "order_count": 2, "total_spending": 160},
        {"customer_id": "C2", "order_count": 1, "total_spending": 30},
    ]
    assert "order_total" not in source.columns


def check_09_calculate_churn_rate(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "contract_type": ["Monthly", "Monthly", "Yearly"],
            "churn": [1, 0, 0],
        }
    )
    result = module.calculate_churn_rate_by_contract(source)
    assert result.to_dict("records") == [
        {"contract_type": "Monthly", "customer_count": 2, "churn_rate": 0.5},
        {"contract_type": "Yearly", "customer_count": 1, "churn_rate": 0.0},
    ]


def check_10_merge_customers_orders(module: ModuleType, _: Path) -> None:
    customers = pd.DataFrame(
        {"customer_id": ["C1", "C2"], "city": ["A", "B"]}
    )
    orders = pd.DataFrame(
        {"customer_id": ["C1", "C1"], "order_id": ["O1", "O2"]}
    )
    result = module.merge_customers_orders(customers, orders)
    assert result["customer_id"].tolist() == ["C1", "C1", "C2"]
    assert pd.isna(result.loc[2, "order_id"])


def check_10_concat_order_batches(module: ModuleType, _: Path) -> None:
    first = pd.DataFrame({"order_id": ["O1", "O2"]})
    second = pd.DataFrame({"order_id": ["O3"]})
    result = module.concat_order_batches([first, second])
    assert result["order_id"].tolist() == ["O1", "O2", "O3"]
    assert result.index.tolist() == [0, 1, 2]
    assert module.concat_order_batches([]).empty


def check_10_find_orders_without_customer(module: ModuleType, _: Path) -> None:
    customers = pd.DataFrame({"customer_id": ["C1", "C2"]})
    orders = pd.DataFrame(
        {"order_id": ["O1", "O9"], "customer_id": ["C1", "C9"]}
    )
    result = module.find_orders_without_customer(customers, orders)
    assert result.to_dict("records") == [{"order_id": "O9", "customer_id": "C9"}]
    assert module.find_orders_without_customer(customers, orders.iloc[:1]).empty


def check_11_add_churn_and_annual_spending(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"churn": [1, 0, 9], "monthly_spending": [100.0, 50.0, 10.0]}
    )
    original = source.copy()
    result = module.add_churn_and_annual_spending(source)
    assert result["churn_label"].iloc[:2].tolist() == ["Churned", "Stayed"]
    assert pd.isna(result.loc[2, "churn_label"])
    assert result["annual_spending"].tolist() == [1200.0, 600.0, 120.0]
    pd.testing.assert_frame_equal(source, original)


def check_11_replace_contract_labels(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame({"contract_type": ["Monthly", "Yearly"]})
    result = module.replace_contract_labels(source, {"Monthly": "月付"})
    assert result["contract_type"].tolist() == ["月付", "Yearly"]
    unchanged = module.replace_contract_labels(source, {})
    pd.testing.assert_frame_equal(unchanged, source)


def check_11_add_spending_band(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"monthly_spending": [199.0, 200.0, 399.0, 400.0, None]}
    )
    result = module.add_spending_band(source)
    assert result["spending_band"].tolist() == [
        "Low",
        "Medium",
        "Medium",
        "High",
        "Unknown",
    ]


def check_12_clean_text_fields(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"city": [" Suzhou ", None], "contract_type": [" Monthly ", None]}
    )
    original = source.copy()
    result = module.clean_text_fields(source)
    assert result.loc[0, "city"] == "suzhou"
    assert result.loc[0, "contract_type"] == "Monthly"
    assert pd.isna(result.loc[1, "city"])
    pd.testing.assert_frame_equal(source, original)


def check_12_filter_products_by_keyword(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"product_name": ["USB Cable", "Phone Case", "Mouse", None]}
    )
    result = module.filter_products_by_keyword(source, "CASE")
    assert result["product_name"].tolist() == ["Phone Case"]
    result_literal = module.filter_products_by_keyword(source, ".")
    assert result_literal.empty
    assert len(module.filter_products_by_keyword(source, "")) == 3


def check_12_add_product_key(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"product_name": [" USB Cable ", "Phone   Case", None]}
    )
    result = module.add_product_key(source)
    assert result["product_key"].iloc[:2].tolist() == [
        "usb_cable",
        "phone_case",
    ]
    assert pd.isna(result.loc[2, "product_key"])


def check_13_add_date_parts(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {"join_date": ["2025-01-12", "2024/03/18", "wrong"]}
    )
    result = module.add_date_parts(source)
    assert result.loc[0, "join_year"] == 2025
    assert result.loc[1, "join_month"] == 3
    assert pd.isna(result.loc[2, "join_date"])
    assert pd.api.types.is_datetime64_any_dtype(result["join_date"])


def check_13_filter_orders_by_date(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "order_id": ["O1", "O2", "O3", "O4"],
            "order_date": ["2025-01-01", "2025-01-31", "2025-02-01", "wrong"],
        }
    )
    result = module.filter_orders_by_date(source, "2025-01-01", "2025-01-31")
    assert result["order_id"].tolist() == ["O1", "O2"]
    with pytest.raises(ValueError):
        module.filter_orders_by_date(source, "bad", "2025-01-31")
    with pytest.raises(ValueError):
        module.filter_orders_by_date(source, "2025-02-01", "2025-01-01")


def check_13_monthly_order_totals(module: ModuleType, _: Path) -> None:
    source = pd.DataFrame(
        {
            "order_date": ["2025-01-01", "2025/01/10", "2025-02-01", "wrong"],
            "quantity": [2, 1, 1, 99],
            "unit_price": [50, 50, 80, 99],
        }
    )
    result = module.monthly_order_totals(source)
    assert result.to_dict("records") == [
        {"order_month": "2025-01", "order_total": 150},
        {"order_month": "2025-02", "order_total": 80},
    ]


def check_14_save_processed(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame({"customer_id": ["C1", "C2"], "city": ["A", "B"]})
    path = tmp_path / "nested" / "customers.csv"
    assert module.save_processed(source, path) is None
    result = pd.read_csv(path)
    pd.testing.assert_frame_equal(result, source)
    assert "Unnamed: 0" not in result.columns


def check_14_save_selected_columns(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame(
        {"customer_id": ["C1"], "age": [20], "city": ["A"]}
    )
    path = tmp_path / "report" / "selected.csv"
    assert module.save_selected_columns(
        source, path, ["age", "customer_id"]
    ) is None
    result = pd.read_csv(path)
    assert result.columns.tolist() == ["age", "customer_id"]
    with pytest.raises(KeyError):
        module.save_selected_columns(source, path, ["unknown"])


def check_14_save_city_summary(module: ModuleType, tmp_path: Path) -> None:
    source = pd.DataFrame({"city": ["A", "A", "B", None]})
    path = tmp_path / "summary" / "city.csv"
    assert module.save_city_summary(source, path) is None
    result = pd.read_csv(path)
    assert result.to_dict("records") == [
        {"city": "A", "customer_count": 2},
        {"city": "B", "customer_count": 1},
    ]
    empty_path = tmp_path / "summary" / "empty.csv"
    module.save_city_summary(source.iloc[:0], empty_path)
    assert pd.read_csv(empty_path).empty


ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_build_customer_frame", answer_01, check_01_build_customer_frame),
    ("answer_01_build_order_series", answer_01, check_01_build_order_series),
    ("answer_01_add_order_total", answer_01, check_01_add_order_total),
    ("answer_02_load_customers", answer_02, check_02_load_customers),
    ("answer_02_load_customer_columns", answer_02, check_02_load_customer_columns),
    ("answer_02_load_orders_with_dates", answer_02, check_02_load_orders_with_dates),
    ("answer_03_summarize_structure", answer_03, check_03_summarize_structure),
    ("answer_03_preview_rows", answer_03, check_03_preview_rows),
    ("answer_03_count_column_values", answer_03, check_03_count_column_values),
    ("answer_04_select_customer_columns", answer_04, check_04_select_customer_columns),
    ("answer_04_select_rows_by_labels", answer_04, check_04_select_rows_by_labels),
    ("answer_04_select_data_block", answer_04, check_04_select_data_block),
    ("answer_05_filter_customers", answer_05, check_05_filter_customers),
    ("answer_05_filter_by_cities", answer_05, check_05_filter_by_cities),
    ("answer_05_filter_spending_range", answer_05, check_05_filter_spending_range),
    ("answer_06_count_missing", answer_06, check_06_count_missing),
    ("answer_06_fill_missing_scores", answer_06, check_06_fill_missing_scores),
    ("answer_06_drop_incomplete_rows", answer_06, check_06_drop_incomplete_rows),
    (
        "answer_07_clean_duplicates_and_spending",
        answer_07,
        check_07_clean_duplicates_and_spending,
    ),
    ("answer_07_convert_customer_types", answer_07, check_07_convert_customer_types),
    (
        "answer_07_keep_latest_customer_records",
        answer_07,
        check_07_keep_latest_customer_records,
    ),
    ("answer_08_spending_statistics", answer_08, check_08_spending_statistics),
    (
        "answer_08_sort_customers_by_spending",
        answer_08,
        check_08_sort_customers_by_spending,
    ),
    (
        "answer_08_top_spending_customers",
        answer_08,
        check_08_top_spending_customers,
    ),
    ("answer_09_summarize_by_city", answer_09, check_09_summarize_by_city),
    (
        "answer_09_summarize_orders_by_customer",
        answer_09,
        check_09_summarize_orders_by_customer,
    ),
    (
        "answer_09_calculate_churn_rate",
        answer_09,
        check_09_calculate_churn_rate,
    ),
    ("answer_10_merge_customers_orders", answer_10, check_10_merge_customers_orders),
    ("answer_10_concat_order_batches", answer_10, check_10_concat_order_batches),
    (
        "answer_10_find_orders_without_customer",
        answer_10,
        check_10_find_orders_without_customer,
    ),
    (
        "answer_11_add_churn_and_annual_spending",
        answer_11,
        check_11_add_churn_and_annual_spending,
    ),
    (
        "answer_11_replace_contract_labels",
        answer_11,
        check_11_replace_contract_labels,
    ),
    ("answer_11_add_spending_band", answer_11, check_11_add_spending_band),
    ("answer_12_clean_text_fields", answer_12, check_12_clean_text_fields),
    (
        "answer_12_filter_products_by_keyword",
        answer_12,
        check_12_filter_products_by_keyword,
    ),
    ("answer_12_add_product_key", answer_12, check_12_add_product_key),
    ("answer_13_add_date_parts", answer_13, check_13_add_date_parts),
    ("answer_13_filter_orders_by_date", answer_13, check_13_filter_orders_by_date),
    ("answer_13_monthly_order_totals", answer_13, check_13_monthly_order_totals),
    ("answer_14_save_processed", answer_14, check_14_save_processed),
    (
        "answer_14_save_selected_columns",
        answer_14,
        check_14_save_selected_columns,
    ),
    ("answer_14_save_city_summary", answer_14, check_14_save_city_summary),
]


PRACTICE_CASES: list[tuple[str, ModuleType, Check]] = [
    (name.replace("answer_", "practice_"), practice, check)
    for (name, _, check), practice in zip(
        ANSWER_CASES,
        [
            practice_01,
            practice_01,
            practice_01,
            practice_02,
            practice_02,
            practice_02,
            practice_03,
            practice_03,
            practice_03,
            practice_04,
            practice_04,
            practice_04,
            practice_05,
            practice_05,
            practice_05,
            practice_06,
            practice_06,
            practice_06,
            practice_07,
            practice_07,
            practice_07,
            practice_08,
            practice_08,
            practice_08,
            practice_09,
            practice_09,
            practice_09,
            practice_10,
            practice_10,
            practice_10,
            practice_11,
            practice_11,
            practice_11,
            practice_12,
            practice_12,
            practice_12,
            practice_13,
            practice_13,
            practice_13,
            practice_14,
            practice_14,
            practice_14,
        ],
    )
]


@pytest.mark.parametrize(
    ("name", "module", "check"),
    ANSWER_CASES,
    ids=[case[0] for case in ANSWER_CASES],
)
def test_answer_contract(
    name: str, module: ModuleType, check: Check, tmp_path: Path
) -> None:
    check(module, tmp_path)


@pytest.mark.parametrize(
    ("name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    name: str, module: ModuleType, check: Check, tmp_path: Path
) -> None:
    try:
        check(module, tmp_path)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
