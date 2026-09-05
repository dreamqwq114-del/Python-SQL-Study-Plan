# 06. 模块与导入：把项目代码分到不同文件

## 1. 本章解决什么实际问题

数据项目通常至少有三类路径：

- `data/`：原始或学习数据；
- `data/processed/`：处理后的表格；
- `figures/`：分析图片。

如果每个脚本都自己写目录，很容易拼错或写成本机绝对路径。本项目把统一路径放在 `utils/paths.py`，其他文件通过 `import` 使用。本章学习模块、导入方式和 `if __name__ == "__main__"`。

---

## 2. 什么是模块

一个 `.py` 文件就是一个 Python 模块。例如：

```text
utils/paths.py
course/python/06_modules_and_imports/example.py
```

模块可以保存函数、类和变量。拆分模块的目的不是增加文件数量，而是让一份定义可以被多个脚本复用。

---

## 3. 导入标准库

Python 安装时自带的模块叫作**标准库**。`pathlib` 是处理路径的标准库模块。

```python
from pathlib import Path

file_path = Path("data") / "customers.csv"

print(file_path)
print(file_path.name)
print(file_path.suffix)
```

运行结果在 Windows 上是：

```text
data\customers.csv
customers.csv
.csv
```

`from pathlib import Path` 表示从 `pathlib` 模块中导入 `Path`。

---

## 4. 导入项目自己的模块

本项目的 `utils/paths.py` 定义：

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FIGURE_DIR = PROJECT_ROOT / "figures"
```

其他模块可以导入其中的常量：

```python
from utils.paths import DATA_DIR, PROJECT_ROOT

customer_path = DATA_DIR / "sample_customers.csv"

print(PROJECT_ROOT.name)
print(customer_path.name)
print(customer_path.parent.name)
```

在当前项目中运行结果：

```text
IOM103_Python_Data_Analysis
sample_customers.csv
data
```

**常量**是程序约定不随意重新赋值的变量，通常使用全大写名称。

---

## 5. 三种常见导入方式

```python
import pathlib
from pathlib import Path
import pathlib as pl
```

- `import pathlib` 后写 `pathlib.Path(...)`，来源最清楚；
- `from pathlib import Path` 后直接写 `Path(...)`，最简洁；
- `as` 给模块设置别名，只有常见或确实更清楚时才使用。

不要写 `from module import *`。它会把很多名称带入当前文件，很难看出名称来自哪里。

---

## 6. 为什么示例使用 `python -m`

从项目根目录运行：

```powershell
python -m course.python.06_modules_and_imports.example
```

Python 会把项目根目录放入模块搜索路径，因此 `from utils.paths import ...` 可以正常工作。直接进入子目录运行文件，可能找不到 `utils`。

---

## 7. 模块被导入时不要自动执行演示

```python
def main():
    print("只在直接运行模块时执行")


if __name__ == "__main__":
    main()
```

直接运行模块时，`__name__` 等于 `"__main__"`；被其他文件导入时，下面的 `main()` 不会自动执行。这能防止“只想导入函数，却意外打印或写文件”。

---

## 8. 用统一常量构造路径

```python
from utils.paths import DATA_DIR, FIGURE_DIR

data_path = DATA_DIR / "sample_customers.csv"
figure_path = FIGURE_DIR / "customers.png"

print(data_path.name)
print(figure_path.name)
```

运行结果：

```text
sample_customers.csv
customers.png
```

代码没有写死某台电脑的用户目录，因此换一台电脑后仍能从项目根目录计算路径。

---

## 9. 常见错误

### 错误 1：写死绝对路径

```python
file_path = "/某台电脑上的绝对路径/data.csv"
```

这只适用于一台电脑。项目文件应从 `PROJECT_ROOT`、`DATA_DIR` 等常量拼接。

### 错误 2：模块名与变量名冲突

```python
pathlib = "text"
```

之后再写 `pathlib.Path` 会失败。变量名不要覆盖已导入模块名。

### 错误 3：在导入时执行写文件代码

把演示调用放进 `if __name__ == "__main__"`，函数和常量才能安全复用。

### 错误 4：从错误工作目录直接运行子文件

统一从项目根目录使用 `python -m 包.模块`。

---

## 10. IOM103 对应位置

IOM103 原脚本集中导入 Pandas、Matplotlib、scikit-learn 与 `Path`，并通过多个函数组织读取、训练和绘图。本学习项目进一步把路径常量拆到 `utils.paths`，避免示例依赖 IDEA 的特殊设置。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 3、12 节；
- 原项目只读脚本顶部导入区和路径初始化代码。

---

## 11. 本章练习

打开 `course/python/06_modules_and_imports/practice.py`：

1. `build_data_path`：构造原始数据路径；
2. `build_processed_path`：构造处理结果路径；
3. `build_figure_path`：构造图片路径；
4. `get_project_directories`：汇总导入的目录常量。

运行：

```powershell
python -m course.python.06_modules_and_imports.example
pytest course/python/06_modules_and_imports/test.py
```

---

## 12. 本章检查清单

- 我知道一个 `.py` 文件就是一个模块；
- 我能从标准库和项目模块导入名称；
- 我不会使用 `import *`；
- 我能从统一目录常量构造相对项目路径；
- 我知道为什么从根目录使用 `python -m`；
- 我能解释 `if __name__ == "__main__"` 的作用。
