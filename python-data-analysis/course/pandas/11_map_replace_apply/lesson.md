# Pandas 11：转换类别、名称和消费档位

## 本章解决什么实际问题

数据里 `churn` 用 0/1 保存，报告要显示 `Stayed`/`Churned`；合同内部名称需要替换；客户还要按月消费分成三个档位。本章比较 `map`、`replace`、`apply` 和直接列运算。

## 1. `map`：一一映射类别

```python
import pandas as pd

customers = pd.DataFrame({"churn": [1, 0, 9]})
customers["churn_label"] = customers["churn"].map(
    {0: "Stayed", 1: "Churned"}
)

print(customers["churn_label"].tolist())
```

```text
['Churned', 'Stayed', nan]
```

`map` 在字典中查找每个值。9 没有对应项，所以结果为缺失值。这种行为能帮助发现意外类别。

## 2. `replace`：替换匹配项，其余保留

```python
import pandas as pd

contracts = pd.Series(["Monthly", "Yearly", "Two-year"])
renamed = contracts.replace(
    {"Monthly": "月付", "Two-year": "两年"}
)

print(renamed.tolist())
```

```text
['月付', 'Yearly', '两年']
```

`Yearly` 没有出现在替换字典里，因此保持不变。这与 `map` 未匹配变缺失的行为不同。

## 3. 直接列运算优先

年消费只是月消费乘 12，不需要 `apply`：

```python
import pandas as pd

customers = pd.DataFrame({"monthly_spending": [100.0, 50.0]})
customers["annual_spending"] = customers["monthly_spending"] * 12

print(customers["annual_spending"].tolist())
```

```text
[1200.0, 600.0]
```

能用整列运算时优先整列运算，代码更短，通常也更快。

## 4. `apply`：执行逐值规则

消费档位有多个分支，可以写普通函数再应用到每个值：

```python
import pandas as pd

def to_band(value):
    if pd.isna(value):
        return "Unknown"
    if value < 200:
        return "Low"
    if value < 400:
        return "Medium"
    return "High"

spending = pd.Series([199.0, 200.0, 400.0, None])
bands = spending.apply(to_band)

print(bands.tolist())
```

```text
['Low', 'Medium', 'High', 'Unknown']
```

`apply` 表示把函数依次用于 Series 的每个值。它适合不好用简单运算表达的小型业务规则。

## 5. 如何选择

```text
固定类别一一对应 → map
只替换部分值，其余保留 → replace
加减乘除等整列计算 → 直接列运算
多分支逐值规则 → apply
```

## 6. 常见错误

### 错误一：用 `map` 后意外出现缺失值

说明原值没有出现在映射字典里。先用 `value_counts()` 找出全部类别，再补充映射或决定如何处理。

### 错误二：能直接相乘却写 `apply(lambda ...)`

`monthly_spending * 12` 更清楚，不需要逐值调用函数。

### 错误三：边界条件重叠

本课程规定 200 属于 Medium，400 属于 High。条件顺序必须和业务规则一致。

### 错误四：修改原表

转换函数先创建副本，再增加或替换列。

## 7. 与 IOM103 原项目的对应

原项目用 `.map({"No": 0, "Yes": 1})` 把流失目标转为 0/1；Task B 对分群汇总使用 `apply(cluster_description, axis=1)` 生成业务画像。`replace` 是本课程为文本标签整理补充的相关技能。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `add_churn_and_annual_spending()`：组合 map 与整列金额计算。
2. `replace_contract_labels()`：只替换字典中存在的合同名称。
3. `add_spending_band()`：用 apply 实现含缺失值和边界的分档规则。

## 9. 运行命令

```powershell
python -m course.pandas.11_map_replace_apply.example
pytest course/pandas/11_map_replace_apply/test.py
```

## 10. 本章检查清单

- 我能解释 map 和 replace 对未匹配值的不同处理。
- 我会优先使用直接列运算。
- 我能把多分支规则写成普通函数，再交给 apply。
- 我会明确检查 200、400 等边界值。
- 我知道映射后出现缺失值可能代表新类别。
