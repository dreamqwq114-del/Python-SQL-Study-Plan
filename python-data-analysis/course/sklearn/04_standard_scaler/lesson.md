# 第 4 节：用 StandardScaler 统一数值尺度

## 本节解决什么实际问题

客户年龄可能在 18 到 80 之间，月消费额可能在几十到几千之间。某些模型会因消费额数字更大而过度受它影响。标准化把不同单位的数值转到可比较的尺度。

- **标准化（standardization）**：对每个特征执行 `(原值 - 训练均值) / 训练标准差`。
- **均值（mean）**：一组数的平均水平。
- **标准差（standard deviation）**：数据围绕均值的分散程度。
- **缩放器（scaler）**：保存均值和标准差，并按同一规则转换数据的对象。

## 标准化训练数据

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

train = np.array(
    [
        [20.0, 100.0],
        [30.0, 200.0],
        [40.0, 300.0],
    ]
)

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train)

print(np.round(train_scaled.mean(axis=0), 6).tolist())
print(np.round(train_scaled.std(axis=0), 6).tolist())
```

预期输出：

```text
[0.0, 0.0]
[1.0, 1.0]
```

`axis=0` 表示按列计算。标准化后，每列训练特征的均值约为 0，标准差约为 1。

## 测试集必须使用训练集参数

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

train = np.array([[20.0], [30.0], [40.0]])
test = np.array([[50.0]])

scaler = StandardScaler()
scaler.fit(train)

print(scaler.mean_.tolist())
print(np.round(scaler.transform(test), 3).tolist())
```

预期输出：

```text
[30.0]
[[2.449]]
```

测试值 50 使用训练均值 30 和训练标准差转换。不能对测试集再次 `fit`，因为那会利用未来数据的信息，也会改变坐标尺度。

## 标准化不会改变什么

标准化改变单位，不改变行数、列数和数值先后关系。它也不会自动处理文字或缺失值：

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

values = np.array([[100.0], [200.0], [300.0]])
scaled = StandardScaler().fit_transform(values)

print(values.shape == scaled.shape)
print(int(scaled.argmin()), int(scaled.argmax()))
```

预期输出：

```text
True
0 2
```

## 常见错误

### 在全体数据上 fit

测试集均值和标准差会泄漏到训练过程。应先划分，再 `scaler.fit(X_train)`，最后分别转换。

### 对类别编号标准化

城市独热列可以进入整体模型管道，但城市本身不是连续数值。原始文字列应先独热编码，不应强行转成数值再标准化。

### 认为所有模型都必须标准化

逻辑回归、KMeans 通常受尺度影响；决策树和随机森林按阈值分裂，对尺度不敏感。是否标准化取决于模型和业务流程。

## 与 IOM103 原项目的对应

流失分类流程把数值列交给 `StandardScaler`；聚类流程也对年龄、收入、消费评分标准化。所有缩放参数都应只从训练数据或当前聚类数据任务中学习。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 用训练集拟合缩放器并转换训练、测试数组。
2. 只标准化 DataFrame 中指定的数值列。
3. 汇总标准化后训练列的均值和标准差。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""用训练集参数标准化训练和测试特征。"""

import numpy as np
from sklearn.preprocessing import StandardScaler

def scale_train_and_test(
    train: np.ndarray,
    test: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """只在训练数组上拟合缩放器。"""
    scaler = StandardScaler()
    return scaler.fit_transform(train), scaler.transform(test)

def main() -> None:
    train = np.array([[20.0, 100.0], [30.0, 200.0], [40.0, 300.0]])
    test = np.array([[50.0, 400.0]])
    train_scaled, test_scaled = scale_train_and_test(train, test)
    print(np.round(train_scaled.mean(axis=0), 6).tolist())
    print(np.round(train_scaled.std(axis=0), 6).tolist())
    print(np.round(test_scaled, 3).tolist())

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/04_standard_scaler/test.py
```

## 本节检查清单

- [ ] 我能用公式解释标准化在做什么。
- [ ] 我知道标准化为什么有助于比较不同单位的特征。
- [ ] 我只用训练集拟合缩放器。
- [ ] 我能检查标准化后的均值和标准差。
- [ ] 我知道树模型不一定需要标准化。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>scale_features</code></summary>

scaler.fit_transform(train)，再 scaler.transform(test)。

</details>

<details>
<summary><code>scale_dataframe_columns</code></summary>

先 copy()，再用 .loc[:, columns] 写回缩放数组。

</details>

<details>
<summary><code>summarize_scaled_training</code></summary>

检查 ndim 和 size，再使用 np.mean(..., axis=0)。

</details>
