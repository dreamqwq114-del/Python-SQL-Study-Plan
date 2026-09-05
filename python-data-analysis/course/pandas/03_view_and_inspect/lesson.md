# Pandas 03：在分析前查看和检查数据

## 本章解决什么实际问题

客户表读取成功后，你还不知道它有多少记录、各列是什么类型、开头数据是否合理、合同类别各有多少。直接开始建模容易把错误带到后面。本章建立“先检查，再分析”的固定习惯。

## 1. 用 `head()` 预览前几行

`head(n)` 返回前 `n` 行，适合确认列和值是否读对。

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2", "C3"],
        "city": ["Suzhou", "Shanghai", "Wuxi"],
    }
)

print(customers.head(2).to_dict("records"))
```

```text
[{'customer_id': 'C1', 'city': 'Suzhou'}, {'customer_id': 'C2', 'city': 'Shanghai'}]
```

`tail(n)` 查看末尾，`sample(n, random_state=42)` 随机抽查。固定 `random_state` 后，每次抽到的行相同，便于复现。

## 2. 用 `shape` 和 `columns` 检查结构

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "order_id": ["O1", "O2", "O3"],
        "quantity": [1, 2, 1],
        "unit_price": [99, 50, 20],
    }
)

print(orders.shape)
print(orders.columns.tolist())
```

```text
(3, 3)
['order_id', 'quantity', 'unit_price']
```

结构摘要中的三个问题是：

- `rows`：有多少条记录？
- `columns`：有哪些字段？
- `dtypes`：每列被 pandas 当成什么类型？

## 3. 用 `dtypes` 检查类型

```python
import pandas as pd

data = pd.DataFrame(
    {"age": [20, 30], "spending_text": ["100", "unknown"]}
)

print({column: str(dtype) for column, dtype in data.dtypes.items()})
```

```text
{'age': 'int64', 'spending_text': 'str'}
```

这里 `spending_text` 看起来含数字，但由于混有 `"unknown"`，整列是字符串。不同 pandas 配置下文本类型名称可能显示为 `object` 或 `str`；重点是它不是数值类型。

## 4. 用 `value_counts()` 检查类别

`value_counts()` 统计每个值出现多少次：

```python
import pandas as pd

customers = pd.DataFrame(
    {"contract_type": ["Monthly", "Yearly", "Monthly", None]}
)

print(customers["contract_type"].value_counts().to_dict())
print(customers["contract_type"].value_counts(dropna=False).sum())
```

```text
{'Monthly': 2, 'Yearly': 1}
4
```

默认忽略缺失值；`dropna=False` 会把缺失值也算进去。

## 5. 本章代码流程

```text
读入 DataFrame
      ↓
head() 看实际记录
      ↓
shape / columns 看结构
      ↓
dtypes 看类型
      ↓
value_counts() 看类别分布
```

## 6. 常见错误

### 错误一：打印整张大表

几千行输出既慢又难读。使用 `head()`、`tail()` 或固定随机种子的 `sample()`。

### 错误二：把 `shape` 当函数

写 `dataframe.shape`，不要写 `dataframe.shape()`。`shape` 是已经保存好的结构属性。

### 错误三：只看列名，不看类型

`monthly_spending` 这个名称不能保证它真是数字。必须检查 `dtypes`，再决定能否计算平均值。

### 错误四：负数传给预览函数

pandas 的 `head(-1)` 有特殊含义，但本课程的 `preview_rows()` 契约把负数视为输入错误，要求主动抛出 `ValueError`。

## 7. 与 IOM103 原项目的对应

原项目在读取 Task A2 后打印 `X.shape` 和目标比例，在 Task B 中打印 `customer_data.shape` 与 `head()`。这是先确认数据规模和内容，再训练模型的检查步骤。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `summarize_structure()`：返回行数、列名和类型名称。
2. `preview_rows()`：安全返回指定数量的表头记录。
3. `count_column_values()`：决定是否把缺失值计入类别频数。

## 9. 运行命令

```powershell
python -m course.pandas.03_view_and_inspect.example
pytest course/pandas/03_view_and_inspect/test.py
```

## 10. 本章检查清单

- 我能用前几行而不是整张表检查数据。
- 我能准确读懂 `(行数, 列数)`。
- 我能区分列名和数据类型。
- 我能统计类别频数，并决定是否包括缺失值。
- 我知道为什么检查应该发生在清洗和建模之前。
