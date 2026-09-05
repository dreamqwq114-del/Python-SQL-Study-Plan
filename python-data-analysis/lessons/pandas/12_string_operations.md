# Pandas 12：批量清理文本列

## 本章解决什么实际问题

同一城市在数据中可能写成 `"Suzhou"`、`" suzhou "`；商品名称可能有多余空格。肉眼看起来相同的值会被分组为不同类别。本章通过 `.str` 对整列文本去空格、统一大小写、搜索关键词并生成规范键。

## 1. `.str.strip()` 去掉两端空格

```python
import pandas as pd

cities = pd.Series([" Suzhou ", "Shanghai", None])
cleaned = cities.str.strip()

print(cleaned.tolist())
```

```text
['Suzhou', 'Shanghai', nan]
```

`.str` 是 pandas 的字符串访问器，表示接下来的字符串操作应用到整列。缺失值通常保持缺失。

## 2. 统一大小写

```python
import pandas as pd

cities = pd.Series(["Suzhou", "SUZHOU", " suzhou "])
cleaned = cities.str.strip().str.lower()

print(cleaned.tolist())
print(cleaned.nunique())
```

```text
['suzhou', 'suzhou', 'suzhou']
1
```

清理前可能被当成三个类别，清理后只有一个。也可以使用 `.str.upper()` 统一为大写。

## 3. `str.contains()` 搜索普通文本

```python
import pandas as pd

products = pd.Series(["USB Cable", "Phone Case", "Mouse", None])
mask = products.str.contains(
    "usb",
    case=False,
    na=False,
    regex=False,
)

print(mask.tolist())
print(products.loc[mask].tolist())
```

```text
[True, False, False, False]
['USB Cable']
```

- `case=False`：不区分大小写；
- `na=False`：缺失商品名视为不匹配；
- `regex=False`：关键词按普通文本，而不是正则表达式解释。

正则表达式是一套文本模式语法。本章搜索普通商品关键词，不需要它，因此明确关闭。

## 4. 把连续空白替换为下划线

```python
import pandas as pd

products = pd.Series([" USB Cable ", "Phone   Case"])
keys = (
    products.str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
)

print(keys.tolist())
```

```text
['usb_cable', 'phone_case']
```

这里 `r"\s+"` 是正则模式，表示一个或多个连续空白。它适合把不确定数量的空格统一为一个下划线。

## 5. 本章代码流程

```text
先用 value_counts() 查看脏类别
       ↓
str.strip() 去两端空格
       ↓
str.lower() 或 str.upper() 统一大小写
       ↓
contains / replace 完成搜索或规范化
       ↓
再次检查 unique / value_counts
```

## 6. 常见错误

### 错误一：忘记 `.str`

Series 不是单个字符串，不能直接写 `series.strip()`。应写 `series.str.strip()`。

### 错误二：没有处理缺失值

搜索时不写 `na=False`，结果 mask 可能含缺失值，无法安全用于筛选。

### 错误三：关键词被当成正则

用户搜索 `"."` 时，正则中的点代表任意字符。普通文本搜索要写 `regex=False`。

### 错误四：清理后不验证

再次查看 `unique()` 或 `value_counts()`，确认 `"Suzhou"` 的多个写法已经合并。

## 7. 与 IOM103 原项目的对应

原始 IOM103 脚本没有使用 pandas `.str` 清理文本列；它直接对已有类别进行预处理。本章根据本课程 sample CSV 中刻意加入的大小写和空格问题补充真实数据清洗技能，为后续正确分组和类别编码做准备。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `clean_text_fields()`：清理城市与合同字段，保留缺失值。
2. `filter_products_by_keyword()`：不区分大小写地搜索普通文本关键词。
3. `add_product_key()`：把商品名称变成稳定的小写下划线键。

## 9. 运行命令

```powershell
python -m examples.pandas.example_12_string_operations
pytest tests/pandas/test_pandas_practice.py -k "answer_12 or practice_12"
```

## 10. 本章检查清单

- 我会用 `.str` 对整列文本操作。
- 我能去掉两端空格并统一大小写。
- 我能让缺失商品名在搜索时安全返回 False。
- 我知道普通文本搜索为什么使用 `regex=False`。
- 我会在清理后重新检查类别数量。
