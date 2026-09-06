# Matplotlib 06：可靠保存图片并释放 Figure

## 本章解决什么实际问题

最终报告需要图片文件，不是只在 PyCharm 中弹出窗口。同一张城市图可能既要网页使用的 PNG，也要报告使用的 PDF。批量生成图片时，还必须关闭 Figure，避免几十张图持续占用内存。

## 1. 创建父目录并保存

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with TemporaryDirectory() as directory:
    path = Path(directory) / "reports" / "churn.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots()
    axis.bar(["0", "1"], [2, 1])
    figure.savefig(path, dpi=150)
    plt.close(figure)
    print(path.exists())
    print(path.stat().st_size > 0)
```

```text
True
True
```

`savefig()` 不会自动创建父目录，因此保存前使用 `mkdir()`。

## 2. DPI 和紧边界

`dpi` 是每英寸点数，影响位图清晰度。本课程报告图使用至少 120 dpi，统一答案使用 150 或 200 dpi。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with TemporaryDirectory() as directory:
    path = Path(directory) / "figure.png"
    figure, axis = plt.subplots()
    axis.plot([1, 2], [100, 200])
    axis.set_xlabel("Month")
    figure.tight_layout()
    figure.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    print(path.suffix)
    print(path.stat().st_size > 0)
```

```text
.png
True
```

`bbox_inches="tight"` 会在保存时收紧图片边界，减少轴标签被裁切的风险。

## 3. 透明背景

PNG 可以保存透明背景，便于叠加在不同颜色的版面上：

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with TemporaryDirectory() as directory:
    path = Path(directory) / "transparent.png"
    figure, axis = plt.subplots()
    axis.scatter([20, 30], [100, 200])
    figure.savefig(path, dpi=200, transparent=True)
    plt.close(figure)
    print(path.exists())
    print(path.stat().st_size > 0)
```

```text
True
True
```

透明背景只影响画布背景，不会让数据点消失。

## 4. 同一 Figure 保存两种格式

```python
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with TemporaryDirectory() as directory:
    output = Path(directory)
    paths = [
        output / "city_counts.png",
        output / "city_counts.pdf",
    ]
    figure, axis = plt.subplots()
    axis.bar(["A", "B"], [2, 1])
    for path in paths:
        figure.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    print([path.suffix for path in paths])
    print(all(path.stat().st_size > 0 for path in paths))
```

```text
['.png', '.pdf']
True
```

PNG 是像素图，适合网页和普通文档；PDF 中的图形可以保持矢量缩放。只需绘制一次，再保存两次。

## 5. 为什么必须关闭

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

first, _ = plt.subplots()
second, _ = plt.subplots()
print(len(plt.get_fignums()))
plt.close(first)
plt.close(second)
print(len(plt.get_fignums()))
```

```text
2
0
```

`plt.get_fignums()` 返回当前仍打开的 Figure 编号。测试会在每道题后要求它为空。

## 6. 正确保存顺序

```text
准备最终数据
  ↓
figure, axis = plt.subplots()
  ↓
绘图、标题、轴标签、图例
  ↓
figure.tight_layout()
  ↓
创建 output_path.parent
  ↓
figure.savefig(...)
  ↓
plt.close(figure)
```

关闭必须发生在保存之后。先关闭再保存可能得到空白图或不可预测结果。

## 7. 常见错误

### 错误一：只 `show()` 不保存

交互窗口关闭后没有可提交文件。课程示例和练习都以文件输出为准。

### 错误二：保存后不关闭

单张图可能看不出问题，循环生成很多图时会积累内存并触发警告。

### 错误三：使用相对当前文件的随意路径

函数接收 `Path`，测试使用临时目录；真实项目使用统一的输出目录。

### 错误四：为 PNG 和 PDF重复绘图

同一内容只创建一次 Figure，分别调用两次 `savefig()`，最后关闭一次。

## 8. 与 IOM103 原项目的对应

原项目定义统一的 `save_plot()`：先进行紧凑布局，再以 300 dpi 和紧边界保存到 figures 目录，最后关闭图形。合同流失率、ROC、特征重要性、聚类评估和分群图都通过这个流程输出。本节直接训练相同的可靠保存习惯。

详见 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 9. 本节练习

1. `save_churn_figure()`：以 150 dpi、紧边界保存流失计数图。
2. `save_transparent_spending_scatter()`：以 200 dpi 保存透明 PNG。
3. `save_city_figure_formats()`：同一 Figure 输出 PNG 和 PDF 路径。

## 10. 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""把同一张图保存为 PNG 和 PDF，并关闭 Figure。"""

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from utils.paths import DATA_DIR

def save_city_formats(
    dataframe: pd.DataFrame,
    output_directory: Path,
) -> list[Path]:
    """把城市客户数图保存为 PNG 和 PDF。"""
    city = dataframe["city"].str.strip().str.lower()
    counts = city.value_counts().sort_index()
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.bar(counts.index, counts.values)
    axis.set(
        title="Customers by City",
        xlabel="City",
        ylabel="Customer Count",
    )
    figure.tight_layout()
    output_directory.mkdir(parents=True, exist_ok=True)
    paths = [
        output_directory / "city_counts.png",
        output_directory / "city_counts.pdf",
    ]
    for path in paths:
        figure.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    return paths

def main() -> None:
    customers = pd.read_csv(DATA_DIR / "sample_customers.csv")
    with TemporaryDirectory() as directory:
        paths = save_city_formats(customers, Path(directory))
        print([path.suffix for path in paths])
        print(all(path.exists() and path.stat().st_size > 0 for path in paths))
        print(len(plt.get_fignums()))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/matplotlib/06_save_figures/test.py
```

## 11. 本章检查清单

- 我会在保存前创建父目录。
- 我能解释 DPI 与紧边界的作用。
- 我会在需要时保存透明 PNG。
- 我能让同一 Figure 输出多个格式。
- 我会在所有路径中保存后关闭 Figure，并验证文件非空。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>save_churn_figure</code></summary>

保存必须发生在 plt.close(fig) 之前。

</details>

<details>
<summary><code>save_transparent_spending_scatter</code></summary>

fig.savefig(..., dpi=200, transparent=True, bbox_inches="tight")。

</details>

<details>
<summary><code>save_city_figure_formats</code></summary>

只创建一个 Figure，对两个 Path 分别调用 fig.savefig()，最后关闭。

</details>
