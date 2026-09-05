# 第 1 节：把客户表拆成特征 X 和标签 y

## 本节解决什么实际问题

假设公司想根据客户的年龄和月消费额，预测客户下个月是否会流失。原始表里既有可供模型参考的信息，也有模型最终要猜的答案。训练前必须把二者分开，否则模型会在输入中直接看到答案。

- **特征（feature）**：模型用来判断的信息，例如年龄、月消费额。scikit-learn 通常用大写 `X` 表示特征表。
- **标签（label）**：模型要预测的答案，例如 `churn` 是否流失。通常用小写 `y` 表示标签列。
- **样本（sample）**：表中的一行，即一位客户。
- **监督学习（supervised learning）**：训练数据同时提供特征和正确标签，让模型从例子中学习规律。

这里的 `X` 不是乘号，而是一张“去掉答案列”的二维表；`y` 是一列答案。

## 从客户表中选择 X 和 y

下面代码可以直接运行：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "age": [23, 41, 35],
        "monthly_spending": [188.5, 420.0, 315.8],
        "city": ["Suzhou", "Shanghai", "Nanjing"],
        "churn": [1, 0, 0],
    }
)

X = customers[["age", "monthly_spending"]].copy()
y = customers["churn"].copy()

print(X.columns.tolist())
print(X.shape)
print(y.tolist())
```

预期输出：

```text
['age', 'monthly_spending']
(3, 2)
[1, 0, 0]
```

`shape` 返回 `(行数, 列数)`。因此 `(3, 2)` 表示 3 位客户、2 个特征。`y` 有 3 个值，必须和 `X` 的 3 行一一对应。

## 为什么要使用二维 X

即使只有一个特征，scikit-learn 也通常要求 `X` 是二维的。双层方括号保留 DataFrame，单层方括号会得到一维 Series：

```python
import pandas as pd

customers = pd.DataFrame({"age": [23, 41, 35]})
one_dimensional = customers["age"]
two_dimensional = customers[["age"]]

print(one_dimensional.shape)
print(two_dimensional.shape)
```

预期输出：

```text
(3,)
(3, 1)
```

`(3,)` 表示一维序列；`(3, 1)` 才表示 3 行 1 列的特征表。

## 先检查标签

二分类是只在两个类别之间做预测的任务。本课程用 `0` 表示未流失，`1` 表示已流失。训练前应检查每类有多少样本：

```python
import pandas as pd

y = pd.Series([1, 0, 0, 1, 0], name="churn")
print(y.value_counts().sort_index().to_dict())
```

预期输出：

```text
{0: 3, 1: 2}
```

如果某一类极少，后续随机划分可能让测试集缺少该类别，模型评估也会不可靠。

## 代码流程

1. 明确业务问题：预测什么。
2. 选出允许模型使用的列，形成 `X`。
3. 选出正确答案列，形成 `y`。
4. 检查 `X.shape`、`y.shape` 和类别数量。
5. 确认 `X` 没有包含标签或预测之后才知道的信息。

## 常见错误

### 把 `churn` 留在 X 中

这叫**标签泄漏**：模型在训练和测试时都能直接看到正确答案，分数会虚高。修改方法是从 `X` 中删除 `churn`。

### X 和 y 行数不同

如果分别删除了不同的行，特征和答案会错位。清洗时应在同一张表上处理，再一起拆分，并检查 `len(X) == len(y)`。

### 把客户编号当成业务特征

`customer_id` 通常只是唯一标识，并不代表客户行为。模型可能记住编号中的偶然规律，因此本项目不把它作为特征。

## 与 IOM103 原项目的对应

原项目的客户流失流程先清理 `TotalCharges`，删除 `customerID`，把 `Churn` 从 `Yes/No` 映射成 `1/0`，再用其余列构造 `X`。本节是在拆解这个准备步骤。详见 [原项目分析](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

打开 [practice_01_features_and_labels.py](../../practice/sklearn/practice_01_features_and_labels.py)，完成：

1. 选择两个固定数值特征和标签。
2. 选择给定的混合类型特征。
3. 统计标签中每个类别的数量。

每道题都先检查输入列，再返回新对象，不要修改原 DataFrame。

## 运行命令

```powershell
python -m examples.sklearn.example_01_features_and_labels
pytest tests/sklearn/test_sklearn_practice.py -k "01"
```

练习未完成时显示 `XFAIL` 是正常状态；完成 TODO 后会执行真实断言。

## 本节检查清单

- [ ] 我能指出一张客户表中哪些列属于特征，哪一列属于标签。
- [ ] 我能解释 `X` 为什么通常是二维表。
- [ ] 我能用 `shape` 检查样本数和特征数。
- [ ] 我不会把 `churn` 或 `customer_id` 直接放进特征。
- [ ] 我能统计二分类标签的类别数量。
