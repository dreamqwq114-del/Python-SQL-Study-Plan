# 第 15 节：用轮廓系数评价聚类

## 本节解决什么实际问题

肘部图可能没有清晰拐点。轮廓系数同时检查“客户和自己组内成员是否接近”以及“与最近的其他组是否足够远”，为不同 `k` 提供另一个可比较分数。

- **凝聚度（cohesion）**：同一簇内部是否紧密。
- **分离度（separation）**：不同簇之间是否分开。
- **轮廓系数（silhouette score）**：结合凝聚度和分离度的指标，范围从 -1 到 1。

大致解释：

- 接近 1：样本与自己的簇很匹配，并远离其他簇。
- 接近 0：样本位于簇边界。
- 小于 0：一些样本可能分到了不合适的簇。

## 计算一个 k 的轮廓系数

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

X = np.array(
    [
        [0.0, 0.0],
        [0.1, 0.1],
        [5.0, 5.0],
        [5.1, 5.1],
    ]
)
labels = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=20,
).fit_predict(X)

score = silhouette_score(X, labels)
print(0.9 < score <= 1.0)
```

预期输出：

```text
True
```

两组点相距很远且组内接近，所以分数很高。

## 比较多个候选 k

```python
scores = {2: 0.61, 3: 0.72, 4: 0.58}
best_k = max(scores, key=scores.get)

print(best_k)
print(scores[best_k])
```

预期输出：

```text
3
0.72
```

当主要规则是最大轮廓系数时，候选中选择 `k=3`。如果多个 `k` 分数很接近，可以优先选择更容易解释、每组样本更充足的方案。

## 为什么不能计算 k=1

轮廓系数要比较“自己的簇”和“最近的其他簇”，所以至少需要两个簇。通常还要求簇数小于样本数，避免每个样本独占一簇。

```python
n_samples = 10
candidate_k = [2, 3, 9]
valid = [k for k in candidate_k if 2 <= k < n_samples]
print(valid)
```

预期输出：

```text
[2, 3, 9]
```

这里 9 在数学上可算，但业务上可能产生大量极小簇，因此还要检查每簇人数。

## 建立完整评价表

```python
import pandas as pd

evaluation = pd.DataFrame(
    {
        "k": [2, 3, 4],
        "inertia": [620.0, 310.0, 250.0],
        "silhouette": [0.61, 0.72, 0.58],
    }
)
print(evaluation.loc[evaluation["silhouette"].idxmax(), "k"])
```

预期输出：

```text
3
```

同时保留惯性、轮廓系数、簇规模和画像，比只报告一个“最佳 k”更容易复核。

## 常见错误

### 只选最高轮廓系数

最高分方案可能出现一个很小的孤立簇，难以采取行动。还要看簇大小和画像是否稳定、可解释。

### 在未标准化特征上比较

距离会被大尺度字段主导。所有候选 `k` 应使用同一份合理缩放的数据。

### 把簇编号当成结果含义

轮廓系数评价分组结构，不解释每组业务含义。仍需回到原始单位汇总特征，再命名画像。

## 与 IOM103 原项目的对应

原项目为各候选 `k` 计算 silhouette score，与肘部图共同选择聚类数量；最终建立 5 个簇并计算每组客户画像。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 对多个候选 `k` 计算轮廓系数。
2. 返回轮廓系数最高的 `k`，并验证输入。
3. 构造同时包含惯性和轮廓系数的评价表。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""用轮廓系数辅助选择聚类数量。"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

def build_evaluation_table() -> pd.DataFrame:
    """同时计算 inertia 和 silhouette。"""
    X, _ = make_blobs(
        n_samples=60,
        centers=3,
        cluster_std=0.45,
        random_state=42,
    )
    rows = []
    for k in [2, 3, 4]:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )
        labels = model.fit_predict(X)
        rows.append(
            {
                "k": k,
                "inertia": model.inertia_,
                "silhouette": silhouette_score(X, labels),
            }
        )
    return pd.DataFrame(rows)

def main() -> None:
    table = build_evaluation_table()
    best_k = int(table.loc[table["silhouette"].idxmax(), "k"])
    print(table["k"].tolist())
    print(best_k)
    print(table["silhouette"].between(-1, 1).all())

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/15_silhouette_score/test.py
```

## 本节检查清单

- [ ] 我能解释凝聚度、分离度和轮廓系数。
- [ ] 我知道轮廓系数的范围和大致含义。
- [ ] 我知道为什么 `k=1` 不能计算轮廓系数。
- [ ] 我会同时参考肘部、轮廓系数和簇大小。
- [ ] 我能在原始单位中解释最终客户簇。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>calculate_silhouette_scores</code></summary>

model.fit_predict(X) 后调用 silhouette_score。

</details>

<details>
<summary><code>select_best_silhouette_k</code></summary>

可以按 (-score, k) 排序，或用 max 的元组规则谨慎处理并列。

</details>

<details>
<summary><code>build_cluster_evaluation</code></summary>

每个 k 只需 fit_predict 一次，再读取 inertia_ 和计算轮廓系数。

</details>
