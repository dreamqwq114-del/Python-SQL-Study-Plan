# Pandas 10：连接客户表与订单表

## 本章解决什么实际问题

客户资料一位客户一行，订单明细一笔订单一行。要回答“每位客户买过什么”，必须按 `customer_id` 横向连接两张表。另一方面，一月和二月订单列结构相同，需要纵向拼接。本章区分 `merge` 和 `concat`。

## 1. `merge`：按共同键横向连接

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2"],
        "city": ["A", "B"],
    }
)
orders = pd.DataFrame(
    {
        "customer_id": ["C1", "C1"],
        "order_id": ["O1", "O2"],
    }
)
merged = customers.merge(
    orders,
    on="customer_id",
    how="left",
)

print(merged.to_dict("records"))
```

```text
[{'customer_id': 'C1', 'city': 'A', 'order_id': 'O1'}, {'customer_id': 'C1', 'city': 'A', 'order_id': 'O2'}, {'customer_id': 'C2', 'city': 'B', 'order_id': nan}]
```

`on="customer_id"` 指定连接键。C1 有两笔订单，所以连接后出现两行；C2 没有订单，仍被保留，订单编号为缺失。

## 2. 左连接和内连接

- `how="left"`：保留左表所有行；
- `how="inner"`：只保留两边都能匹配的键。

```python
import pandas as pd

customers = pd.DataFrame({"customer_id": ["C1", "C2"]})
orders = pd.DataFrame({"customer_id": ["C1"], "order_id": ["O1"]})

left_result = customers.merge(orders, on="customer_id", how="left")
inner_result = customers.merge(orders, on="customer_id", how="inner")

print(left_result["customer_id"].tolist())
print(inner_result["customer_id"].tolist())
```

```text
['C1', 'C2']
['C1']
```

选择连接方式是业务决定：客户总表通常需要左连接，避免无订单客户消失。

## 3. `concat`：同结构数据上下拼接

```python
import pandas as pd

january = pd.DataFrame({"order_id": ["O1", "O2"]})
february = pd.DataFrame({"order_id": ["O3"]})
all_orders = pd.concat(
    [january, february],
    ignore_index=True,
)

print(all_orders["order_id"].tolist())
print(all_orders.index.tolist())
```

```text
['O1', 'O2', 'O3']
[0, 1, 2]
```

`ignore_index=True` 丢弃各批次原来的重复索引，生成连续新索引。

## 4. 找出无法匹配的订单

```python
import pandas as pd

customers = pd.DataFrame({"customer_id": ["C1", "C2"]})
orders = pd.DataFrame(
    {
        "order_id": ["O1", "O9"],
        "customer_id": ["C1", "C9"],
    }
)
mask = ~orders["customer_id"].isin(customers["customer_id"])

print(orders.loc[mask].to_dict("records"))
```

```text
[{'order_id': 'O9', 'customer_id': 'C9'}]
```

这种记录叫“孤立订单”：它引用的客户不在客户主表中。

## 5. 本章代码流程

```text
先问：是横向增加列，还是纵向增加行？
        ↓                         ↓
共同键连接 merge()          同结构批次 concat()
        ↓                         ↓
检查行数与未匹配键          ignore_index=True
        ↓
验证结果是否符合一对一/一对多关系
```

## 6. 常见错误

### 错误一：连接键类型不同

一边是整数 1，另一边是文本 `"1"`，不会正常匹配。连接前检查两边键的类型。

### 错误二：没有理解一对多导致行数增加

一位客户有多笔订单，客户资料会复制到多行。这是合理的一对多结果，不一定是重复错误。

### 错误三：误用内连接丢掉客户

若分析对象是所有客户，使用 `inner` 会让无订单客户消失，应使用 `left`。

### 错误四：对空列表直接 `pd.concat`

`pd.concat([])` 会报错。本课程练习先检查空列表并返回空 DataFrame。

## 7. 与 IOM103 原项目的对应

原始 IOM103 脚本分别读取流失数据和分群数据，没有直接把两表 `merge` 或 `concat`。本章是为了综合客户项目中连接 sample 客户与订单而补充的必备技能，不能误写成原作业已经执行了客户订单连接。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `merge_customers_orders()`：按客户编号左连接。
2. `concat_order_batches()`：按顺序拼接订单批次并处理空列表。
3. `find_orders_without_customer()`：找出客户主表中不存在的订单。

## 9. 运行命令

```powershell
python -m course.pandas.10_merge_and_concat.example
pytest course/pandas/10_merge_and_concat/test.py
```

## 10. 本章检查清单

- 我能判断该用横向连接还是纵向拼接。
- 我能解释左连接和内连接的区别。
- 我理解一位客户多笔订单为什么会增加行数。
- 我会重置拼接后的索引。
- 我会检查无法匹配的业务键。
