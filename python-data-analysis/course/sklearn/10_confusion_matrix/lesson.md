# 第 10 节：用混淆矩阵看清四种分类结果

## 本节解决什么实际问题

单个分数不能告诉客户经理模型究竟错在哪里。混淆矩阵把预测拆成正确保留、误报流失、漏报流失、正确发现流失四类，便于计算业务代价。

**混淆矩阵（confusion matrix）**是实际类别与预测类别的交叉计数表。本课程固定标签顺序 `[0, 1]`，矩阵布局是：

```text
[[TN, FP],
 [FN, TP]]
```

## 计算矩阵

```python
from sklearn.metrics import confusion_matrix

y_true = [0, 0, 1, 1]
y_pred = [0, 1, 0, 1]

matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
print(matrix.tolist())
```

预期输出：

```text
[[1, 1], [1, 1]]
```

四个格子都是 1：一位未流失客户判断正确，一位被误报；一位流失客户被漏掉，一位判断正确。

## 拆出 TN、FP、FN、TP

```python
from sklearn.metrics import confusion_matrix

y_true = [0, 0, 0, 1, 1]
y_pred = [0, 1, 0, 0, 1]

tn, fp, fn, tp = confusion_matrix(
    y_true, y_pred, labels=[0, 1]
).ravel()

print({"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)})
```

预期输出：

```text
{'tn': 2, 'fp': 1, 'fn': 1, 'tp': 1}
```

`ravel()` 按行把 2×2 矩阵展开。只有明确传入 `labels=[0, 1]` 后，才能可靠地按这个顺序解释。

## 归一化矩阵

原始计数适合计算总成本；按真实类别归一化后，每一行变成比例，更适合类别数量不同时比较：

```python
import numpy as np
from sklearn.metrics import confusion_matrix

y_true = [0, 0, 0, 1]
y_pred = [0, 1, 0, 1]
matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1],
    normalize="true",
)

print(np.round(matrix, 3).tolist())
```

预期输出：

```text
[[0.667, 0.333], [0.0, 1.0]]
```

第一行表示真实未流失客户中约 66.7% 判断正确、33.3% 被误报；第二行表示真实流失客户全部找回。

## 把错误转换成业务成本

如果一次无效联系成本为 5 元，漏掉一位流失客户损失为 100 元，可计算：

```python
false_positives = 8
false_negatives = 3
cost = false_positives * 5 + false_negatives * 100
print(cost)
```

预期输出：

```text
340
```

这能帮助团队选择阈值，而不是只追求一个抽象分数。

## 常见错误

### 记反 FP 和 FN

先看“真实情况”，再看“模型预测”。FP 是把负类错报成正类；FN 是把正类漏报成负类。

### 不固定标签顺序

当某个类别缺失时，矩阵形状可能变化。二分类课程中显式传入 `labels=[0, 1]`。

### 归一化矩阵当作人数

归一化结果是比例，不是客户数。汇报时应写清单位。

## 与 IOM103 原项目的对应

原项目为表现最好的分类模型绘制混淆矩阵，用它检查流失与未流失客户的具体预测情况。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 构建固定顺序的 2×2 混淆矩阵。
2. 返回 TN、FP、FN、TP 四个整数。
3. 构建按真实类别归一化的矩阵。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""把分类结果整理为混淆矩阵与四个计数。"""

import numpy as np
from sklearn.metrics import confusion_matrix

def build_counts() -> tuple[np.ndarray, dict[str, int]]:
    """返回固定示例的矩阵和 TN/FP/FN/TP。"""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 0, 1])
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    counts = {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }
    return matrix, counts

def main() -> None:
    matrix, counts = build_counts()
    print(matrix.tolist())
    print(counts)
    print(matrix.shape)

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/10_confusion_matrix/test.py
```

## 本节检查清单

- [ ] 我能画出 `[[TN, FP], [FN, TP]]` 的位置。
- [ ] 我能区分误报和漏报。
- [ ] 我会显式指定标签顺序。
- [ ] 我能区分计数矩阵和比例矩阵。
- [ ] 我能把 FP、FN 转换成业务成本。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>build_confusion_matrix</code></summary>

confusion_matrix(y_true, y_pred, labels=[0, 1])。

</details>

<details>
<summary><code>confusion_counts</code></summary>

对 2×2 数组使用 .ravel()，再把值转为 int。

</details>

<details>
<summary><code>normalized_confusion_matrix</code></summary>

confusion_matrix(..., labels=[0,1], normalize="true")。

</details>
