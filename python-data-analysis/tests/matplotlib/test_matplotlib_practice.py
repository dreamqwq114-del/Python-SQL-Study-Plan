"""Matplotlib 6 节、18 道练习与答案的契约测试。"""

from pathlib import Path
from types import ModuleType
from typing import Callable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import pytest

from answers.matplotlib import answer_01_line_and_bar as answer_01
from answers.matplotlib import answer_02_histogram as answer_02
from answers.matplotlib import answer_03_scatter_plot as answer_03
from answers.matplotlib import answer_04_pandas_plot as answer_04
from answers.matplotlib import answer_05_labels_legends_layout as answer_05
from answers.matplotlib import answer_06_save_figures as answer_06
from practice.matplotlib import practice_01_line_and_bar as practice_01
from practice.matplotlib import practice_02_histogram as practice_02
from practice.matplotlib import practice_03_scatter_plot as practice_03
from practice.matplotlib import practice_04_pandas_plot as practice_04
from practice.matplotlib import practice_05_labels_legends_layout as practice_05
from practice.matplotlib import practice_06_save_figures as practice_06


Check = Callable[[ModuleType, Path, pytest.MonkeyPatch], None]


@pytest.fixture(autouse=True)
def close_all_figures() -> None:
    plt.close("all")
    yield
    assert plt.get_fignums() == []


def capture_saved_figures(
    monkeypatch: pytest.MonkeyPatch,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    original_savefig = Figure.savefig

    def savefig_spy(
        figure: Figure,
        filename: object,
        *args: object,
        **kwargs: object,
    ) -> object:
        axes_records = []
        for axis in figure.axes:
            legend = axis.get_legend()
            axes_records.append(
                {
                    "title": axis.get_title(),
                    "xlabel": axis.get_xlabel(),
                    "ylabel": axis.get_ylabel(),
                    "line_count": len(axis.lines),
                    "line_labels": [
                        line.get_label() for line in axis.lines
                    ],
                    "line_x": [
                        list(line.get_xdata()) for line in axis.lines
                    ],
                    "line_y": [
                        list(line.get_ydata()) for line in axis.lines
                    ],
                    "patch_heights": [
                        patch.get_height() for patch in axis.patches
                    ],
                    "collection_sizes": [
                        len(collection.get_offsets())
                        for collection in axis.collections
                    ],
                    "legend_labels": (
                        [text.get_text() for text in legend.get_texts()]
                        if legend is not None
                        else []
                    ),
                    "ylim": axis.get_ylim(),
                }
            )
        records.append(
            {
                "filename": Path(filename),
                "kwargs": dict(kwargs),
                "axes": axes_records,
                "suptitle": (
                    figure._suptitle.get_text()
                    if figure._suptitle is not None
                    else ""
                ),
            }
        )
        return original_savefig(figure, filename, *args, **kwargs)

    monkeypatch.setattr(Figure, "savefig", savefig_spy)
    return records


def assert_image(path: Path) -> None:
    assert path.exists()
    assert path.stat().st_size > 0


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


def check_02_plot_age_histogram(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"age": ["20", "bad", 40, None]})
    path = tmp_path / "nested" / "age.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_age_histogram(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Customer Age Distribution"
    assert len(axis["patch_heights"]) == 5
    assert sum(axis["patch_heights"]) == 2


def check_02_plot_spending_histogram(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"monthly_spending": ["100", "bad", 200, 300]}
    )
    path = tmp_path / "nested" / "spending.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_spending_histogram(source, path, 3)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert len(axis["patch_heights"]) == 3
    assert sum(axis["patch_heights"]) == 3
    invalid_path = tmp_path / "nested" / "invalid.png"
    with pytest.raises(ValueError):
        module.plot_spending_histogram(source, invalid_path, 0)
    assert not invalid_path.exists()


def check_02_plot_age_histograms_by_churn(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"age": [20, 30, 40, "bad"], "churn": [0, 1, 1, 0]}
    )
    path = tmp_path / "nested" / "age_churn.png"
    records = capture_saved_figures(monkeypatch)
    module.plot_age_histograms_by_churn(source, path)
    assert_image(path)
    axis = records[0]["axes"][0]
    assert axis["title"] == "Age Distribution by Churn"
    assert axis["legend_labels"] == ["Stayed", "Churned"]
    assert sum(axis["patch_heights"]) == 3


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


