# Pandas 07：去除重复记录并修正数据类型

## 本章解决什么实际问题

客户 C1 被重复导入两次，月消费列中还混入 `"bad"`。如果不处理，客户数会被重复计算，平均消费也无法正确求出。本章完成“按业务主键去重”和“把文本安全转换成数字”。

“业务主键”是能标识一条业务实体的字段，例如 `customer_id` 标识客户。

## 1. 发现重复值

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C1", "C2"],
        "monthly_spending": ["100", "120", "bad"],
    }
)

print(customers.duplicated(subset="customer_id").tolist())
print(customers.duplicated(subset="customer_id").sum())
```

```text
[False, True, False]
1
```

第二条 C1 的客户编号已经出现过，因此标记为重复。

## 2. 保留第一条或最后一条

`keep="first"` 保留第一次出现，`keep="last"` 保留最后一次出现：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2", "C1"],
        "monthly_spending": [100, 200, 120],
    }
)
latest = customers.drop_duplicates(
    subset="customer_id",
    keep="last",
).reset_index(drop=True)

print(latest.to_dict("records"))
```

```text
[{'customer_id': 'C2', 'monthly_spending': 200}, {'customer_id': 'C1', 'monthly_spending': 120}]
```

“最新”在本练习中指表中最后出现的记录。真实项目若有更新时间，应先按时间排序。

## 3. 用 `to_numeric()` 安全转换数字

```python
import pandas as pd

spending_text = pd.Series(["100", "19.5", "bad"])
spending = pd.to_numeric(spending_text, errors="coerce")

print(spending.tolist())
print(spending.isna().tolist())
```

```text
[100.0, 19.5, nan]
[False, False, True]
```

`errors="coerce"` 把无法解释成数字的 `"bad"` 转为 `NaN`。转换后必须检查新产生了多少缺失值。

## 4. 可空整数 `Int64`

普通整数列不能保存 `NaN`。pandas 的大写 `Int64` 类型可以同时保存整数和缺失值：

```python
import pandas as pd

ages = pd.to_numeric(
    pd.Series(["21", "bad"]),
    errors="coerce",
).astype("Int64")

print(ages.tolist())
print(str(ages.dtype))
```

```text
[21, <NA>]
Int64
```

这里大写 `Int64` 是 pandas 的“可空整数类型”，不要与 NumPy 的小写 `int64` 混淆。

## 5. 本章代码流程

```text
检查 customer_id 重复数量
        ↓
决定保留 first 还是 last
        ↓
drop_duplicates()
        ↓
pd.to_numeric(errors="coerce")
        ↓
检查 dtype 与新缺失值
```

## 6. 常见错误

### 错误一：对整行去重，却忽略客户编号

同一客户的消费值变了，整行并不完全相同。需要明确 `subset="customer_id"`。

### 错误二：随意决定保留第一条

第一条和最后一条代表什么取决于数据顺序。真实项目要查看时间字段或业务规则。

### 错误三：直接使用 `astype(float)`

遇到 `"bad"` 会立刻报错。脏数据先用 `pd.to_numeric(errors="coerce")`，然后统计失败值。

### 错误四：转换后不检查

程序没有报错不等于数据都成功转换。必须检查 `isna().sum()`。

## 7. 与 IOM103 原项目的对应

原项目 `prepare_churn_data()` 对 `TotalCharges` 使用 `pd.to_numeric(..., errors="coerce")`，随后在划分前用全表中位数填充转换失败产生的缺失值。这是本章最直接的对应，但用于建模时会让测试信息提前进入填充值；更规范的做法是只在这里完成数值转换，把填补交给只在训练集拟合的 Pipeline。按客户去重是 sample 数据刻意补充的通用清洗练习，原脚本没有声明执行该步骤。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `clean_duplicates_and_spending()`：保留首条客户记录并安全转换消费。
2. `convert_customer_types()`：把年龄转为可空整数，把消费转为数值。
3. `keep_latest_customer_records()`：保留表中最后出现的客户记录。

## 9. 运行命令

```powershell
python -m course.pandas.07_duplicates_and_types.example
pytest course/pandas/07_duplicates_and_types/test.py
```

## 10. 本章检查清单

- 我能说明为什么按业务主键去重。
- 我能根据业务规则选择保留第一条或最后一条。
- 我能安全转换含脏值的数字文本。
- 我能解释 `errors="coerce"`。
- 我知道转换后要检查新产生的缺失值。
