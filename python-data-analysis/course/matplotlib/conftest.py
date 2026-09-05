"""Matplotlib 各章共享的 pytest 配置与夹具。"""

import matplotlib
import matplotlib.pyplot as plt
import pytest

matplotlib.use("Agg")

@pytest.fixture(autouse=True)
def close_all_figures() -> None:
    plt.close("all")
    yield
    assert plt.get_fignums() == []
