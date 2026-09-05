# 07. 文件与路径：读取输入并保存分析结果

## 1. 本章解决什么实际问题

数据分析不会只在变量中进行。原始数据来自磁盘，清洗结果和报告也要保存到磁盘。本章暂时不使用 Pandas，而是用 Python 标准库完成：

- 读取文本第一行；
- 清理并保留非空行；
- 创建输出目录并写报告；
- 统计 CSV 的数据行数。

这些操作帮助你理解“路径指向文件，打开文件后才读取内容”。

---

## 2. 使用 `Path` 表示路径

```python
from pathlib import Path

file_path = Path("data") / "sample_customers.csv"

print(file_path.name)
print(file_path.suffix)
print(file_path.parent)
```

在 Windows 中运行结果：

```text
sample_customers.csv
.csv
data
```

`Path` 只表示位置，不代表文件一定存在。

```python
from pathlib import Path

file_path = Path("not_exists.txt")
print(file_path.exists())
```

运行结果：

```text
False
```

---

## 3. 读取文本文件

`with` 会在代码块结束后自动关闭文件。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "note.txt"
    path.write_text("first\nsecond\n", encoding="utf-8")

    with path.open("r", encoding="utf-8") as file:
        first_line = file.readline().rstrip("\r\n")

    print(first_line)
```

运行结果：

```text
first
```

明确写 `encoding="utf-8"`，可以减少中文在不同电脑上出现乱码的风险。

---

## 4. 一次读取多行并清理

```python
text = " age \n\n city\n"
result = []

for line in text.splitlines():
    cleaned = line.strip()
    if cleaned != "":
        result.append(cleaned)

print(result)
```

运行结果：

```text
['age', 'city']
```

`strip()` 删除文本两边空白，`splitlines()` 按行拆分。

---

## 5. 写入报告并创建父目录

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    report_path = Path(folder) / "outputs" / "summary.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("客户数：3\n流失数：1\n", encoding="utf-8")

    print(report_path.exists())
    print(report_path.read_text(encoding="utf-8"), end="")
```

运行结果：

```text
True
客户数：3
流失数：1
```

- `parents=True` 表示缺少多层目录时一起创建；
- `exist_ok=True` 表示目录已经存在也不报错。

---

## 6. 使用 `csv` 标准库统计记录

CSV 是“逗号分隔值”文件。第一行通常是表头，不算数据记录。

```python
import csv
from io import StringIO

content = StringIO("id,name\n1,A\n2,B\n")
reader = csv.reader(content)
header = next(reader)
row_count = 0

for row in reader:
    row_count += 1

print(header)
print(row_count)
```

运行结果：

```text
['id', 'name']
2
```

这里只学习文件与行。下一领域会使用 Pandas 直接读取 CSV 为 DataFrame。

---

## 7. 文件读写的数据流

```text
Path 表示位置
    ↓
open/read_text 打开并读取
    ↓
字符串或行列表进入 Python
    ↓
清理与计算
    ↓
write_text 把结果写回磁盘
```

路径、文件对象和文件内容是三个不同概念。

---

## 8. 常见错误

### 错误 1：忘记编码

依赖系统默认编码时，中文文件可能在另一台电脑上乱码。课程文本统一使用 UTF-8。

### 错误 2：父目录不存在

直接写入 `outputs/report.txt`，但 `outputs` 不存在，会产生 `FileNotFoundError`。写入前创建父目录。

### 错误 3：把读取模式写成写入模式

`"r"` 是读取，`"w"` 是写入。使用 `"w"` 会覆盖现有文件，写入前必须确认目标是输出文件。

### 错误 4：把表头算成数据行

CSV 第一行通常是列名。统计前先读取并跳过表头。

---

## 9. IOM103 对应位置

IOM103 原项目从三个 CSV 读取数据，把模型指标和客户分群保存到 `outputs/`，把图表保存到 `figures/`。原脚本主要通过 Pandas 完成表格读写，但底层仍是路径、文件和编码。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../ORIGINAL_PROJECT_ANALYSIS.md) 第 2、3、12 节；
- 原项目只读脚本中的 `pd.read_csv()`、`to_csv()` 和 `savefig()` 调用。

---

## 10. 本章练习

打开 `practice/python/practice_07_files_and_paths.py`：

1. `read_first_line`：读取第一行；
2. `read_nonempty_lines`：清理非空行；
3. `write_report`：创建目录并写报告；
4. `count_csv_rows`：跳过表头统计记录。

运行：

```powershell
python -m examples.python.example_07_files_and_paths
pytest tests/python/test_python_practice.py -k "answer_07 or practice_07"
```

---

## 11. 本章检查清单

- 我能区分路径、文件对象和文件内容；
- 我能用 `Path` 拼接路径并检查是否存在；
- 我能以 UTF-8 读取和写入文本；
- 我知道 `with` 会自动关闭文件；
- 我能在写入前创建父目录；
- 我知道 CSV 表头不属于数据记录。
