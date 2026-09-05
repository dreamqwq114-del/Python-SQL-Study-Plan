# Pandas 09：按城市或合同分组汇总

## 本章解决什么实际问题

一行一个客户的明细表不方便直接比较城市。经理需要“每个城市有多少客户、平均消费是多少”，流失分析还需要“每种合同的流失率”。本章把明细拆成组，再为每组计算汇总值。

`groupby` 的含义是“按照某列相同的值分组”；`agg` 是 aggregate（聚合）的缩写，表示把每组很多行压缩成统计结果。

## 1. 最简单的分组平均

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "city": ["A", "A", "B"],
        "monthly_spending": [100, 300, 50],
    }
)
average = customers.groupby("city")["monthly_spending"].mean()

print(average.to_dict())
```

```text
{'A': 200.0, 'B': 50.0}
```

先按 city 分组，再从每组中选择消费列计算平均数。

## 2. 一次计算多项指标

“命名聚合”可以清楚指定输出列名、来源列和计算方法：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2", "C2", "C3"],
        "city": ["A", "A", "A", "B"],
        "monthly_spending": [100.0, 300.0, 300.0, 50.0],
    }
)
summary = (
    customers.groupby("city")
    .agg(
        customer_count=("customer_id", "nunique"),
        average_spending=("monthly_spending", "mean"),
    )
    .reset_index()
)

print(summary.round(2).to_dict("records"))
```

```text
[{'city': 'A', 'customer_count': 2, 'average_spending': 233.33}, {'city': 'B', 'customer_count': 1, 'average_spending': 50.0}]
```

这里 A 城有三行，但 C2 重复出现，所以 `nunique` 得到 2 位不同客户。平均消费仍按三行计算，得到 233.33。选择 `count`、`size` 还是 `nunique` 必须符合业务问题。

## 3. 汇总订单金额

先计算行级订单金额，再按客户汇总：

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "order_id": ["O1", "O2", "O3"],
        "customer_id": ["C1", "C1", "C2"],
        "quantity": [2, 1, 3],
        "unit_price": [50, 60, 10],
    }
)
orders["order_total"] = orders["quantity"] * orders["unit_price"]
summary = (
    orders.groupby("customer_id")
    .agg(
        order_count=("order_id", "nunique"),
        total_spending=("order_total", "sum"),
    )
    .reset_index()
)

print(summary.to_dict("records"))
```

```text
[{'customer_id': 'C1', 'order_count': 2, 'total_spending': 160}, {'customer_id': 'C2', 'order_count': 1, 'total_spending': 30}]
```

## 4. 0/1 平均值就是比例

流失编码为 1，未流失编码为 0 时，平均值就是流失率：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "contract_type": ["Monthly", "Monthly", "Yearly"],
        "churn": [1, 0, 0],
    }
)
rate = customers.groupby("contract_type")["churn"].mean()

print(rate.to_dict())
```

```text
{'Monthly': 0.5, 'Yearly': 0.0}
```

Monthly 组中一个 1、一个 0，平均值为 0.5，也就是 50%。

## 5. 本章代码流程

```text
明细表
  ↓ 确认一行代表什么
groupby(分组列)
  ↓
agg(输出名=(来源列, 统计方法))
  ↓
reset_index()
  ↓
每组一行的汇总表
```

## 6. 常见错误

### 错误一：分组后忘记 `reset_index()`

分组列默认变成索引。要保存或继续合并时，常用 `reset_index()` 恢复普通列。

### 错误二：混淆 `count`、`size` 和 `nunique`

`size` 统计行数，`count` 忽略该列缺失值，`nunique` 统计不同值数量。先明确业务问题。

### 错误三：对文本金额求平均

先用 `pd.to_numeric()`，否则统计可能失败。

### 错误四：直接把 Yes/No 求平均

文本不能直接算比例。先映射为 0/1，再求平均。

## 7. 与 IOM103 原项目的对应

原项目把 `Contract` 与 0/1 `Churn` 组合成 DataFrame，按合同分组求平均流失率。Task B 还按 `Cluster` 分组，聚合客户数、平均年龄、平均收入、平均消费得分以及性别数量。这两处正是本章的核心用法。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `summarize_by_city()`：统计不同客户数和平均消费。
2. `summarize_orders_by_customer()`：从订单行计算客户订单数和总金额。
3. `calculate_churn_rate_by_contract()`：用 0/1 平均值计算合同流失率。

## 9. 运行命令

```powershell
python -m examples.pandas.example_09_groupby_and_agg
pytest tests/pandas/test_pandas_practice.py -k "answer_09 or practice_09"
```

## 10. 本章检查清单

- 我能说明一行明细代表什么、分组后一行代表什么。
- 我会使用命名聚合生成清楚的列名。
- 我能区分行数、有效值数和不同值数。
- 我能先计算行级金额，再计算分组总金额。
- 我能解释为什么 0/1 平均值等于比例。
