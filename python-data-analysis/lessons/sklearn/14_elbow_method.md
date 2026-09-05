# 第 14 节：用肘部法观察聚类数量

## 本节解决什么实际问题

KMeans 要提前给出簇数 `k`。分 2 组可能太粗，分 20 组又难以解释。肘部法比较不同 `k` 的组内距离，寻找“继续加组收益明显变小”的位置。

- **惯性（inertia）**：每个样本到所属质心的平方距离之和，越小表示组内越紧凑。
- **肘部法（elbow method）**：画出 `k` 与惯性，寻找下降曲线明显转缓、形似手肘的位置。

## 计算不同 k 的惯性

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array(
    [
        [0.0, 0.0],
        [0.1, 0.1],
        [5.0, 5.0],
        [5.1, 5.1],
        [10.0, 0.0],
        [10.1, 0.1],
    ]
)

inertias = []
for k in [1, 2, 3]:
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20,
    )
    model.fit(X)
    inertias.append(model.inertia_)

print(len(inertias))
print(inertias[0] > inertias[1] > inertias[2])
```

预期输出：

```text
3
True
```

随着 `k` 增大，惯性不会上升，因为更多质心总能让样本离中心不更远。但如果一直追求最低惯性，最终每个客户单独一组时惯性为 0，完全没有汇总价值。

## 计算每次增加一组的下降量

```python
inertias = [1200.0, 620.0, 310.0, 250.0, 220.0]
drops = [
    inertias[index - 1] - inertias[index]
    for index in range(1, len(inertias))
]

print(drops)
```

预期输出：

```text
[580.0, 310.0, 60.0, 30.0]
```

从 2 增到 3 仍减少 310，但从 3 增到 4 只减少 60，`k=3` 附近出现明显转折。这里是人为构造的清晰示例；真实曲线可能没有唯一肘部。

## 结果表要保留什么

```python
import pandas as pd

table = pd.DataFrame(
    {
        "k": [2, 3, 4],
        "inertia": [620.0, 310.0, 250.0],
    }
)
table["drop"] = table["inertia"].shift(1) - table["inertia"]

print(table["drop"].isna().tolist())
```

预期输出：

```text
[True, False, False]
```

第一个 `k` 没有前一个值可比较，下降量自然缺失。

## 肘部法的限制

- 有些数据没有明显拐点。
- 最紧凑的分组不一定最有业务价值。
- 不同标准化和特征选择会改变曲线。
- 应结合轮廓系数、簇大小、画像可解释性和业务可执行性。

## 常见错误

### 选择惯性最低的 k

惯性通常随 `k` 下降，因此这会偏向最大候选值。肘部法看的是边际收益何时明显变小。

### 每个 k 使用不同预处理

比较就失去意义。所有候选 `k` 必须使用同一份标准化特征。

### 候选 k 大于样本数

不能建立比样本更多的非空簇。先检查 `2 <= k <= 样本数 - 1`，便于后续评价。

## 与 IOM103 原项目的对应

原项目循环多个候选 `k`，记录 `KMeans.inertia_` 并绘制肘部图，为最终选择 5 个簇提供依据。详见 [原项目分析](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 对一组候选 `k` 计算惯性。
2. 计算相邻 `k` 的惯性下降量。
3. 构造包含 `k`、惯性和下降量的结果表。

## 运行命令

```powershell
python -m examples.sklearn.example_14_elbow_method
pytest tests/sklearn/test_sklearn_practice.py -k "14"
```

## 本节检查清单

- [ ] 我能解释惯性的含义。
- [ ] 我知道惯性为什么随 k 增大而不升。
- [ ] 我会观察下降速度，而不是直接选最低惯性。
- [ ] 我能计算相邻 k 的下降量。
- [ ] 我会结合其他指标和业务解释选择 k。
