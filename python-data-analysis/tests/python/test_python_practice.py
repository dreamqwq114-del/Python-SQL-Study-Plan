"""Python 九章答案与练习的统一行为测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable

import pytest

from answers.python import answer_01_variables_and_types as answer_01
from answers.python import answer_02_lists_tuples_sets as answer_02
from answers.python import answer_03_dictionaries as answer_03
from answers.python import answer_04_if_and_loops as answer_04
from answers.python import answer_05_functions as answer_05
from answers.python import answer_06_modules_and_imports as answer_06
from answers.python import answer_07_files_and_paths as answer_07
from answers.python import answer_08_exceptions as answer_08
from answers.python import answer_09_basic_classes as answer_09
from practice.python import practice_01_variables_and_types as practice_01
from practice.python import practice_02_lists_tuples_sets as practice_02
from practice.python import practice_03_dictionaries as practice_03
from practice.python import practice_04_if_and_loops as practice_04
from practice.python import practice_05_functions as practice_05
from practice.python import practice_06_modules_and_imports as practice_06
from practice.python import practice_07_files_and_paths as practice_07
from practice.python import practice_08_exceptions as practice_08
from practice.python import practice_09_basic_classes as practice_09

CheckFunction = Callable[[ModuleType, Path], None]


def check_convert_age(module: ModuleType, tmp_path: Path) -> None:
    assert module.convert_age("21") == 21
    assert module.convert_age(" 0 ") == 0
    for invalid in ("-1", "21.5", "twenty", ""):
        with pytest.raises(ValueError):
            module.convert_age(invalid)


def check_convert_price(module: ModuleType, tmp_path: Path) -> None:
    assert module.convert_price("39.90") == pytest.approx(39.9)
    assert module.convert_price(" 0 ") == pytest.approx(0.0)
    for invalid in ("-0.01", "39.90元", "", "free"):
        with pytest.raises(ValueError):
            module.convert_price(invalid)


def check_calculate_order_amount(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_order_amount("12.50", "4") == pytest.approx(50.0)
    assert module.calculate_order_amount("8", "0") == pytest.approx(0.0)
    for price, quantity in (("-1", "2"), ("10", "-2"), ("10", "2.5"), ("bad", "2")):
        with pytest.raises(ValueError):
            module.calculate_order_amount(price, quantity)


def check_build_order_summary(module: ModuleType, tmp_path: Path) -> None:
    assert module.build_order_summary("Notebook", "2", "12.50") == (
        "商品：Notebook，数量：2，单价：12.50 元，总金额：25.00 元"
    )
    assert module.build_order_summary("Pen", "0", "3") == (
        "商品：Pen，数量：0，单价：3.00 元，总金额：0.00 元"
    )
    for quantity, price in (("-1", "12.50"), ("2", "-1"), ("two", "12.50")):
        with pytest.raises(ValueError):
            module.build_order_summary("Notebook", quantity, price)


def check_unique_recent_items(module: ModuleType, tmp_path: Path) -> None:
    items = ["Pen", "Book", "Pen", "Mouse"]
    assert module.unique_recent_items(items, 1) == {"Book", "Pen", "Mouse"}
    assert module.unique_recent_items(items, 4) == set()
    assert module.unique_recent_items(items, -2) == {"Pen", "Mouse"}
    assert items == ["Pen", "Book", "Pen", "Mouse"]


def check_calculate_average_score(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_average_score([80, 90, 70]) == pytest.approx(80.0)
    assert module.calculate_average_score([88.5]) == pytest.approx(88.5)
    with pytest.raises(ValueError):
        module.calculate_average_score([])


def check_unpack_order(module: ModuleType, tmp_path: Path) -> None:
    assert module.unpack_order(("Notebook", 2, 12.5)) == "Notebook：2 × 12.50"
    assert module.unpack_order(("Pen", 0, 3.0)) == "Pen：0 × 3.00"
    with pytest.raises(ValueError):
        module.unpack_order(("Pen", -1, 3.0))
    with pytest.raises(ValueError):
        module.unpack_order(("Pen", 1, -3.0))


def check_find_common_customers(module: ModuleType, tmp_path: Path) -> None:
    first = {"C1", "C2"}
    second = {"C2", "C3"}
    assert module.find_common_customers(first, second) == {"C2"}
    assert module.find_common_customers(set(), second) == set()
    assert first == {"C1", "C2"}
    assert second == {"C2", "C3"}


def check_count_categories(module: ModuleType, tmp_path: Path) -> None:
    assert module.count_categories(["A", "B", "A"]) == {"A": 2, "B": 1}
    assert module.count_categories([]) == {}
    assert module.count_categories(["a", "A"]) == {"a": 1, "A": 1}


def check_build_customer_record(module: ModuleType, tmp_path: Path) -> None:
    assert module.build_customer_record("C1", "Suzhou", 120.5) == {
        "customer_id": "C1",
        "city": "Suzhou",
        "monthly_spending": 120.5,
    }
    assert module.build_customer_record("C2", "", 0)["monthly_spending"] == 0
    with pytest.raises(ValueError):
        module.build_customer_record("", "Suzhou", 10)
    with pytest.raises(ValueError):
        module.build_customer_record("C1", "Suzhou", -1)


def check_get_required_value(module: ModuleType, tmp_path: Path) -> None:
    assert module.get_required_value({"city": "Suzhou"}, "city") == "Suzhou"
    assert module.get_required_value({"score": 0}, "score") == 0
    with pytest.raises(KeyError):
        module.get_required_value({}, "customer_id")


def check_merge_monthly_sales(module: ModuleType, tmp_path: Path) -> None:
    january = {"Pen": 10.0}
    february = {"Pen": 5.0, "Book": 20.0}
    assert module.merge_monthly_sales(january, february) == {"Pen": 15.0, "Book": 20.0}
    assert january == {"Pen": 10.0}
    assert module.merge_monthly_sales({}, {"Book": 8.0}) == {"Book": 8.0}
    with pytest.raises(ValueError):
        module.merge_monthly_sales({"Pen": -1.0}, {})


def check_classify_spending(module: ModuleType, tmp_path: Path) -> None:
    assert module.classify_spending(99.0) == "low"
    assert module.classify_spending(100.0) == "medium"
    assert module.classify_spending(499.99) == "medium"
    assert module.classify_spending(500.0) == "high"
    with pytest.raises(ValueError):
        module.classify_spending(-0.01)


def check_count_churned(module: ModuleType, tmp_path: Path) -> None:
    assert module.count_churned(["Yes", "No", "Yes"]) == 2
    assert module.count_churned([]) == 0
    with pytest.raises(ValueError):
        module.count_churned(["yes"])


def check_calculate_valid_average(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_valid_average([4, None, 2]) == pytest.approx(3.0)
    assert module.calculate_valid_average([5]) == pytest.approx(5.0)
    with pytest.raises(ValueError):
        module.calculate_valid_average([])
    with pytest.raises(ValueError):
        module.calculate_valid_average([None, None])


def check_find_first_large_order(module: ModuleType, tmp_path: Path) -> None:
    assert module.find_first_large_order([20, 150, 80], 100) == 1
    assert module.find_first_large_order([20, 100], 100) is None
    assert module.find_first_large_order([], 0) is None
    with pytest.raises(ValueError):
        module.find_first_large_order([10, -1], 5)
    with pytest.raises(ValueError):
        module.find_first_large_order([10], -1)


def check_calculate_order_total(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_order_total(3, 20.0, 0.1) == pytest.approx(54.0)
    assert module.calculate_order_total(2, 15.0) == pytest.approx(30.0)
    assert module.calculate_order_total(0, 15.0, 1.0) == pytest.approx(0.0)
    for arguments in ((-1, 10.0, 0.0), (1, -1.0, 0.0), (1, 10.0, 1.1)):
        with pytest.raises(ValueError):
            module.calculate_order_total(*arguments)


def check_calculate_growth_rate(module: ModuleType, tmp_path: Path) -> None:
    assert module.calculate_growth_rate(100, 120) == pytest.approx(20.0)
    assert module.calculate_growth_rate(200, 150) == pytest.approx(-25.0)
    assert module.calculate_growth_rate(100, 0) == pytest.approx(-100.0)
    with pytest.raises(ValueError):
        module.calculate_growth_rate(0, 10)
    with pytest.raises(ValueError):
        module.calculate_growth_rate(10, -1)


def check_summarize_scores(module: ModuleType, tmp_path: Path) -> None:
    assert module.summarize_scores([60, 80, 100]) == pytest.approx((60, 100, 80))
    assert module.summarize_scores([88.5]) == pytest.approx((88.5, 88.5, 88.5))
    with pytest.raises(ValueError):
        module.summarize_scores([])
    with pytest.raises(ValueError):
        module.summarize_scores([101])


def check_format_customer_label(module: ModuleType, tmp_path: Path) -> None:
    assert module.format_customer_label(" C001 ", " Suzhou ") == "C001 - Suzhou"
    assert module.format_customer_label("C002") == "C002 - Unknown"
    assert module.format_customer_label("C003", "  ") == "C003 - Unknown"
    with pytest.raises(ValueError):
        module.format_customer_label("  ", "Suzhou")


def check_build_data_path(module: ModuleType, tmp_path: Path) -> None:
    path = module.build_data_path("sample_customers.csv")
    assert path.name == "sample_customers.csv"
    assert path.parent.name == "data"
    for invalid in ("", "customers.txt", "folder/customers.csv"):
        with pytest.raises(ValueError):
            module.build_data_path(invalid)


def check_build_processed_path(module: ModuleType, tmp_path: Path) -> None:
    path = module.build_processed_path("clean.csv")
    assert path.name == "clean.csv"
    assert path.parent.name == "processed"
    with pytest.raises(ValueError):
        module.build_processed_path("clean.xlsx")
    with pytest.raises(ValueError):
        module.build_processed_path("nested/clean.csv")


def check_build_figure_path(module: ModuleType, tmp_path: Path) -> None:
    path = module.build_figure_path("sales.png")
    assert path.name == "sales.png"
    assert path.parent.name == "figures"
    with pytest.raises(ValueError):
        module.build_figure_path("sales.jpg")
    with pytest.raises(ValueError):
        module.build_figure_path("nested/sales.png")


def check_get_project_directories(module: ModuleType, tmp_path: Path) -> None:
    directories = module.get_project_directories()
    assert set(directories) == {"root", "data", "processed", "figures"}
    assert directories["data"].parent == directories["root"]
    assert directories["processed"].parent == directories["data"]
    assert directories["figures"].parent == directories["root"]


def check_read_first_line(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("first\nsecond\n", encoding="utf-8")
    assert module.read_first_line(path) == "first"
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    assert module.read_first_line(empty) == ""
    with pytest.raises(FileNotFoundError):
        module.read_first_line(tmp_path / "missing.txt")


def check_read_nonempty_lines(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "fields.txt"
    path.write_text(" age \n\n city\n  \n", encoding="utf-8")
    assert module.read_nonempty_lines(path) == ["age", "city"]
    empty = tmp_path / "empty_lines.txt"
    empty.write_text("", encoding="utf-8")
    assert module.read_nonempty_lines(empty) == []


def check_write_report(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "nested" / "report.txt"
    lines = ["A", "B"]
    assert module.write_report(path, lines) is None
    assert path.read_text(encoding="utf-8") == "A\nB\n"
    assert lines == ["A", "B"]
    empty_path = tmp_path / "empty_report.txt"
    module.write_report(empty_path, [])
    assert empty_path.read_text(encoding="utf-8") == ""


def check_count_csv_rows(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "data.csv"
    path.write_text('id,name\n1,"A, B"\n2,C\n', encoding="utf-8")
    assert module.count_csv_rows(path) == 2
    header_only = tmp_path / "header.csv"
    header_only.write_text("id,name\n", encoding="utf-8")
    assert module.count_csv_rows(header_only) == 0
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        module.count_csv_rows(empty)


def check_parse_positive_amount(module: ModuleType, tmp_path: Path) -> None:
    assert module.parse_positive_amount("12.5") == pytest.approx(12.5)
    assert module.parse_positive_amount(" 1 ") == pytest.approx(1.0)
    for invalid in ("0", "-1", "", "bad"):
        with pytest.raises(ValueError):
            module.parse_positive_amount(invalid)


def check_parse_optional_score(module: ModuleType, tmp_path: Path) -> None:
    assert module.parse_optional_score("88.5") == pytest.approx(88.5)
    assert module.parse_optional_score(" NA ") is None
    assert module.parse_optional_score("") is None
    assert module.parse_optional_score("0") == pytest.approx(0.0)
    assert module.parse_optional_score("100") == pytest.approx(100.0)
    for invalid in ("-1", "101", "bad"):
        with pytest.raises(ValueError):
            module.parse_optional_score(invalid)


def check_safe_divide(module: ModuleType, tmp_path: Path) -> None:
    assert module.safe_divide(10, 2) == pytest.approx(5.0)
    assert module.safe_divide(0, 5) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        module.safe_divide(10, 0)


def check_read_required_text(module: ModuleType, tmp_path: Path) -> None:
    path = tmp_path / "required.txt"
    path.write_text(" customer_id \n", encoding="utf-8")
    assert module.read_required_text(path) == "customer_id"
    empty = tmp_path / "blank.txt"
    empty.write_text(" \n", encoding="utf-8")
    with pytest.raises(ValueError):
        module.read_required_text(empty)
    with pytest.raises(ValueError):
        module.read_required_text(tmp_path / "missing.txt")


def check_customer_class(module: ModuleType, tmp_path: Path) -> None:
    customer = module.Customer("Alice", 188.5)
    assert customer.describe() == "Alice: 188.50"
    assert customer.annual_spending() == pytest.approx(2262.0)
    with pytest.raises(ValueError):
        module.Customer("", 10)
    with pytest.raises(ValueError):
        module.Customer("Alice", -1)


def check_order_class(module: ModuleType, tmp_path: Path) -> None:
    order = module.Order("Pen", 3, 2.5)
    assert order.total() == pytest.approx(7.5)
    assert order.describe() == "Pen × 3 = 7.50"
    zero_order = module.Order("Book", 0, 12)
    assert zero_order.total() == pytest.approx(0.0)
    with pytest.raises(ValueError):
        module.Order("", 1, 1)
    with pytest.raises(ValueError):
        module.Order("Pen", -1, 1)


def check_score_summary_class(module: ModuleType, tmp_path: Path) -> None:
    source_scores = [60, 80, 100]
    summary = module.ScoreSummary(source_scores)
    source_scores.append(0)
    assert summary.average() == pytest.approx(80.0)
    assert summary.highest() == pytest.approx(100.0)
    with pytest.raises(ValueError):
        module.ScoreSummary([])
    with pytest.raises(ValueError):
        module.ScoreSummary([101])


def check_build_customers(module: ModuleType, tmp_path: Path) -> None:
    customers = module.build_customers([("A", 10), ("B", 20)])
    assert [customer.describe() for customer in customers] == ["A: 10.00", "B: 20.00"]
    assert module.build_customers([]) == []
    with pytest.raises(ValueError):
        module.build_customers([("", 10)])


ANSWER_CASES: list[tuple[str, ModuleType, CheckFunction]] = [
    ("answer_01_convert_age", answer_01, check_convert_age),
    ("answer_01_convert_price", answer_01, check_convert_price),
    ("answer_01_order_amount", answer_01, check_calculate_order_amount),
    ("answer_01_order_summary", answer_01, check_build_order_summary),
    ("answer_02_unique_recent_items", answer_02, check_unique_recent_items),
    ("answer_02_average_score", answer_02, check_calculate_average_score),
    ("answer_02_unpack_order", answer_02, check_unpack_order),
    ("answer_02_common_customers", answer_02, check_find_common_customers),
    ("answer_03_count_categories", answer_03, check_count_categories),
    ("answer_03_customer_record", answer_03, check_build_customer_record),
    ("answer_03_required_value", answer_03, check_get_required_value),
    ("answer_03_merge_sales", answer_03, check_merge_monthly_sales),
    ("answer_04_classify_spending", answer_04, check_classify_spending),
    ("answer_04_count_churned", answer_04, check_count_churned),
    ("answer_04_valid_average", answer_04, check_calculate_valid_average),
    ("answer_04_first_large_order", answer_04, check_find_first_large_order),
    ("answer_05_order_total", answer_05, check_calculate_order_total),
    ("answer_05_growth_rate", answer_05, check_calculate_growth_rate),
    ("answer_05_summarize_scores", answer_05, check_summarize_scores),
    ("answer_05_customer_label", answer_05, check_format_customer_label),
    ("answer_06_data_path", answer_06, check_build_data_path),
    ("answer_06_processed_path", answer_06, check_build_processed_path),
    ("answer_06_figure_path", answer_06, check_build_figure_path),
    ("answer_06_directories", answer_06, check_get_project_directories),
    ("answer_07_first_line", answer_07, check_read_first_line),
    ("answer_07_nonempty_lines", answer_07, check_read_nonempty_lines),
    ("answer_07_write_report", answer_07, check_write_report),
    ("answer_07_count_csv", answer_07, check_count_csv_rows),
    ("answer_08_positive_amount", answer_08, check_parse_positive_amount),
    ("answer_08_optional_score", answer_08, check_parse_optional_score),
    ("answer_08_safe_divide", answer_08, check_safe_divide),
    ("answer_08_required_text", answer_08, check_read_required_text),
    ("answer_09_customer", answer_09, check_customer_class),
    ("answer_09_order", answer_09, check_order_class),
    ("answer_09_score_summary", answer_09, check_score_summary_class),
    ("answer_09_build_customers", answer_09, check_build_customers),
]

PRACTICE_CASES: list[tuple[str, ModuleType, CheckFunction]] = [
    ("practice_01_convert_age", practice_01, check_convert_age),
    ("practice_01_convert_price", practice_01, check_convert_price),
    ("practice_01_order_amount", practice_01, check_calculate_order_amount),
    ("practice_01_order_summary", practice_01, check_build_order_summary),
    ("practice_02_unique_recent_items", practice_02, check_unique_recent_items),
    ("practice_02_average_score", practice_02, check_calculate_average_score),
    ("practice_02_unpack_order", practice_02, check_unpack_order),
    ("practice_02_common_customers", practice_02, check_find_common_customers),
    ("practice_03_count_categories", practice_03, check_count_categories),
    ("practice_03_customer_record", practice_03, check_build_customer_record),
    ("practice_03_required_value", practice_03, check_get_required_value),
    ("practice_03_merge_sales", practice_03, check_merge_monthly_sales),
    ("practice_04_classify_spending", practice_04, check_classify_spending),
    ("practice_04_count_churned", practice_04, check_count_churned),
    ("practice_04_valid_average", practice_04, check_calculate_valid_average),
    ("practice_04_first_large_order", practice_04, check_find_first_large_order),
    ("practice_05_order_total", practice_05, check_calculate_order_total),
    ("practice_05_growth_rate", practice_05, check_calculate_growth_rate),
    ("practice_05_summarize_scores", practice_05, check_summarize_scores),
    ("practice_05_customer_label", practice_05, check_format_customer_label),
    ("practice_06_data_path", practice_06, check_build_data_path),
    ("practice_06_processed_path", practice_06, check_build_processed_path),
    ("practice_06_figure_path", practice_06, check_build_figure_path),
    ("practice_06_directories", practice_06, check_get_project_directories),
    ("practice_07_first_line", practice_07, check_read_first_line),
    ("practice_07_nonempty_lines", practice_07, check_read_nonempty_lines),
    ("practice_07_write_report", practice_07, check_write_report),
    ("practice_07_count_csv", practice_07, check_count_csv_rows),
    ("practice_08_positive_amount", practice_08, check_parse_positive_amount),
    ("practice_08_optional_score", practice_08, check_parse_optional_score),
    ("practice_08_safe_divide", practice_08, check_safe_divide),
    ("practice_08_required_text", practice_08, check_read_required_text),
    ("practice_09_customer", practice_09, check_customer_class),
    ("practice_09_order", practice_09, check_order_class),
    ("practice_09_score_summary", practice_09, check_score_summary_class),
    ("practice_09_build_customers", practice_09, check_build_customers),
]


@pytest.mark.parametrize(
    ("case_name", "module", "check"),
    ANSWER_CASES,
    ids=[case[0] for case in ANSWER_CASES],
)
def test_answer_contract(
    case_name: str,
    module: ModuleType,
    check: CheckFunction,
    tmp_path: Path,
) -> None:
    """参考答案必须满足完整题目契约。"""
    check(module, tmp_path)


@pytest.mark.parametrize(
    ("case_name", "module", "check"),
    PRACTICE_CASES,
    ids=[case[0] for case in PRACTICE_CASES],
)
def test_practice_contract(
    case_name: str,
    module: ModuleType,
    check: CheckFunction,
    tmp_path: Path,
) -> None:
    """未完成练习 xfail；学生实现后自动执行相同契约。"""
    try:
        check(module, tmp_path)
    except NotImplementedError as error:
        pytest.xfail(str(error))
