# Matplotlib 05：让图形脱离代码也能读懂

## 本章解决什么实际问题

一张没有标题、坐标轴名称和图例的折线图，只有代码作者知道两条线表示什么。报告读者只看到图片，因此图必须自己说明“分析什么、横纵轴是什么、不同线代表谁”。本章补齐标题、轴标签、图例、网格和布局。

## 1. 标题与轴标签

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axis = plt.subplots()
axis.plot([1, 2], [50, 70])
axis.set_title("Order Amount by Status")
axis.set_xlabel("Order Sequence")
axis.set_ylabel("Order Amount")

print(axis.get_title())
print(axis.get_xlabel())
print(axis.get_ylabel())
plt.close(figure)
```

```text
Order Amount by Status
Order Sequence
Order Amount
```

标题说明问题，横纵轴标签说明数值含义。不要只写 `"Chart 1"` 或 `"Value"`。

## 2. 图例来自每条线的 `label`

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axis = plt.subplots()
axis.plot([1, 2], [50, 70], marker="o", label="Paid")
axis.plot([1, 2], [20, 10], marker="o", label="Refunded")
axis.legend()

labels = [text.get_text() for text in axis.get_legend().get_texts()]
print(labels)
print(len(axis.lines))
plt.close(figure)
```

```text
['Paid', 'Refunded']
2
```

先给每条线设置 `label`，再调用一次 `legend()`。图例顺序通常跟绘图顺序相同。

## 3. 网格帮助读数

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axis = plt.subplots()
axis.plot([1, 2, 3], [100, 150, 120])
axis.grid(alpha=0.3)

visible = any(line.get_visible() for line in axis.get_xgridlines())
print(visible)
plt.close(figure)
```

```text
True
```

浅色网格能帮助对齐数据点和刻度。透明度太高会抢走数据本身的注意力。

## 4. 多子图总标题和紧凑布局

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axes = plt.subplots(1, 2)
axes[0].set_title("Customers by City")
axes[1].set_title("Customers by Churn")
figure.suptitle("Customer Overview")
figure.tight_layout()

print(figure._suptitle.get_text())
print([axis.get_title() for axis in axes])
print(len(figure.axes))
plt.close(figure)
```

```text
Customer Overview
['Customers by City', 'Customers by Churn']
2
```

`suptitle()` 是整张 Figure 的总标题；每个 Axes 仍有自己的小标题。`tight_layout()` 调整子图和文字间距。

## 5. 两条业务折线的完整流程

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

months = [1, 2]
online = [100, 200]
store = [120, 150]
figure, axis = plt.subplots()
axis.plot(months, online, marker="o", label="Online")
axis.plot(months, store, marker="o", label="Store")
axis.set(
    title="Sales by Channel",
    xlabel="Month",
    ylabel="Sales",
)
axis.legend()
axis.grid(alpha=0.3)
figure.tight_layout()

print([line.get_label() for line in axis.lines])
print([
    [int(value) for value in line.get_ydata()]
    for line in axis.lines
])
plt.close(figure)
```

```text
['Online', 'Store']
[[100, 200], [120, 150]]
```

## 6. 常见错误

### 错误一：调用 `legend()` 却没有设置 label

图例没有可显示内容。每条需要解释的线都要设置业务名称。

### 错误二：图例名称与数据顺序不一致

标签必须在对应的那次 `plot()` 中传入，避免后面手写一个顺序错误的列表。

### 错误三：只设置标题，没有轴标签

标题不能替代变量和单位。横纵轴仍需清楚命名。

### 错误四：保存时文字被裁切

保存前调用 `figure.tight_layout()`，第 6 节还会使用 `bbox_inches="tight"`。

## 7. 与 IOM103 原项目的对应

原项目的合同流失率、ROC 曲线、聚类评估折线和客户分群散点图都设置了业务标题与轴标签；多模型 ROC 曲线和 Cluster 散点图还使用图例区分系列。本节把这些报告可读性要求拆成基础操作。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `plot_order_status_lines()`：每种状态一条线，图例来自状态名称。
2. `plot_online_and_store_sales()`：比较两个渠道并检查排序、图例和网格。
3. `plot_customer_dashboard()`：两个子图、各自标题和整图总标题。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""用完整标题、轴标签、图例和布局绘制订单状态折线。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR

def save_status_lines(dataframe: pd.DataFrame, output_path: Path) -> list[str]:
    """保存订单状态折线并返回图例标签。"""
    result = dataframe.copy()
    result["order_amount"] = result["quantity"] * result["unit_price"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(7, 4))
    labels = []
    for status, group in result.groupby("order_status", sort=True):
        labels.append(str(status))
        axis.plot(
            range(1, len(group) + 1),
            group["order_amount"],
            marker="o",
            label=str(status),
        )
    axis.set(
        title="Order Amount by Status",
        xlabel="Order Sequence",
        ylabel="Order Amount",
    )
    axis.legend()
    axis.grid(alpha=0.3)
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    return labels

def main() -> None:
    orders = pd.read_csv(DATA_DIR / "sample_orders.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "status_lines.png"
        labels = save_status_lines(orders, target)
        print(labels)
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/matplotlib/05_labels_legends_layout/test.py
```

## 10. 本章检查清单

- 我的图脱离代码后仍能说明业务问题。
- 每个数值轴都有明确标签。
- 多条线都在绘图时绑定正确 label。
- 我能区分 Axes 标题和 Figure 总标题。
- 我会使用浅色网格和紧凑布局提高可读性。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>plot_order_status_lines</code></summary>

groupby("status", sort=True) 后对每组调用 ax.plot(..., label=status)。

</details>

<details>
<summary><code>plot_online_and_store_sales</code></summary>

对排序后的同一 Axes 调用两次 plot()，并分别设置 label。

</details>

<details>
<summary><code>plot_customer_dashboard</code></summary>

plt.subplots(1, 2) 后分别使用 value_counts().sort_index()。

</details>
