# Matplotlib 02：用直方图查看数值分布

## 本章解决什么实际问题

客户年龄有几十个不同数值。经理不想读完整名单，而想知道年龄主要集中在哪些区间、是否有很年轻或很年长的客户。直方图把连续数值切成若干区间，再统计每个区间有多少条记录。

直方图中的一个区间叫一个“箱”（bin）。`bins` 表示箱的数量或明确边界，不是样本数量。

## 1. 直方图与柱状图的区别

- 柱状图比较已经存在的类别，例如城市；
- 直方图把连续数值临时分箱，例如 20–29 岁、30–39 岁。

下面明确给出两个年龄区间：

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ages = [20, 21, 22, 40]
figure, axis = plt.subplots()
counts, boundaries, bars = axis.hist(
    ages,
    bins=[20, 30, 50],
    edgecolor="black",
)

print(counts.astype(int).tolist())
print(boundaries.astype(int).tolist())
print(len(bars))
plt.close(figure)
```

```text
[3, 1]
[20, 30, 50]
2
```

20、21、22 落入第一个箱，40 落入第二个箱。

## 2. 先把脏文本转为数值

CSV 中年龄可能混有无效文本。绘图前先清理：

```python
import pandas as pd

ages = pd.to_numeric(
    pd.Series(["20", "bad", 40, None]),
    errors="coerce",
).dropna()

print(ages.tolist())
print(len(ages))
```

```text
[20.0, 40.0]
2
```

`errors="coerce"` 把无法转换的值变成缺失值，`dropna()` 再排除它们。图形不能代替数据清洗。

## 3. `bins` 如何影响阅读

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

values = [10, 11, 12, 20, 21, 30]
figure, axes = plt.subplots(1, 2)
counts_two = axes[0].hist(values, bins=2)[0]
counts_three = axes[1].hist(values, bins=3)[0]

print(len(counts_two))
print(len(counts_three))
print(int(counts_two.sum()))
print(int(counts_three.sum()))
plt.close(figure)
```

```text
2
3
6
6
```

箱数改变分布细节，但有效样本总数仍为 6。箱太少会隐藏结构，箱太多会让小数据显得零碎。

## 4. 比较两个群体的分布

流失与未流失客户可以在同一 Axes 叠加，必须使用透明度和图例：

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

stayed = [20, 30, 40]
churned = [25, 35]
figure, axis = plt.subplots()
axis.hist(stayed, bins=3, alpha=0.6, label="Stayed")
axis.hist(churned, bins=3, alpha=0.6, label="Churned")
axis.legend()

legend = [text.get_text() for text in axis.get_legend().get_texts()]
print(legend)
print(len(axis.patches))
plt.close(figure)
```

```text
['Stayed', 'Churned']
6
```

每组 3 个箱，因此 Axes 中共有 6 个矩形。两组使用相同箱数，才容易比较。

## 5. 本章代码流程

```text
连续数值列
  ↓ pd.to_numeric(errors="coerce")
有效数值
  ↓ dropna()
选择合理 bins
  ↓ ax.hist()
设置标题和轴标签
  ↓ 保存并关闭
```

## 6. 常见错误

### 错误一：把 `bins=5` 理解为只画 5 个客户

它表示把数值范围切成 5 个区间，所有有效客户仍参与统计。

### 错误二：直接绘制字符串年龄

先安全转换为数值，否则图形可能报错或把文本当类别。

### 错误三：两个群体使用完全不同的区间

柱子位置无法对应。比较时应使用相同箱数，严谨分析还可显式提供同一组边界。

### 错误四：箱数为 0 或负数

没有实际意义。本课程练习要求 `bins <= 0` 时抛出 `ValueError`，且不创建文件。

## 7. 与 IOM103 原项目的对应

原始 IOM103 脚本没有绘制直方图。本节是为查看年龄、消费等连续变量分布补充的基础探索技能。后续模型和聚类仍会使用这些数值字段，但不能把本节图误写成原作业已有输出。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `plot_age_histogram()`：安全清理年龄并固定绘制 5 个箱。
2. `plot_spending_histogram()`：允许调用者指定正数箱数。
3. `plot_age_histograms_by_churn()`：叠加流失与未流失年龄分布。

## 9. 运行命令

```powershell
python -m course.matplotlib.02_histogram.example
pytest course/matplotlib/02_histogram/test.py
```

## 10. 本章检查清单

- 我能区分直方图的连续数值和柱状图的离散类别。
- 我能解释 bin 表示数值区间。
- 我会在绘图前转换数值并删除无效值。
- 我知道箱数会改变图形细节但不会改变有效样本总数。
- 我能用透明度和图例比较两个群体。
