# Pandas 08：排序客户并计算描述统计

## 本章解决什么实际问题

客户经理想找到消费最高的前三位客户，同时了解典型消费水平和最大消费。本章用排序回答“谁最高”，用平均数、中位数和最大值回答“总体怎样”。

“描述统计”是用少量数字概括一列数据，不是在预测未来。

## 1. 排序

`sort_values()` 按某列重新排列行：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2", "C3"],
        "monthly_spending": [100, 300, 200],
    }
)
high_to_low = customers.sort_values(
    "monthly_spending",
    ascending=False,
).reset_index(drop=True)

print(high_to_low["customer_id"].tolist())
print(high_to_low["monthly_spending"].tolist())
```

```text
['C2', 'C3', 'C1']
[300, 200, 100]
```

`ascending=False` 表示降序，也就是从大到小。排序后重置索引，结果更方便继续处理。

## 2. 取前 N 名

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2", "C3"],
        "monthly_spending": [100, 300, 200],
    }
)
top_two = (
    customers.sort_values("monthly_spending", ascending=False)
    .head(2)
    .reset_index(drop=True)
)

print(top_two.to_dict("records"))
```

```text
[{'customer_id': 'C2', 'monthly_spending': 300}, {'customer_id': 'C3', 'monthly_spending': 200}]
```

`count=0` 应返回空表，负数在本课程契约中视为错误。

## 3. 平均数、中位数和最大值

```python
import pandas as pd

spending = pd.Series([100.0, None, 300.0])

print(spending.mean())
print(spending.median())
print(spending.max())
```

```text
200.0
200.0
300.0
```

- 平均数 `mean()`：总和除以有效数量；
- 中位数 `median()`：排序后中间位置的值；
- 最大值 `max()`：最高值。

这些函数默认忽略缺失值。

## 4. 为什么同时看平均数和中位数

```python
import pandas as pd

spending = pd.Series([100, 110, 120, 1000])

print(spending.mean())
print(spending.median())
```

```text
332.5
115.0
```

1000 把平均数明显拉高，而中位数仍接近大多数客户。出现极端值时，不能只看平均数。

## 5. 本章代码流程

```text
确认消费列是数值
       ↓
mean / median / max 描述总体
       ↓
sort_values(ascending=False)
       ↓
head(count) 取得高消费客户
```

## 6. 常见错误

### 错误一：在字符串列上排序

字符串会按字符排序，`"90"` 可能排在 `"800"` 后面。先确认类型或用 `to_numeric()` 清理。

### 错误二：把降序方向写反

消费最高需要 `ascending=False`。运行后检查前几项，而不是只相信参数。

### 错误三：把平均数当成“多数人的金额”

极端客户会影响平均数。一起查看中位数和数据分布。

### 错误四：空数据产生 `NaN`

空列没有可计算的平均数、最大值，因此结果是 `NaN`，不是 0。

## 7. 与 IOM103 原项目的对应

原项目把模型指标表按 `AUROC` 降序排列以寻找最佳模型，并把特征重要性按数值降序取前 15 个。Task B 的分群汇总还使用 `.round(2)` 使报告更易读。本章先在消费数据上练习同样的排序与摘要思路。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `spending_statistics()`：返回平均数、中位数和最大值。
2. `sort_customers_by_spending()`：按调用者指定方向排序。
3. `top_spending_customers()`：返回高消费前 N 名并验证数量输入。

## 9. 运行命令

```powershell
python -m examples.pandas.example_08_sort_and_statistics
pytest tests/pandas/test_pandas_practice.py -k "answer_08 or practice_08"
```

## 10. 本章检查清单

- 我能正确设置升序和降序。
- 我能取得排序后的前 N 行。
- 我能计算平均数、中位数和最大值。
- 我知道缺失值默认如何参与这些统计。
- 我能解释极端值为什么会让平均数和中位数不同。
