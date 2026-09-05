"""Matplotlib《Matplotlib 01：根据问题选择折线图或柱状图》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._figure_helpers import assert_image, capture_saved_figures
from . import answer
from . import practice

Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]

def check_01_plot_city_counts(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"city": ["B", "A", "A", None]})
    original = source.copy()
    path = tmp_path / "nested" / "city.png"
    records = capture_saved_figures(monkeypatch)
    assert module.plot_city_counts(source, path) is None
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Customers by City"
    assert axis["xlabel"] == "City"
    assert axis["ylabel"] == "Customer Count"
    assert axis["patch_heights"] == [2, 1]
    assert records[0]["kwargs"]["dpi"] == 150
    pd.testing.assert_frame_equal(source, original)
    with pytest.raises(KeyError):
        module.plot_city_counts(pd.DataFrame({"town": ["A"]}), path)

def check_01_plot_monthly_sales(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"month": [2, 1], "sales": [150, 120]})
    path = tmp_path / "nested" / "sales.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_monthly_sales(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Monthly Sales Trend"
    assert axis["line_count"] == 1
    assert axis["line_x"] == [[1, 2]]
    assert axis["line_y"] == [[120, 150]]
    assert records[0]["kwargs"]["dpi"] == 150

def check_01_plot_sales_and_city_counts(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sales = pd.DataFrame({"month": [2, 1], "sales": [150, 120]})
    customers = pd.DataFrame({"city": ["B", "A", "A"]})
    path = tmp_path / "nested" / "dashboard.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_sales_and_city_counts(sales, customers, path)
    assert_image(path)
    axes = records[0]["axes"]
    assert len(axes) == 2
    assert [axis["title"] for axis in axes] == [
        "Monthly Sales",
        "Customers by City",
    ]
    assert axes[0]["line_x"] == [[1, 2]]
    assert axes[1]["patch_heights"] == [2, 1]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_plot_city_counts", answer, check_01_plot_city_counts),
    ("answer_01_plot_monthly_sales", answer, check_01_plot_monthly_sales),
    ("answer_01_plot_sales_and_city_counts", answer, check_01_plot_sales_and_city_counts),
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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    check(module, tmp_path, monkeypatch)


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
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    try:
        check(module, tmp_path, monkeypatch)
    except NotImplementedError:
        pytest.xfail(f"{name} 尚未完成")
