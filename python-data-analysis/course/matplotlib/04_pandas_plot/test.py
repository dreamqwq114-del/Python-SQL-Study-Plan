"""Matplotlib《Matplotlib 04：先用 Pandas 聚合，再绘制业务结果》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._figure_helpers import assert_image, capture_saved_figures
from . import answer
from . import practice

Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]

def check_04_plot_city_average(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"city": ["B", "A", "A"], "monthly_spending": [50, 100, 300]}
    )
    path = tmp_path / "nested" / "city_average.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_city_average(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Average Spending by City"
    assert axis["patch_heights"] == [200, 50]

def check_04_plot_contract_churn_rate(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {
            "contract_type": ["Monthly", "Monthly", "Yearly"],
            "churn": [1, 0, 0],
        }
    )
    path = tmp_path / "nested" / "contract_churn.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_contract_churn_rate(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Churn Rate by Contract"
    assert axis["patch_heights"] == [0.5, 0.0]
    assert axis["ylim"] == (0.0, 1.0)

def check_04_plot_monthly_order_totals(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {
            "order_date": ["2025-01-01", "2025/01/10", "2025-02-01", "bad"],
            "quantity": [2, 1, 1, 99],
            "unit_price": [50, 50, 80, 99],
        }
    )
    original = source.copy()
    path = tmp_path / "nested" / "monthly_orders.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_monthly_order_totals(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Monthly Order Totals"
    assert axis["line_y"] == [[150, 80]]
    pd.testing.assert_frame_equal(source, original)

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_04_plot_city_average", answer, check_04_plot_city_average),
    ("answer_04_plot_contract_churn_rate", answer, check_04_plot_contract_churn_rate),
    ("answer_04_plot_monthly_order_totals", answer, check_04_plot_monthly_order_totals),
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
