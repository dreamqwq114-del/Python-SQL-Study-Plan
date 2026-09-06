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

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 2、3、12 节；
- 原项目只读脚本中的 `pd.read_csv()`、`to_csv()` 和 `savefig()` 调用。

---

## 10. 本章练习

打开 `course/python/07_files_and_paths/practice.py`：

1. `read_first_line`：读取第一行；
2. `read_nonempty_lines`：清理非空行；
3. `write_report`：创建目录并写报告；
4. `count_csv_rows`：跳过表头统计记录。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""使用 pathlib 读写 UTF-8 文件示例。"""

from pathlib import Path
from tempfile import TemporaryDirectory

def write_report(file_path: Path, lines: list[str]) -> None:
    """创建父目录并写入多行报告。"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def read_nonempty_lines(file_path: Path) -> list[str]:
    """返回清理后的非空行。"""
    result: list[str] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()
        if cleaned:
            result.append(cleaned)
    return result

def main() -> None:
    with TemporaryDirectory() as temporary_directory:
        report_path = Path(temporary_directory) / "outputs" / "summary.txt"
        write_report(report_path, ["客户数：3", "流失数：1"])

        print("文件存在：", report_path.exists())
        print("文件名：", report_path.name)
        print("报告内容：", read_nonempty_lines(report_path))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/07_files_and_paths/test.py
```

---

## 11. 本章检查清单

- 我能区分路径、文件对象和文件内容；
- 我能用 `Path` 拼接路径并检查是否存在；
- 我能以 UTF-8 读取和写入文本；
- 我知道 `with` 会自动关闭文件；
- 我能在写入前创建父目录；
- 我知道 CSV 表头不属于数据记录。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>read_first_line</code></summary>

可以使用 file_path.open() 和文件对象的 readline()。

</details>

<details>
<summary><code>read_nonempty_lines</code></summary>

可以在列表推导式前先写普通 for 循环，理解后再决定是否简化。

</details>

<details>
<summary><code>write_report</code></summary>

file_path.parent.mkdir(parents=True, exist_ok=True) 可创建父目录。

</details>

<details>
<summary><code>count_csv_rows</code></summary>

先用 next(reader, None) 读取表头，再循环统计后续行。

</details>
