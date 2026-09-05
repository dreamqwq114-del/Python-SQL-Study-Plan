"""Matplotlib《Matplotlib 03：用散点图观察两个数值变量》练习与参考答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable
import pandas as pd
import pytest

from .._figure_helpers import assert_image, capture_saved_figures
from . import answer
from . import practice

Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]

def check_03_plot_age_spending(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {
            "age": [20, "bad", 40],
            "monthly_spending": [100, 200, "300"],
        }
    )
    path = tmp_path / "nested" / "age_spending.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_age_spending(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Age vs Monthly Spending"
    assert axis["collection_sizes"] == [2]

def check_03_plot_quantity_unit_price(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"quantity": [1, 2], "unit_price": [99, 50]})
    path = tmp_path / "nested" / "quantity_price.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_quantity_unit_price(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Quantity vs Unit Price"
    assert axis["collection_sizes"] == [2]
    with pytest.raises(KeyError):
        module.plot_quantity_unit_price(pd.DataFrame({"quantity": [1]}), path)

def check_03_plot_income_spending_by_cluster(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {
            "annual_income": [30, 80, 35],
            "spending_score": [70, 20, 65],
            "cluster": [0, 1, 0],
        }
    )
    path = tmp_path / "nested" / "clusters.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_income_spending_by_cluster(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Customer Segments"
    assert axis["collection_sizes"] == [2, 1]
    assert axis["legend_labels"] == ["Cluster 0", "Cluster 1"]

ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_03_plot_age_spending", answer, check_03_plot_age_spending),
    ("answer_03_plot_quantity_unit_price", answer, check_03_plot_quantity_unit_price),
    ("answer_03_plot_income_spending_by_cluster", answer, check_03_plot_income_spending_by_cluster),
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
