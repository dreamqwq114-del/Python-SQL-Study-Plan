"""Matplotlib 多章测试共享的构造辅助函数。"""

from pathlib import Path
from matplotlib.figure import Figure
import pytest

def assert_image(path: Path) -> None:
    assert path.exists()
    assert path.stat().st_size > 0

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
