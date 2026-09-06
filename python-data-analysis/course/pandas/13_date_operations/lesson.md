# Pandas 13：解析日期并制作月度订单汇总

## 本章解决什么实际问题

CSV 中的加入日期和订单日期是文本，格式还可能不同。字符串不能可靠回答“这笔订单属于哪个月”“一月份总金额多少”。本章把文本解析为 pandas 日期，提取年月、筛选日期范围并按月汇总。

## 1. `to_datetime()` 把文本转成日期

```python
import pandas as pd

dates = pd.Series(["2025-01-12", "2024/03/18", "wrong"])
parsed = pd.to_datetime(
    dates,
    errors="coerce",
    format="mixed",
)

print(parsed.dt.strftime("%Y-%m-%d").tolist())
print(parsed.isna().tolist())
```

```text
['2025-01-12', '2024-03-18', nan]
[False, False, True]
```

无效文本变成 `NaT`。转换后先统计缺失，不能悄悄忽略转换失败。

## 2. 使用 `.dt` 提取年和月

```python
import pandas as pd

customers = pd.DataFrame(
    {"join_date": ["2025-01-12", "2024-03-18"]}
)
customers["join_date"] = pd.to_datetime(customers["join_date"])
customers["join_year"] = customers["join_date"].dt.year
customers["join_month"] = customers["join_date"].dt.month

print(customers[["join_year", "join_month"]].to_dict("records"))
```

```text
[{'join_year': 2025, 'join_month': 1}, {'join_year': 2024, 'join_month': 3}]
```

`.dt` 是日期访问器，类似文本列的 `.str`。

## 3. 筛选闭合日期范围

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "order_id": ["O1", "O2", "O3"],
        "order_date": pd.to_datetime(
            ["2025-01-01", "2025-01-31", "2025-02-01"]
        ),
    }
)
mask = orders["order_date"].between(
    pd.Timestamp("2025-01-01"),
    pd.Timestamp("2025-01-31"),
)

print(orders.loc[mask, "order_id"].tolist())
```

```text
['O1', 'O2']
```

起止日期都包含在内。函数还应检查开始日期不能晚于结束日期。

## 4. 按月汇总订单金额

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "order_date": pd.to_datetime(
            ["2025-01-01", "2025-01-10", "2025-02-01"]
        ),
        "quantity": [2, 1, 1],
        "unit_price": [50, 50, 80],
    }
)
orders["order_total"] = orders["quantity"] * orders["unit_price"]
orders["order_month"] = orders["order_date"].dt.strftime("%Y-%m")
summary = (
    orders.groupby("order_month", as_index=False)["order_total"]
    .sum()
)

print(summary.to_dict("records"))
```

```text
[{'order_month': '2025-01', 'order_total': 150}, {'order_month': '2025-02', 'order_total': 80}]
```

先计算每行金额，再用 `YYYY-MM` 作为月份分组键。

## 5. 本章代码流程

```text
日期文本
  ↓ pd.to_datetime(errors="coerce", format="mixed")
真正的 datetime
  ↓ 检查 NaT
dt.year / dt.month / dt.strftime
  ↓
范围筛选或月份分组
```

## 6. 常见错误

### 错误一：直接比较不同格式的日期字符串

字符串按字符顺序比较，不代表真实时间顺序。先转为 datetime。

### 错误二：无效日期没有检查

例如 2 月 30 日会变成 `NaT`。转换后统计 `isna().sum()`。

### 错误三：开始日期晚于结束日期

本课程练习主动抛出 `ValueError`，避免返回一个令人误解的空表。

### 错误四：在转换前使用 `.dt`

`.dt` 只适用于日期类型。字符串列先用 `pd.to_datetime()`。

## 7. 与 IOM103 原项目的对应

原始 IOM103 模型脚本没有日期字段转换，因此本章不是对原脚本某一行的复制。它来自本课程 sample 客户和订单数据的真实字段，为按加入月份或订单月份进行业务分析补充基础。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `add_date_parts()`：安全解析客户加入日期并提取年月。
2. `filter_orders_by_date()`：验证起止日期并保留闭区间订单。
3. `monthly_order_totals()`：排除无效日期并生成月度金额汇总。

## 9. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""日期解析与 dt 访问器演示。"""

import pandas as pd

from utils.paths import DATA_DIR


def demo_date_parts() -> pd.DataFrame:
    """演示安全解析日期并提取年、月和星期，不做分组汇总。"""
    orders = pd.read_csv(DATA_DIR / "sample_orders.csv")
    parsed = pd.to_datetime(orders["order_date"], errors="coerce", format="mixed")
    return pd.DataFrame(
        {
            "order_date": parsed,
            "year": parsed.dt.year,
            "month": parsed.dt.month,
            "weekday": parsed.dt.day_name(),
        }
    ).head(5)


def main() -> None:
    print(demo_date_parts().to_dict("records"))


if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/pandas/13_date_operations/test.py
```

## 10. 本章检查清单

- 我知道 CSV 日期最初可能只是字符串。
- 我能安全转换混合格式日期并识别 `NaT`。
- 我能用 `.dt` 提取年、月或格式化月份。
- 我会验证日期范围的先后顺序。
- 我能先计算行级金额，再做月度汇总。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>add_date_parts</code></summary>

pd.to_datetime(..., errors="coerce", format="mixed") 后使用 .dt。

</details>

<details>
<summary><code>filter_orders_by_date</code></summary>

先用 pd.to_datetime() 转边界，再用 between()。

</details>

<details>
<summary><code>monthly_order_totals</code></summary>

日期列的 .dt.strftime("%Y-%m") 可生成月份文本。

</details>
