# Pandas 02：从 CSV 读取客户和订单数据

## 本章解决什么实际问题

真实分析的数据通常不直接写在 Python 代码里，而是保存在 CSV 文件中。你需要读取客户表、只取报告需要的列，并把订单日期从文本转换为真正的日期。

CSV（Comma-Separated Values）是一种文本表格格式：第一行通常是列名，后面每行是一条记录。

## 1. 用 `read_csv()` 读取文件

项目已经用 `utils.paths.DATA_DIR` 记录了数据目录，所以不需要写死电脑上的绝对路径。

```python
import pandas as pd
from utils.paths import DATA_DIR

customers = pd.read_csv(DATA_DIR / "sample_customers.csv")

print(customers.shape)
print(customers.columns.tolist())
```

```text
(31, 9)
['customer_id', 'age', 'gender', 'city', 'monthly_spending', 'contract_type', 'join_date', 'churn', 'satisfaction_score']
```

`DATA_DIR / "sample_customers.csv"` 使用 `pathlib` 拼接路径，在 Windows 和其他系统上都比手写斜杠可靠。

## 2. 读取后先看几条记录

```python
import pandas as pd
from utils.paths import DATA_DIR

customers = pd.read_csv(DATA_DIR / "sample_customers.csv")

print(customers[["customer_id", "city"]].head(2).to_dict("records"))
```

```text
[{'customer_id': 'C001', 'city': 'Suzhou'}, {'customer_id': 'C002', 'city': 'Shanghai'}]
```

`head(2)` 返回开头两行。读取成功不代表数据已经干净，所以现在只做快速确认。

## 3. 只返回需要的列

分析报告只需要少数列时，可以读取后按指定顺序选择：

```python
import pandas as pd
from utils.paths import DATA_DIR

customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
columns = ["city", "customer_id"]
selected = customers.loc[:, columns]

print(selected.columns.tolist())
print(selected.shape)
```

```text
['city', 'customer_id']
(31, 2)
```

`.loc[:, columns]` 中冒号表示“所有行”，`columns` 表示“这些列”。

## 4. 读取后转换日期

CSV 是文本文件，日期常先被读成字符串。`pd.to_datetime()` 把它转为 pandas 日期：

```python
import pandas as pd

orders = pd.DataFrame(
    {"order_date": ["2025-01-15", "2025/02/02", "wrong"]}
)
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce",
    format="mixed",
)

print(orders["order_date"].dt.strftime("%Y-%m-%d").tolist())
print(orders["order_date"].isna().tolist())
```

```text
['2025-01-15', '2025-02-02', nan]
[False, False, True]
```

`errors="coerce"` 的含义是：无法转换的值不让程序中断，而是变成日期缺失值 `NaT`。`format="mixed"` 允许同一列中出现多种常见日期格式。

## 5. 本章代码流程

```text
Path 文件路径
      ↓
pd.read_csv()
      ↓
检查 shape 和 columns
      ↓
选择需要的列或转换日期
      ↓
返回 DataFrame
```

## 6. 常见错误

### 错误一：运行位置不对

模块示例必须从项目根目录运行。如果在 `examples/pandas/` 内直接启动，`utils` 包可能无法找到。

### 错误二：写死绝对路径

个人电脑上的桌面绝对路径只在一台电脑有效。项目数据使用 `DATA_DIR / "文件名.csv"`，练习函数则接收 `Path` 参数。

### 错误三：文件名或列名拼错

文件不存在会抛出 `FileNotFoundError`；选择不存在的列会抛出 `KeyError`。不要用宽泛的 `try/except` 隐藏这些错误，否则更难发现拼写问题。

### 错误四：以为读入后数字一定是数值

一列只要混入 `"unknown"`，就可能成为文本类型。读取和类型清理是两个步骤，第 7 节会专门处理。

## 7. 与 IOM103 原项目的对应

原项目的 `prepare_churn_data()` 使用 `pd.read_csv()` 读取流失数据；`task_b_customer_segmentation()` 也用它读取客户分群数据。这两处读取的是两份独立 CSV，本章练习使用项目自己的小型 sample CSV 复现同一入口。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `load_customers()`：读取完整客户 CSV，并保留正常文件错误。
2. `load_customer_columns()`：按调用者给出的顺序返回指定列。
3. `load_orders_with_dates()`：读取订单并把无效日期安全转换为 `NaT`。

## 9. 运行命令

```powershell
python -m examples.pandas.example_02_read_csv
pytest tests/pandas/test_pandas_practice.py -k "answer_02 or practice_02"
```

## 10. 本章检查清单

- 我知道 CSV 是文本表格，不会假设每列类型都正确。
- 我能使用相对项目路径读取 CSV。
- 我能用 `shape` 和 `columns` 验证读取结果。
- 我能按指定顺序选择少量列。
- 我能解释无效日期为什么会变成 `NaT`。
