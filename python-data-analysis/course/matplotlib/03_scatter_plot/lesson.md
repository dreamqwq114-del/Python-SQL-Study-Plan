# Matplotlib 03：用散点图观察两个数值变量

## 本章解决什么实际问题

分析师想知道“年龄较大的客户是否消费更多”，分群完成后还想查看不同 Cluster 在收入—消费平面上的位置。散点图让每一行客户变成一个点，用横纵坐标同时表达两个数值。

散点图适合观察关系、群组和离群点，但仅凭图形不能证明一个变量导致另一个变量变化。

## 1. 一行数据对应一个点

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ages = [20, 30, 40]
spending = [100, 180, 140]
figure, axis = plt.subplots()
points = axis.scatter(ages, spending)

print(len(points.get_offsets()))
print(points.get_offsets().tolist())
plt.close(figure)
```

```text
3
[[20.0, 100.0], [30.0, 180.0], [40.0, 140.0]]
```

第一行客户对应 `(20, 100)`，第二行对应 `(30, 180)`。横纵坐标必须成对保持同一行关系。

## 2. 成对清理无效值

不能分别对年龄和消费 `dropna()` 后再强行组合，因为两列可能删除不同的行：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "age": [20, "bad", 40],
        "monthly_spending": [100, 200, "300"],
    }
)
points = pd.DataFrame(
    {
        "age": pd.to_numeric(customers["age"], errors="coerce"),
        "spending": pd.to_numeric(
            customers["monthly_spending"],
            errors="coerce",
        ),
    }
).dropna()

print(points.to_dict("records"))
```

```text
[{'age': 20.0, 'spending': 100}, {'age': 40.0, 'spending': 300}]
```

临时 DataFrame 保留原索引对齐，再统一删除任一坐标缺失的行。

## 3. 添加标题和轴标签

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

figure, axis = plt.subplots()
axis.scatter([20, 30], [100, 200])
axis.set_title("Age vs Monthly Spending")
axis.set_xlabel("Age")
axis.set_ylabel("Monthly Spending")

print(axis.get_title())
print(axis.get_xlabel())
print(axis.get_ylabel())
plt.close(figure)
```

```text
Age vs Monthly Spending
Age
Monthly Spending
```

没有标签的两个数字轴无法独立解释，报告图必须写清变量和含义。

## 4. 按群组绘制并添加图例

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

customers = pd.DataFrame(
    {
        "income": [30, 35, 80],
        "score": [70, 65, 20],
        "cluster": [0, 0, 1],
    }
)
figure, axis = plt.subplots()
for cluster in sorted(customers["cluster"].unique()):
    group = customers.loc[customers["cluster"] == cluster]
    axis.scatter(
        group["income"],
        group["score"],
        label=f"Cluster {cluster}",
    )
axis.legend()

labels = [text.get_text() for text in axis.get_legend().get_texts()]
sizes = [len(group.get_offsets()) for group in axis.collections]
print(labels)
print(sizes)
plt.close(figure)
```

```text
['Cluster 0', 'Cluster 1']
[2, 1]
```

每次 `scatter()` 创建一组点，图例说明颜色对应哪个聚类编号。编号只是算法标签，不天然表示好坏或高低。

## 5. 如何阅读而不过度结论

观察时可以问：

- 点整体向右上还是右下？
- 是否出现几个明显群组？
- 是否有远离其他点的离群点？
- 某个区域是否几乎没有数据？

散点图只能显示样本中的关系。要判断相关强度、因果或模型效果，还需要进一步分析。

## 6. 常见错误

### 错误一：横纵坐标长度不同

通常来自分别删除缺失值。把两列放进同一临时 DataFrame，再一次 `dropna()`。

### 错误二：把类别字符串直接当数值轴

散点图的两个主轴应该是数值变量。类别更适合用于颜色分组或图例。

### 错误三：没有图例解释群组

多次调用 `scatter()` 时给每组设置 `label`，最后调用 `legend()`。

### 错误四：把相关写成因果

年龄和消费一起变化不代表年龄导致消费变化。图形只是探索证据。

## 7. 与 IOM103 原项目的对应

原项目 Task B 在收入与消费得分平面上绘制客户散点，并用 Cluster 区分群组。这帮助解释 K-means 结果的空间结构。本节第三道练习使用同样的数据关系，但采用小型确定性数据和基础 Matplotlib。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `plot_age_spending()`：成对清理年龄与消费后绘制散点。
2. `plot_quantity_unit_price()`：观察订单数量与商品单价关系。
3. `plot_income_spending_by_cluster()`：按聚类编号绘制多组散点和图例。

## 9. 运行命令

```powershell
python -m course.matplotlib.03_scatter_plot.example
pytest course/matplotlib/03_scatter_plot/test.py
```

## 10. 本章检查清单

- 我能解释一行数据如何对应一个散点。
- 我会成对清理横纵坐标，避免数据错位。
- 我能为散点图设置明确标题和轴标签。
- 我能按类别分组绘点并添加图例。
- 我不会仅凭散点图声称因果关系。
