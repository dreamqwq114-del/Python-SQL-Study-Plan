# Pandas 06：识别、填充和删除缺失值

## 本章解决什么实际问题

客户表中有人没有填写满意度，有人的关键客户编号或城市缺失。直接计算或建模可能失败。你需要先统计缺失，再根据业务含义选择“填充”还是“删除”。

缺失值表示“这个位置没有可用数据”。常见显示包括 `NaN`、`None` 和日期中的 `NaT`。

## 1. 用 `isna()` 找缺失值

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "age": [20, None, 30],
        "city": ["A", "B", None],
    }
)

print(customers.isna().sum().to_dict())
```

```text
{'age': 1, 'city': 1}
```

`isna()` 把每个位置变成真假值，`sum()` 把 `True` 当作 1 相加，得到每列缺失数量。

## 2. 用 `fillna()` 填充

如果满意度缺失代表“暂时使用默认评分”，可以使用指定值填充：

```python
import pandas as pd

customers = pd.DataFrame(
    {"satisfaction_score": [5.0, None, 2.0]}
)
result = customers.copy()
result["satisfaction_score"] = result["satisfaction_score"].fillna(3.0)

print(result["satisfaction_score"].tolist())
print(customers["satisfaction_score"].isna().sum())
```

```text
[5.0, 3.0, 2.0]
1
```

第二行输出说明原表仍有一个缺失值，函数只修改了副本。

数值分析中也常用中位数填充：

```python
import pandas as pd

values = pd.Series([1.0, None, 9.0])
filled = values.fillna(values.median())

print(values.median())
print(filled.tolist())
```

```text
5.0
[1.0, 5.0, 9.0]
```

中位数是排序后位于中间的值，比平均数更不容易受极端大值影响。

## 3. 用 `dropna()` 删除不完整记录

如果客户编号和城市是分析必须字段，可以只检查这两列：

```python
import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1", None, "C3"],
        "city": ["A", "B", None],
        "score": [5, 4, 3],
    }
)
complete = customers.dropna(
    subset=["customer_id", "city"]
).reset_index(drop=True)

print(complete.to_dict("records"))
```

```text
[{'customer_id': 'C1', 'city': 'A', 'score': 5}]
```

`subset` 表示只把指定列视为必填列。不要无条件删除所有含缺失的行。

## 4. 如何选择处理方式

先问缺失的业务含义：

- 非关键、可合理补齐的数值：可能用中位数；
- 非关键类别：可能用最常见值或 `"Unknown"`；
- 分析必需的关键字段：可能删除该行；
- 缺失本身有意义：可以保留并增加“是否缺失”标记。

不存在适用于所有数据的唯一填充方法。

## 5. 本章代码流程

```text
isna().sum() 统计
       ↓
判断字段是否关键、缺失是否有含义
       ↓
fillna() 填充 或 dropna(subset=...) 删除
       ↓
再次 isna().sum() 验证
```

## 6. 常见错误

### 错误一：把空字符串当作自动缺失

`""` 和 `"   "` 不一定自动成为 `NaN`。需要先清理文本，或在读取 CSV 时配置缺失标记。

### 错误二：不加选择地删除整行

`dropna()` 不写 `subset` 会检查所有列，可能因为不重要字段缺失而丢掉大量客户。

### 错误三：直接在原表上填充

课程练习要求保留输入表。先 `copy()`，再给副本列赋值。

### 错误四：填充后不验证

处理完成后再次统计缺失值，确认目标列真的已补齐。

## 7. 与 IOM103 原项目的对应

原项目 `prepare_churn_data()` 先把 `TotalCharges` 转为数值，再用该列中位数填充无法转换产生的缺失值。后续 scikit-learn 预处理器也分别为数值和类别列配置缺失值填充。这里先用 pandas 掌握相同的数据质量思想。若只是制作一张固定清洗报表，可以按整张表的规则填充；若这些列将作为模型特征，应先划分数据，再让训练管道（Pipeline，即按顺序连接预处理和模型的对象）只从训练集学习中位数。原项目在划分前使用全表中位数，是一个应改进的数据泄漏点。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `count_missing()`：统计每一列的缺失数量。
2. `fill_missing_scores()`：在副本中用指定满意度补齐。
3. `drop_incomplete_rows()`：只按调用者指定的关键列删除记录。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""统计缺失值并填充客户满意度。"""

import pandas as pd

from utils.paths import DATA_DIR

def fill_satisfaction(dataframe: pd.DataFrame) -> pd.DataFrame:
    """用满意度中位数填充缺失值。"""
    result = dataframe.copy()
    median_score = result["satisfaction_score"].median()
    result["satisfaction_score"] = result["satisfaction_score"].fillna(
        median_score
    )
    return result

def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    cleaned = fill_satisfaction(customers)
    print(customers.isna().sum().to_dict())
    print(cleaned["satisfaction_score"].isna().sum())
    print(cleaned["satisfaction_score"].median())

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/pandas/06_missing_values/test.py
```

## 10. 本章检查清单

- 我能区分“发现缺失”和“处理缺失”。
- 我能统计每列缺失数量。
- 我会根据业务含义选择填充或删除。
- 我能只检查指定关键列。
- 我会在处理后再次验证缺失数量。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>count_missing</code></summary>

先用 isna() 得到真假表，再按列 sum()。

</details>

<details>
<summary><code>fill_missing_scores</code></summary>

先 copy()，再对指定列使用 fillna()。

</details>

<details>
<summary><code>drop_incomplete_rows</code></summary>

dropna(subset=...) 可只检查指定列，之后 reset_index(drop=True)。

</details>
