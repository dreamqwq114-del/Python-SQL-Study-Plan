# Pandas 04：准确选择需要的行和列

## 本章解决什么实际问题

客户表有 9 列，但消费报告只需要客户编号和月消费；经理还可能指定某些客户或只想预览前三行。本章学习在不改变原表的前提下选出一个小数据块。

## 1. 选择一列和多列

一层方括号返回 Series，双层方括号返回 DataFrame：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2"],
        "city": ["Suzhou", "Wuxi"],
        "monthly_spending": [100, 200],
    }
)

one_column = customers["city"]
two_columns = customers[["customer_id", "monthly_spending"]]

print(one_column.ndim)
print(two_columns.ndim)
print(two_columns.to_dict("records"))
```

```text
1
2
[{'customer_id': 'C1', 'monthly_spending': 100}, {'customer_id': 'C2', 'monthly_spending': 200}]
```

`ndim` 表示维度数。Series 是 1 维，DataFrame 是 2 维。

## 2. `loc`：按标签选择

`loc` 根据行标签和列名选择：

```python
import pandas as pd

customers = pd.DataFrame(
    {"city": ["Suzhou", "Wuxi"], "age": [23, 41]},
    index=["C001", "C002"],
)

selected = customers.loc[["C002", "C001"], ["age"]]

print(selected.index.tolist())
print(selected["age"].tolist())
```

```text
['C002', 'C001']
[41, 23]
```

列表中的顺序决定返回顺序。标签不存在时，pandas 会抛出 `KeyError`，这能及时暴露客户编号拼错的问题。

## 3. `iloc`：按位置选择

`iloc` 根据第几行、第几列选择，位置从 0 开始：

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "order_id": ["O1", "O2", "O3"],
        "quantity": [1, 2, 3],
        "unit_price": [99, 50, 20],
    }
)

block = orders.iloc[:2, :2]

print(block.to_dict("records"))
```

```text
[{'order_id': 'O1', 'quantity': 1}, {'order_id': 'O2', 'quantity': 2}]
```

`:2` 表示从开始取到位置 2 之前，因此得到位置 0 和 1。

## 4. 选择后返回副本

课程练习要求函数不修改传入表。安全写法是：

```python
import pandas as pd

customers = pd.DataFrame(
    {"customer_id": ["C1"], "monthly_spending": [100], "city": ["A"]}
)
result = customers[["customer_id", "monthly_spending"]].copy()
result["monthly_spending"] = 999

print(customers["monthly_spending"].tolist())
print(result["monthly_spending"].tolist())
```

```text
[100]
[999]
```

## 5. 本章代码流程

```text
完整 DataFrame
     ↓ 需要列名还是位置？
loc / 双层方括号    iloc
     ↓
检查返回维度和顺序
     ↓
copy() 后再修改
```

## 6. 常见错误

### 错误一：混淆标签和位置

客户索引为 `"C001"` 时用 `.loc["C001"]`；想取第一行时用 `.iloc[0]`。不要把客户编号当数字位置。

### 错误二：切片边界理解错误

`iloc[:3]` 取位置 0、1、2；`loc[0:2]` 在整数标签下通常包含标签 2。两者规则不同。

### 错误三：多列只写一层列表

`dataframe["a", "b"]` 会把元组当成一个列名。多列必须写 `dataframe[["a", "b"]]`。

## 7. 与 IOM103 原项目的对应

原项目在 `prepare_churn_data()` 中选择 `Churn` 作为目标 `y`，并把它从特征表 `X` 中删除；在 Task B 中用 `customer_data[cluster_features]` 只选年龄、收入和消费得分三列。本章就是这些“明确选择输入字段”操作的基础。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `select_customer_columns()`：固定返回报告需要的两列。
2. `select_rows_by_labels()`：按标签和给定顺序选择客户。
3. `select_data_block()`：组合指定列和前若干行，并检查负数输入。

## 9. 运行命令

```powershell
python -m course.pandas.04_select_rows_and_columns.example
pytest course/pandas/04_select_rows_and_columns/test.py
```

## 10. 本章检查清单

- 我能判断一次选择会返回 Series 还是 DataFrame。
- 我能解释 `loc` 按标签、`iloc` 按位置。
- 我知道切片的结束位置是否包含。
- 我能保持调用者要求的行列顺序。
- 我会在需要修改结果前创建副本。
