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

原项目使用 `test_size=0.25`、`stratify=y` 和 `random_state=42`，即 75% 训练、25% 测试，并保持流失比例。详见 [原项目分析](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 按固定规则分层划分客户数据。
2. 接收调用者给出的测试比例。
3. 汇总训练集和测试集的样本数及正类比例。

## 运行命令

```powershell
python -m examples.sklearn.example_02_train_test_split
pytest tests/sklearn/test_sklearn_practice.py -k "02"
```

## 本节检查清单

- [ ] 我能解释训练集和测试集的不同职责。
- [ ] 我知道为什么不能用测试集帮助训练。
- [ ] 我能解释 `test_size`、`stratify` 和 `random_state`。
- [ ] 我能检查划分后的行数和标签比例。
- [ ] 我会先划分，再拟合预处理器。