def check_06_save_churn_figure(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"churn": [0, 1, 0, None]})
    path = tmp_path / "nested" / "churn.png"
    records = capture_saved_figures(monkeypatch)
    module.save_churn_figure(source, path)
    assert_image(path)
    assert records[0]["kwargs"]["dpi"] >= 120
    assert records[0]["kwargs"]["bbox_inches"] == "tight"
    assert records[0]["axes"][0]["patch_heights"] == [2, 1]


def check_06_save_transparent_spending_scatter(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame(
        {"age": [20, 30], "monthly_spending": [100, 200]}
    )
    path = tmp_path / "transparent" / "spending.png"
    records = capture_saved_figures(monkeypatch)
    module.save_transparent_spending_scatter(source, path)
    assert_image(path)
    assert records[0]["kwargs"]["dpi"] == 200
    assert records[0]["kwargs"]["transparent"] is True
    assert records[0]["kwargs"]["bbox_inches"] == "tight"


def check_06_save_city_figure_formats(
    module: ModuleType,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pd.DataFrame({"city": ["B", "A", "A"]})
    output_directory = tmp_path / "formats"
    records = capture_saved_figures(monkeypatch)
    paths = module.save_city_figure_formats(source, output_directory)
    assert paths == [
        output_directory / "city_counts.png",
        output_directory / "city_counts.pdf",
    ]
    assert len(records) == 2
    for path in paths:
        assert_image(path)
    assert [record["filename"].suffix for record in records] == [".png", ".pdf"]
    assert all(record["kwargs"]["dpi"] == 150 for record in records)
    assert records[0]["axes"][0]["patch_heights"] == [2, 1]


ANSWER_CASES: list[tuple[str, ModuleType, Check]] = [
    ("answer_01_plot_city_counts", answer_01, check_01_plot_city_counts),
    ("answer_01_plot_monthly_sales", answer_01, check_01_plot_monthly_sales),
    (
        "answer_01_plot_sales_and_city_counts",
        answer_01,
        check_01_plot_sales_and_city_counts,
    ),
    ("answer_02_plot_age_histogram", answer_02, check_02_plot_age_histogram),
    (
        "answer_02_plot_spending_histogram",
        answer_02,
        check_02_plot_spending_histogram,
    ),
    (
        "answer_02_plot_age_histograms_by_churn",
        answer_02,
        check_02_plot_age_histograms_by_churn,
    ),
    ("answer_03_plot_age_spending", answer_03, check_03_plot_age_spending),
    (
        "answer_03_plot_quantity_unit_price",
        answer_03,
        check_03_plot_quantity_unit_price,
    ),
    (
        "answer_03_plot_income_spending_by_cluster",
        answer_03,
        check_03_plot_income_spending_by_cluster,
    ),
    ("answer_04_plot_city_average", answer_04, check_04_plot_city_average),
    (
        "answer_04_plot_contract_churn_rate",
        answer_04,
        check_04_plot_contract_churn_rate,
    ),
    (
        "answer_04_plot_monthly_order_totals",
        answer_04,
        check_04_plot_monthly_order_totals,
    ),
    (
        "answer_05_plot_order_status_lines",
        answer_05,
        check_05_plot_order_status_lines,
    ),
    (
        "answer_05_plot_online_and_store_sales",
        answer_05,
        check_05_plot_online_and_store_sales,
    ),
    (
        "answer_05_plot_customer_dashboard",
        answer_05,
        check_05_plot_customer_dashboard,
    ),
    ("answer_06_save_churn_figure", answer_06, check_06_save_churn_figure),
    (
        "answer_06_save_transparent_spending_scatter",
        answer_06,
        check_06_save_transparent_spending_scatter,
    ),
    (
        "answer_06_save_city_figure_formats",
        answer_06,
        check_06_save_city_figure_formats,
    ),
]


practice_modules = [
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
]

PRACTICE_CASES: list[tuple[str, ModuleType, Check]] = [
    (name.replace("answer_", "practice_"), practice, check)
    for (name, _, check), practice in zip(ANSWER_CASES, practice_modules)
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
