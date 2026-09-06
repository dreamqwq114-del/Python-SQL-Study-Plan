# Matplotlib 04：先用 Pandas 聚合，再绘制业务结果

## 本章解决什么实际问题

客户表一行一个客户，经理要比较“各城市平均消费”和“各合同流失率”。如果直接画明细，会出现很多重复城市，图形回答不了问题。本章先用 pandas 把数据聚合成每组一个结果，再用 `.plot()` 作为 Matplotlib 的便捷入口。

`Series.plot()` 和 `DataFrame.plot()` 最终仍创建 Matplotlib Axes，所以标题、标签、保存和关闭方法相同。

## 1. 为什么先聚合

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "city": ["A", "A", "B"],
        "monthly_spending": [100, 300, 50],
    }
)
summary = (
    customers.groupby("city")["monthly_spending"]
    .mean()
    .sort_index()
)

print(customers.shape)
print(summary.to_dict())
```

```text
(3, 2)
{'A': 200.0, 'B': 50.0}
```

明细有 3 行，聚合后每个城市只有一个平均值。图形应该画 `summary`，不是原始三行。

## 2. 用 `Series.plot.bar()` 绘制聚合结果

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

summary = pd.Series(
    {"A": 200.0, "B": 50.0},
    name="monthly_spending",
)
figure, axis = plt.subplots()
summary.plot.bar(ax=axis)
axis.set_title("Average Spending by City")
axis.set_xlabel("City")
axis.set_ylabel("Average Monthly Spending")

print([float(bar.get_height()) for bar in axis.patches])
print(axis.get_title())
plt.close(figure)
```

```text
[200.0, 50.0]
Average Spending by City
```

`ax=axis` 明确告诉 pandas 把图画在哪个 Axes 上，后续能稳定控制和关闭这张 Figure。

## 3. 0/1 平均值绘制流失率

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

customers = pd.DataFrame(
    {
        "contract": ["Monthly", "Monthly", "Yearly"],
        "churn": [1, 0, 0],
    }
)
rate = (
    customers.groupby("contract")["churn"]
    .mean()
    .sort_values(ascending=False)
)
figure, axis = plt.subplots()
rate.plot.bar(ax=axis)
axis.set_ylim(0, 1)

print(rate.to_dict())
print(tuple(float(value) for value in axis.get_ylim()))
plt.close(figure)
```

```text
{'Monthly': 0.5, 'Yearly': 0.0}
(0.0, 1.0)
```

比例的完整范围是 0 到 1。固定纵轴范围可以避免 0.5 的柱子看起来像“满格”。

## 4. 月度订单金额折线

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.DataFrame(
    {
        "order_month": ["2025-01", "2025-01", "2025-02"],
        "order_total": [100, 50, 80],
    }
)
summary = (
    orders.groupby("order_month")["order_total"]
    .sum()
    .sort_index()
)
figure, axis = plt.subplots()
summary.plot(ax=axis, marker="o")

print(summary.to_dict())
print([int(value) for value in axis.lines[0].get_ydata()])
plt.close(figure)
```

```text
{'2025-01': 150, '2025-02': 80}
[150, 80]
```

月份有顺序，因此聚合后用折线图。`.plot()` 默认绘制折线。

## 5. 本章代码流程

```text
明细 DataFrame
  ↓ 清理类型和类别
groupby + mean / sum / count
  ↓ sort_index 或 sort_values
每组一个值的 Series
  ↓ Series.plot.bar() 或 Series.plot()
Matplotlib Axes
  ↓ 设置标题、轴标签、保存、关闭
```

## 6. 常见错误

### 错误一：直接对明细类别绘图

同一城市重复出现，柱子不代表城市平均值。先明确问题，再聚合。

### 错误二：聚合方法不符合问题

客户数量用 `count` 或 `nunique`，金额总量用 `sum`，平均消费用 `mean`。图画得漂亮不能修复错误统计。

### 错误三：流失率纵轴自动缩放

比例图固定 `set_ylim(0, 1)`，不同图才可公平比较。

### 错误四：让 pandas 自动创建图后不知道如何关闭

推荐先 `figure, axis = plt.subplots()`，再把 `ax=axis` 传给 `.plot()`。

## 7. 与 IOM103 原项目的对应

原项目先按合同聚合流失率，再画合同流失率柱状图；Task B 也先生成 Cluster 汇总表，再绘制分群概览。原脚本没有直接调用 pandas `.plot()`，本节教授的是生成同类图表的便捷入口，聚合逻辑与原分析一致。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `plot_city_average()`：城市平均消费聚合后绘柱状图。
2. `plot_contract_churn_rate()`：合同流失率降序图并固定 0–1 纵轴。
3. `plot_monthly_order_totals()`：清理日期、汇总金额并绘月度折线。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""先用 pandas 聚合，再通过 pandas 绘图入口保存柱状图。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR

def save_city_average_plot(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> pd.Series:
    """保存城市平均消费图并返回聚合结果。"""
    result = dataframe.copy()
    result["city"] = result["city"].str.strip().str.lower()
    result["monthly_spending"] = pd.to_numeric(
        result["monthly_spending"],
        errors="coerce",
    )
    summary = (
        result.groupby("city")["monthly_spending"]
        .mean()
        .sort_index()
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(6, 4))
    summary.plot.bar(ax=axis)
    axis.set(
        title="Average Spending by City",
        xlabel="City",
        ylabel="Average Monthly Spending",
    )
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    return summary

def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        target = Path(directory) / "city_average.png"
        summary = save_city_average_plot(customers, target)
        print(summary.round(2).to_dict())
        print(target.exists() and target.stat().st_size > 0)
        print(len(plt.get_fignums()))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/matplotlib/04_pandas_plot/test.py
```

## 10. 本章检查清单

- 我会先明确图中一根柱或一个点代表什么。
- 我能在绘图前完成正确的分组聚合。
- 我会排序类别或月份，保证显示顺序合理。
- 我能把 pandas 绘图结果放到指定 Axes。
- 我知道统计正确比图形样式更重要。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>plot_city_average</code></summary>

groupby("city")["monthly_spending"].mean().sort_index().plot.bar()。

</details>

<details>
<summary><code>plot_contract_churn_rate</code></summary>

0/1 列分组后的 mean() 就是每组比例。

</details>

<details>
<summary><code>plot_monthly_order_totals</code></summary>

先生成 order_month，再 groupby().sum().sort_index().plot(marker="o")。

</details>
