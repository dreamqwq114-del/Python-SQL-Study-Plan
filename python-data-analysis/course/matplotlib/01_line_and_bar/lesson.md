# Matplotlib 01：根据问题选择折线图或柱状图

## 本章解决什么实际问题

销售经理提出两个问题：

1. 一月至三月的销售额怎样变化？
2. 苏州、上海、无锡哪个城市客户最多？

第一个问题有明确的时间顺序，适合折线图；第二个问题比较离散类别，适合柱状图。本章不是只记两个函数，而是先判断分析问题，再选图。

## 1. Figure 和 Axes 是什么

Matplotlib 中：

- `Figure` 是整张画布；
- `Axes` 是画布中的一个绘图区；
- 一张 Figure 可以放一个或多个 Axes。

第一次出现的 `Axes` 不是“坐标轴标签”，而是包含标题、横纵轴和图形元素的完整绘图区。

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axis = plt.subplots()

print(len(figure.axes))
print(axis is figure.axes[0])
plt.close(figure)
print(len(plt.get_fignums()))
```

```text
1
True
0
```

`Agg` 是不需要弹出窗口的绘图后端，适合自动测试和保存图片。`plt.close(figure)` 后未关闭图形数量为 0。

## 2. 折线图：展示有顺序的变化

月份有先后顺序，先排序再画线：

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sales = pd.DataFrame(
    {"month": [3, 1, 2], "sales": [135, 120, 150]}
).sort_values("month")

figure, axis = plt.subplots()
line = axis.plot(
    sales["month"],
    sales["sales"],
    marker="o",
)[0]
axis.set_title("Monthly Sales Trend")

print([int(value) for value in line.get_xdata()])
print([int(value) for value in line.get_ydata()])
print(axis.get_title())
plt.close(figure)
```

```text
[1, 2, 3]
[120, 150, 135]
Monthly Sales Trend
```

`marker="o"` 在每个真实数据点放一个圆点，帮助读者看清哪些位置有观测值。折线连接顺序由传入数据顺序决定，因此月份必须先排序。

## 3. 柱状图：比较离散类别

城市没有连续时间含义，柱子的高度表示每类数量：

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

customers = pd.DataFrame(
    {"city": ["Shanghai", "Suzhou", "Suzhou", "Wuxi"]}
)
counts = customers["city"].value_counts().sort_index()

figure, axis = plt.subplots()
bars = axis.bar(counts.index, counts.values)
axis.set_title("Customers by City")

print(counts.to_dict())
print([int(bar.get_height()) for bar in bars])
plt.close(figure)
```

```text
{'Shanghai': 1, 'Suzhou': 2, 'Wuxi': 1}
[1, 2, 1]
```

先用 pandas 得到正确计数，再让 Matplotlib 负责表达结果。不要把未聚合的城市明细直接当成柱高。

## 4. 用子图同时展示两个问题

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axes = plt.subplots(1, 2, figsize=(8, 3))
axes[0].plot([1, 2, 3], [120, 150, 135], marker="o")
axes[0].set_title("Monthly Sales")
axes[1].bar(["A", "B"], [2, 1])
axes[1].set_title("Customers by City")
figure.tight_layout()

print(len(figure.axes))
print([axis.get_title() for axis in axes])
plt.close(figure)
```

```text
2
['Monthly Sales', 'Customers by City']
```

`plt.subplots(1, 2)` 创建一行两列的布局。`tight_layout()` 自动调整子图间距，减少文字重叠。

## 5. 选图判断

```text
问题强调时间、步骤、连续顺序变化
                    → 折线图

问题强调不同城市、商品、合同等类别大小
                    → 柱状图
```

折线会暗示相邻点之间存在连续变化，所以不要用它连接没有自然顺序的城市。

## 6. 常见错误

### 错误一：月份没有排序

数据顺序为 3、1、2 时，折线会来回折返。先 `sort_values("month")`。

### 错误二：城市标签和计数顺序不一致

横轴标签和柱高必须来自同一个已排序 Series：`counts.index` 与 `counts.values`。

### 错误三：反复创建图却不关闭

批量画图会持续占用内存。保存后使用 `plt.close(figure)`，而不是只写 `plt.close()` 后猜测关闭了哪一张。

### 错误四：使用折线比较无顺序类别

城市 A 到城市 B 之间没有连续路径含义，柱状图更合适。

## 7. 与 IOM103 原项目的对应

原项目 Task A2 用柱状图比较不同合同类型的流失率；Task B 用折线图展示聚类数量变化时的 Inertia 和 Silhouette Score。两者的区别正是“类别比较”与“有顺序的 k 值变化”。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `plot_city_counts()`：按城市名称排序并绘制客户计数柱状图。
2. `plot_monthly_sales()`：按月份排序并绘制带圆点的销售折线。
3. `plot_sales_and_city_counts()`：在两个子图中组合折线图和柱状图。

每道题的标题、轴标签、DPI、边界情况和提示都写在 [practice_01_line_and_bar.py](practice.py) 中。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""在两个子图中展示销售趋势和城市客户数量。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

def create_sales_dashboard(
    sales: pd.DataFrame,
    customers: pd.DataFrame,
    output_path: Path,
) -> None:
    """创建折线图与柱状图组成的报告。"""
    ordered = sales.sort_values("month")
    city_counts = customers["city"].value_counts().sort_index()
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(ordered["month"], ordered["sales"], marker="o")
    axes[0].set(
        title="Monthly Sales",
        xlabel="Month",
        ylabel="Sales",
    )
    axes[1].bar(city_counts.index, city_counts.values)
    axes[1].set(
        title="Customers by City",
        xlabel="City",
        ylabel="Customer Count",
    )
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)

def main() -> None:
    sales = pd.DataFrame(
        {"month": [3, 1, 2], "sales": [135, 120, 150]}
    )
    customers = pd.DataFrame({"city": ["Suzhou", "Wuxi", "Suzhou"]})
    with TemporaryDirectory() as directory:
        target = Path(directory) / "line_and_bar.png"
        create_sales_dashboard(sales, customers, target)
        print(target.name)
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/matplotlib/01_line_and_bar/test.py
```

练习未完成时显示 3 个 `XFAIL` 是正常现象。

## 10. 本章检查清单

- 我能解释 Figure 与 Axes 的关系。
- 我会根据“趋势”或“类别比较”选择图形。
- 我会在画折线前按顺序字段排序。
- 我能从同一计数 Series 取得类别标签和柱高。
- 我会保存后关闭自己创建的 Figure。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>plot_city_counts</code></summary>

value_counts().sort_index() 得到计数，使用 ax.bar() 绘图。

</details>

<details>
<summary><code>plot_monthly_sales</code></summary>

sort_values("month") 后使用 ax.plot(..., marker="o")。

</details>

<details>
<summary><code>plot_sales_and_city_counts</code></summary>

fig, axes = plt.subplots(1, 2)，分别使用 axes[0] 和 axes[1]。

</details>
