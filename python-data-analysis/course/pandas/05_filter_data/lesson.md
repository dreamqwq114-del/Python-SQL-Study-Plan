# Pandas 05：用业务条件筛选客户

## 本章解决什么实际问题

客户挽留团队不需要整张表，只想查看“年龄至少 30 岁且已经流失”的客户；区域经理只看自己负责的城市；营销活动只面向某个消费区间。本章把这些业务句子翻译成布尔条件。

“布尔条件”就是每行得到 `True` 或 `False` 的判断结果。pandas 只保留结果为 `True` 的行。

## 1. 单个条件

```python
import pandas as pd

customers = pd.DataFrame(
    {"customer_id": ["C1", "C2", "C3"], "age": [23, 35, 41]}
)
mask = customers["age"] >= 30
selected = customers.loc[mask]

print(mask.tolist())
print(selected["customer_id"].tolist())
```

```text
[False, True, True]
['C2', 'C3']
```

`mask` 是和数据行一一对应的真假 Series。

## 2. 多个条件：`&`、`|` 和 `~`

- `&`：两个条件都满足；
- `|`：至少满足一个；
- `~`：对真假取反。

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", "C2", "C3", "C4"],
        "age": [35, 35, 29, 30],
        "churn": [1, 0, 1, 1],
    }
)
mask = (customers["age"] >= 30) & (customers["churn"] == 1)

print(customers.loc[mask, "customer_id"].tolist())
```

```text
['C1', 'C4']
```

每个比较条件都加括号，这是 pandas 中最清楚、最安全的写法。

## 3. `isin()`：属于多个城市之一

```python
import pandas as pd

customers = pd.DataFrame(
    {"city": ["Suzhou", "Wuxi", "Shanghai", "Nanjing"]}
)
mask = customers["city"].isin(["Suzhou", "Wuxi"])

print(customers.loc[mask, "city"].tolist())
```

```text
['Suzhou', 'Wuxi']
```

如果允许列表为空，`isin([])` 对所有行都是 `False`，因此返回空表。

## 4. `between()`：筛选闭区间

```python
import pandas as pd

customers = pd.DataFrame(
    {"monthly_spending": [100.0, 200.0, 300.0, None]}
)
mask = customers["monthly_spending"].between(100, 200)

print(mask.tolist())
print(customers.loc[mask, "monthly_spending"].tolist())
```

```text
[True, True, False, False]
[100.0, 200.0]
```

默认包含 100 和 200 两个边界。缺失值不能证明位于区间内，所以不会保留。

## 5. 本章代码流程

```text
业务描述
  ↓ 翻译成每个单项比较
condition_1 / condition_2
  ↓ 用 &、|、~ 组合
布尔 mask
  ↓ dataframe.loc[mask]
筛选结果副本
```

## 6. 常见错误

### 错误一：使用 Python 的 `and` 或 `or`

Series 包含很多真假值，Python 不知道应该把整列当成一个真假值。使用 `&` 和 `|`，并给每个条件加括号。

### 错误二：忘记赋值筛选结果

`dataframe.loc[mask]` 不会自动替换原变量。需要写 `selected = dataframe.loc[mask].copy()`。

### 错误三：最小值大于最大值

范围 300 到 100 在业务上无意义。本课程练习要求主动抛出 `ValueError`，让调用者修正输入。

### 错误四：大小写或空格导致城市匹配失败

`" Suzhou "` 不等于 `"Suzhou"`。第 12 节会先统一文本，再筛选。

## 7. 与 IOM103 原项目的对应

原项目没有把“按城市筛选客户”作为独立任务，但 `prepare_churn_data()` 会选择目标列、删除标识列，模型评分也会从测试数据中取预测概率。这些操作都依赖“根据条件或字段选出所需数据”的思路。本节的业务筛选是为清洗和探索分析补充的通用技能，不声称原作业使用了相同条件。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `filter_customers()`：同时检查年龄和 0/1 流失状态。
2. `filter_by_cities()`：用城市列表进行成员筛选。
3. `filter_spending_range()`：筛选包含边界的消费区间，并拒绝反向范围。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""筛选指定年龄、城市与流失状态的客户。"""

import pandas as pd

from utils.paths import DATA_DIR

def select_retention_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """筛选 25 至 45 岁、苏州或上海、已流失的客户。"""
    city = dataframe["city"].str.strip().str.lower()
    mask = (
        dataframe["age"].between(25, 45)
        & city.isin(["suzhou", "shanghai"])
        & (dataframe["churn"] == "Yes")
    )
    return dataframe.loc[mask].copy()

def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    selected = select_retention_customers(customers)
    print(selected.shape)
    print(selected["customer_id"].tolist())
    print(selected[["age", "city", "churn"]].to_dict("records"))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/pandas/05_filter_data/test.py
```

## 10. 本章检查清单

- 我能把一条业务规则拆成多个比较条件。
- 我会使用 `&`、`|`、`~`，而不是 `and`、`or`。
- 我能用 `isin()` 筛选多个类别。
- 我知道 `between()` 是否包含边界。
- 我会检查不合理的范围输入。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>filter_customers</code></summary>

每个条件加括号，并使用 & 连接。

</details>

<details>
<summary><code>filter_by_cities</code></summary>

Series.isin() 用来判断值是否属于一个列表。

</details>

<details>
<summary><code>filter_spending_range</code></summary>

Series.between(minimum, maximum) 默认包含两端。

</details>
