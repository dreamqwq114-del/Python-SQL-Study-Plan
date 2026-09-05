"""Matplotlib《Matplotlib 05：让图形脱离代码也能读懂》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._figure_helpers import assert_image, capture_saved_figures
from . import answer
from . import practice

Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]

def check_05_plot_order_status_lines(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {
            "status": ["refunded", "paid", "paid"],
            "order_amount": [20, 50, 70],
        }
    )
    path = tmp_path / "nested" / "status.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_order_status_lines(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["legend_labels"] == ["paid", "refunded"]
    assert axis["line_x"] == [[1, 2], [1]]
    assert axis["line_y"] == [[50, 70], [20]]

def check_05_plot_online_and_store_sales(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {
            "month": [2, 1],
            "online_sales": [200, 100],
            "store_sales": [150, 120],
        }
    )
    path = tmp_path / "nested" / "channels.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_online_and_store_sales(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["legend_labels"] == ["Online", "Store"]
    assert axis["line_x"] == [[1, 2], [1, 2]]
    assert axis["line_y"] == [[100, 200], [120, 150]]

def check_05_plot_customer_dashboard(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"city": ["B", "A", "A"], "churn": [1, 0, 0]}
    )
    path = tmp_path / "nested" / "customer_dashboard.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_customer_dashboard(source, path)
    assert_image(path)
    assert records[0]["suptitle"] == "Customer Overview"
    axes = records[0]["axes"]
    assert len(axes) == 2
    assert axes[0]["patch_heights"] == [2, 1]
    assert axes[1]["patch_heights"] == [2, 1]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_05_plot_order_status_lines", answer, check_05_plot_order_status_lines),
    ("answer_05_plot_online_and_store_sales", answer, check_05_plot_online_and_store_sales),
    ("answer_05_plot_customer_dashboard", answer, check_05_plot_customer_dashboard),
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
