# Pandas 14：把清洗结果安全保存为 CSV

## 本章解决什么实际问题

分析结果只存在内存里，关闭 Python 就会消失。你需要创建输出目录，把完整清洗表、指定列报告或城市汇总保存为 CSV，并重新读取验证文件内容。

本章强调：路径由调用者传入、不写 DataFrame 索引、保存后验证。

## 1. 用 `to_csv()` 保存

下面使用临时目录演示，不会在项目里留下输出文件：

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

customers = pd.DataFrame(
    {"customer_id": ["C1", "C2"], "city": ["A", "B"]}
)

with TemporaryDirectory() as directory:
    path = Path(directory) / "customers.csv"
    customers.to_csv(path, index=False, encoding="utf-8")
    reloaded = pd.read_csv(path)
    print(path.exists())
    print(reloaded.to_dict("records"))
```

```text
True
[{'customer_id': 'C1', 'city': 'A'}, {'customer_id': 'C2', 'city': 'B'}]
```

`index=False` 表示不把 DataFrame 的 0、1、2 索引写成额外数据列。

## 2. 创建尚不存在的父目录

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

report = pd.DataFrame({"city": ["A"], "customer_count": [2]})

with TemporaryDirectory() as directory:
    path = Path(directory) / "reports" / "city.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(path, index=False, encoding="utf-8")
    print(path.exists())
```

```text
True
```

- `parents=True`：需要时连同多层父目录一起创建；
- `exist_ok=True`：目录已存在也不报错。

## 3. 只保存允许的列

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

customers = pd.DataFrame(
    {
        "customer_id": ["C1"],
        "age": [20],
        "internal_note": ["private"],
    }
)

with TemporaryDirectory() as directory:
    path = Path(directory) / "public.csv"
    customers.loc[:, ["age", "customer_id"]].to_csv(
        path,
        index=False,
        encoding="utf-8",
    )
    print(pd.read_csv(path).columns.tolist())
```

```text
['age', 'customer_id']
```

先明确选择列，可以避免把内部字段意外写进对外文件。

## 4. 先汇总再保存

```python
import pandas as pd

customers = pd.DataFrame({"city": ["A", "A", "B", None]})
summary = (
    customers.groupby("city")
    .size()
    .reset_index(name="customer_count")
)

print(summary.to_dict("records"))
```

```text
[{'city': 'A', 'customer_count': 2}, {'city': 'B', 'customer_count': 1}]
```

保存函数不一定只能原样写出 DataFrame，也可以先产生符合报告需要的汇总表。

## 5. 本章代码流程

```text
准备最终 DataFrame
       ↓
明确目标 Path 和允许列
       ↓
path.parent.mkdir(...)
       ↓
to_csv(index=False, encoding="utf-8")
       ↓
read_csv() 重新读取验证
```

## 6. 常见错误

### 错误一：忘记 `index=False`

重新读取后出现 `Unnamed: 0`，通常就是把索引写进了 CSV。保存业务表时一般不需要它。

### 错误二：父目录不存在

`to_csv()` 不会自动创建目录。先调用 `mkdir()`。

### 错误三：写死桌面绝对路径

保存函数接收 `Path` 参数，测试传临时目录，真实项目可传统一输出目录。

### 错误四：保存成功就不验证

至少检查文件存在、行列数正确、没有额外索引列。关键结果还应重新读取比较。

## 7. 与 IOM103 原项目的对应

原项目多次使用 `to_csv(index=False)` 保存模型指标、重要特征、聚类数量评估、带聚类标签的客户表和分群汇总。本章对应的是这些分析结果从内存落到可提交文件的最后一步。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 8. 本节练习

1. `save_processed()`：创建父目录并保存完整表。
2. `save_selected_columns()`：只按指定顺序保存允许列。
3. `save_city_summary()`：先统计城市客户数，再保存汇总 CSV。

所有保存练习都写入 pytest 临时目录，不会污染项目数据目录。

## 9. 运行命令

```powershell
python -m course.pandas.14_save_data.example
pytest course/pandas/14_save_data/test.py
```

## 10. 本章检查清单

- 我能创建目标文件的父目录。
- 我知道为什么业务 CSV 常使用 `index=False`。
- 我能控制输出列及顺序。
- 我不会在函数中写死个人电脑路径。
- 我会重新读取结果，验证行列和内容。
