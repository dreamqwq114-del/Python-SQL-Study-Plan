# Pandas 01：用 Series 和 DataFrame 表示表格数据

## 本章解决什么实际问题

你收到三条订单数量和两条客户记录。普通列表能保存数值，却没有“这一列叫什么”“这一行属于哪个订单”等表格信息。本章把订单数量表示成一列 `Series`，把客户记录表示成一张 `DataFrame`，并计算每笔订单金额。

本章的输入是 Python 列表或字典，输出是带行、列标签的 pandas 对象。

## 1. pandas 是什么

`pandas` 是处理表格数据的 Python 工具包。通常使用简称 `pd`：

```python
import pandas as pd

print(pd.__name__)
```

```text
pandas
```

`import pandas as pd` 的意思是：导入 pandas，并在后面的代码中用较短的 `pd` 指代它。

## 2. Series：带标签的一列数据

`Series` 是“一维”数据，也就是一列值。它可以有：

- 数据值；
- 每个值对应的索引标签；
- 这一列的名称。

```python
import pandas as pd

quantities = pd.Series(
    [1, 2, 3],
    index=["O001", "O002", "O003"],
    name="quantity",
)

print(quantities.to_dict())
print(quantities.loc["O002"])
print(quantities.name)
```

```text
{'O001': 1, 'O002': 2, 'O003': 3}
2
quantity
```

这里 `O001` 等是索引标签。`.loc["O002"]` 按标签取得订单 O002 的购买数量。

## 3. DataFrame：有行有列的一张表

`DataFrame` 是“二维”数据，可以理解为 Excel 工作表。字典中的键成为列名，每个列表成为一列。

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C001", "C002"],
        "city": ["Suzhou", "Shanghai"],
        "monthly_spending": [188.5, 420.0],
    }
)

print(customers.to_dict("records"))
print(customers.shape)
print(customers.columns.tolist())
```

```text
[{'customer_id': 'C001', 'city': 'Suzhou', 'monthly_spending': 188.5}, {'customer_id': 'C002', 'city': 'Shanghai', 'monthly_spending': 420.0}]
(2, 3)
['customer_id', 'city', 'monthly_spending']
```

`shape` 返回 `(行数, 列数)`，所以 `(2, 3)` 表示 2 行 3 列。`to_dict("records")` 把每行转成一个字典，便于清楚查看结果。

## 4. 用列计算新列

DataFrame 的两列可以逐行运算。下面把数量乘以单价：

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "order_id": ["O001", "O002"],
        "quantity": [2, 3],
        "unit_price": [50, 20],
    }
)
orders["order_total"] = orders["quantity"] * orders["unit_price"]

print(orders[["order_id", "order_total"]].to_dict("records"))
```

```text
[{'order_id': 'O001', 'order_total': 100}, {'order_id': 'O002', 'order_total': 60}]
```

这叫“向量化计算”：pandas 一次对整列执行运算，不需要自己写 `for` 循环。

## 5. 本章代码流程

```text
Python 列表或字典
        ↓
pd.Series() 或 pd.DataFrame()
        ↓
检查 shape、columns 和实际记录
        ↓
使用已有列计算新列
```

## 6. 常见错误

### 错误一：各列长度不同

`{"id": ["C1", "C2"], "city": ["A"]}` 中两列行数不同，pandas 无法判断第二位客户的城市，会报 `ValueError`。修正方法是让所有列表长度一致，或明确用缺失值占位。

### 错误二：把 Series 当成 DataFrame

`customers["city"]` 返回一维 Series；`customers[["city"]]` 返回二维 DataFrame。需要保留表格结构时使用双层方括号。

### 错误三：无意修改原表

练习要求“返回副本”时，先写 `result = dataframe.copy()`，再修改 `result`。否则函数外面的原数据也可能改变。

## 7. 与 IOM103 原项目的对应

原项目在 `task_a2_churn_prediction()` 中用 `pd.DataFrame(score_rows)` 建立模型指标表，在 `task_b_customer_segmentation()` 中给客户 DataFrame 新增 `Cluster` 列。也就是说，后面的模型输入和结果表都建立在本章的二维表概念上。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。本节使用的是缩小后的客户和订单示例，不修改原作业。

## 8. 本节练习

1. `build_customer_frame()`：按指定记录创建两行客户 DataFrame。
2. `build_order_series()`：创建带订单索引和列名的数量 Series。
3. `add_order_total()`：在副本中计算订单金额，不修改原表。

练习的详细输入、输出和边界情况写在 [practice_01_series_and_dataframe.py](practice.py) 的 docstring 中；最小提示统一放在本教材末尾的折叠区。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""用 Series 和 DataFrame 表示订单数量与客户记录。"""

import pandas as pd

def create_customer_data() -> tuple[pd.Series, pd.DataFrame]:
    """创建订单数量 Series 和客户 DataFrame。"""
    quantities = pd.Series(
        [1, 2, 3],
        index=["O001", "O002", "O003"],
        name="quantity",
    )
    customers = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "city": ["Suzhou", "Shanghai"],
            "monthly_spending": [188.5, 420.0],
        }
    )
    return quantities, customers

def main() -> None:
    quantities, customers = create_customer_data()
    print(quantities.to_dict())
    print(customers.to_dict("records"))
    print(customers.shape)

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/pandas/01_series_and_dataframe/test.py
```

练习仍有 TODO 时显示 3 个 `XFAIL` 是正常现象。

## 10. 本章检查清单

- 我能说出 Series 是一列、DataFrame 是一张表。
- 我能用字典创建 DataFrame，并读懂 `(行数, 列数)`。
- 我能通过索引标签从 Series 取值。
- 我能用两列直接计算新列。
- 我知道何时先使用 `copy()`，避免修改原始数据。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>build_customer_frame</code></summary>

把“列名: 一列数据”写进字典，再交给 pd.DataFrame()。

</details>

<details>
<summary><code>build_order_series</code></summary>

pd.Series() 可以同时接收 data、index 和 name。

</details>

<details>
<summary><code>add_order_total</code></summary>

先使用 dataframe.copy()，再让两列直接相乘。

</details>
