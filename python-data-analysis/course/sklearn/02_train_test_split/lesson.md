# 第 2 节：划分训练集和测试集

## 本节解决什么实际问题

如果用全部客户训练模型，又用同一批客户给模型打分，模型可能只记住训练数据。为了判断它能否处理从未见过的新客户，需要在训练前留出一部分数据作为测试集。

- **训练集（training set）**：供模型学习的数据。
- **测试集（test set）**：训练时不能看到，只在最后评估时使用。
- **泛化（generalization）**：模型把学到的规律应用到新数据的能力。

## 基本划分

`train_test_split` 会按相同位置同时划分 `X` 和 `y`：

```python
import pandas as pd
from sklearn.model_selection import train_test_split

X = pd.DataFrame({"customer_number": range(8)})
y = pd.Series([0, 1, 0, 1, 0, 1, 0, 1], name="churn")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

print(len(X_train), len(X_test))
print(len(y_train), len(y_test))
```

预期输出：

```text
6 2
6 2
```

`test_size=0.25` 表示把 25% 的样本留作测试；其余 75% 用于训练。

## random_state 是什么

划分前会随机打乱行。`random_state` 是**随机种子**：它固定伪随机过程的起点，使同样的代码每次得到同样的划分，便于复现和排错。

```python
from sklearn.model_selection import train_test_split

values = list(range(10))
first_train, first_test = train_test_split(
    values, test_size=0.2, random_state=42
)
second_train, second_test = train_test_split(
    values, test_size=0.2, random_state=42
)

print(first_test)
print(first_test == second_test)
```

预期输出：

```text
[8, 1]
True
```

固定随机种子不是取消随机，而是让随机结果可重复。

## 为什么二分类要分层

`stratify=y` 表示**分层抽样**：尽量让训练集和测试集保持原标签比例。

```python
import pandas as pd
from sklearn.model_selection import train_test_split

X = pd.DataFrame({"customer_number": range(40)})
y = pd.Series([0, 1] * 20, name="churn")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42,
)

print(len(X_train), len(X_test))
print(y_train.mean(), y_test.mean())
```

预期输出：

```text
30 10
0.5 0.5
```

标签只有 `0/1` 时，平均值就是 `1` 的比例。两个 `0.5` 说明训练集和测试集都含一半流失客户。

## 正确的数据流

1. 先得到完整的 `X` 和 `y`。
2. 立刻划分训练集和测试集。
3. 只用训练集学习清洗参数和模型参数。
4. 把同样规则应用到测试集。
5. 最后在测试集上评估一次。

## 常见错误

### 先标准化全体数据再划分

这样测试集的均值和标准差会提前进入训练过程，属于数据泄漏。正确做法是先划分，再用 `X_train` 拟合缩放器。

### 忘记同时传入 X 和 y

分别随机划分会使客户行和标签错位。应在一次 `train_test_split(X, y, ...)` 调用中一起划分。

### 小数据无法分层

如果某个类别只有一个样本，就无法同时分到训练集和测试集。应先检查类别计数，收集更多样本或调整测试比例，而不是悄悄删除 `stratify`。

## 与 IOM103 原项目的对应

原项目使用 `test_size=0.25`、`stratify=y` 和 `random_state=42`，即 75% 训练、25% 测试，并保持流失比例。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 按固定规则分层划分客户数据。
2. 接收调用者给出的测试比例。
3. 汇总训练集和测试集的样本数及正类比例。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""使用固定随机种子进行分层训练/测试划分。"""

import pandas as pd
from sklearn.model_selection import train_test_split

def split_customer_data(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """按 75%/25% 分层划分数据。"""
    return train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )

def main() -> None:
    X = pd.DataFrame({"customer_number": range(40)})
    y = pd.Series([0, 1] * 20, name="churn")
    X_train, X_test, y_train, y_test = split_customer_data(X, y)
    print((len(X_train), len(X_test)))
    print((y_train.mean(), y_test.mean()))
    print(sorted(X_test["customer_number"].tolist())[:3])

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/02_train_test_split/test.py
```

## 本节检查清单

- [ ] 我能解释训练集和测试集的不同职责。
- [ ] 我知道为什么不能用测试集帮助训练。
- [ ] 我能解释 `test_size`、`stratify` 和 `random_state`。
- [ ] 我能检查划分后的行数和标签比例。
- [ ] 我会先划分，再拟合预处理器。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>split_data</code></summary>

train_test_split(..., test_size=0.25, stratify=y, random_state=42)。

</details>

<details>
<summary><code>split_with_test_size</code></summary>

先验证比例，再调用 train_test_split。

</details>

<details>
<summary><code>summarize_split_balance</code></summary>

0/1 Series 的 mean() 就是正类比例。

</details>
