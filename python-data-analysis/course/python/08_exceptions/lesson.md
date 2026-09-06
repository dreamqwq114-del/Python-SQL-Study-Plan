# 08. 异常：让错误数据尽早停止

## 1. 本章解决什么实际问题

用户或表格可能提供以下金额：

```text
"12.5"
"0"
"unknown"
""
```

如果错误数据悄悄进入后续统计，最终结果可能看似正常却完全错误。**异常**是 Python 表示“当前操作无法正常完成”的方式。本章学习：

- 识别常见异常；
- 使用 `raise` 主动拒绝不合理数据；
- 使用 `try/except` 在明确场景中处理错误；
- 不用宽泛捕获掩盖真正的问题。

---

## 2. 转换失败会产生异常

```python
amount = float("12.5")
print(amount)
```

运行结果：

```text
12.5
```

但 `float("unknown")` 无法转换，会产生 `ValueError`。错误信息不是“程序坏了”，而是在告诉你输入不满足函数要求。

---

## 3. 主动抛出 `ValueError`

`float("0")` 可以转换，但如果业务规定金额必须大于 0，就要主动检查。

```python
def parse_positive_amount(text):
    amount = float(text)
    if amount <= 0:
        raise ValueError("金额必须大于 0")
    return amount

print(parse_positive_amount("12.5"))
```

运行结果：

```text
12.5
```

`raise` 表示立即抛出异常，函数不会继续向下执行。

---

## 4. `try/except` 处理预期错误

```python
def parse_positive_amount(text):
    amount = float(text)
    if amount <= 0:
        raise ValueError("金额必须大于 0")
    return amount

for text in ["12.5", "0", "bad"]:
    try:
        amount = parse_positive_amount(text)
        print(f"{text} -> {amount}")
    except ValueError as error:
        print(f"{text} -> 错误：{error}")
```

运行结果：

```text
12.5 -> 12.5
0 -> 错误：金额必须大于 0
bad -> 错误：could not convert string to float: 'bad'
```

这里只捕获 `ValueError`，因为我们明确知道数据转换可能失败。

---

## 5. 区分缺失值与错误值

空字符串和 `"NA"` 可以按题目契约表示缺失，返回 `None`；`"abc"` 则是错误格式。

```python
def parse_optional_score(text):
    cleaned = text.strip()
    if cleaned == "" or cleaned == "NA":
        return None
    score = float(cleaned)
    if score < 0 or score > 100:
        raise ValueError("成绩必须在 0 到 100 之间")
    return score

print(parse_optional_score("88.5"))
print(parse_optional_score(" NA "))
```

运行结果：

```text
88.5
None
```

什么代表缺失必须由数据说明决定，不能随意猜测。

---

## 6. 捕获文件不存在并转换错误

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "required.txt"
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        print("必需文件不存在")
```

运行结果：

```text
必需文件不存在
```

底层是 `FileNotFoundError`，业务函数可以根据契约把它转换成更统一的 `ValueError`，并使用 `raise ... from error` 保留原始原因。

---

## 7. 不要捕获所有异常

下面写法不推荐：

```python
try:
    result = some_operation()
except:
    result = None
```

它会把拼写错误、逻辑错误和系统错误全部隐藏。只捕获你知道如何处理的具体异常；无法正确处理时，让异常继续出现。

---

## 8. 常见错误

### 错误 1：只捕获错误但不修正状态

打印“失败”后继续使用未创建的变量，会产生新的错误。处理异常后要么返回明确结果，要么停止当前流程。

### 错误 2：错误地把所有失败值变成 0

0 是真实数据，缺失和格式错误不是 0。随意替换会改变统计结果。

### 错误 3：异常类型写错

数字转换失败是 `ValueError`，文件不存在是 `FileNotFoundError`，字典缺键是 `KeyError`。先读错误最后一行，再决定处理方式。

### 错误 4：用异常替代普通条件

金额是否小于 0 是普通业务判断，应先用 `if` 检查，再 `raise ValueError`。

---

## 9. IOM103 对应位置

IOM103 的 `TotalCharges` 列包含空白文本。原项目使用 `pd.to_numeric(..., errors="coerce")` 把无法转换的值变成缺失，而不是逐行 `try/except`。这是一种批量数据处理策略；本章先帮助你理解“为什么转换可能失败，以及失败后必须有明确规则”。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 2、3、12 节；
- 原项目只读脚本 `prepare_churn_data()` 中 `TotalCharges` 的转换。

---

## 10. 本章练习

打开 `course/python/08_exceptions/practice.py`：

1. `parse_positive_amount`：转换并验证正金额；
2. `parse_optional_score`：区分缺失和错误；
3. `safe_divide`：拒绝分母为 0；
4. `read_required_text`：处理必需文件缺失或为空。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""使用 try/except 保护输入转换演示。"""


def demo_parse_seat(text: str) -> int:
    """把座位号文本转成整数，并演示何时主动抛出异常。"""
    seat = int(text)
    if seat < 1:
        raise ValueError("座位号至少为 1")
    return seat


def main() -> None:
    for text in ["12", "0", "abc"]:
        try:
            print(text, "->", demo_parse_seat(text))
        except ValueError as error:
            print(text, "-> 无法使用：", error)


if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/08_exceptions/test.py
```

---

## 11. 本章检查清单

- 我知道异常表示操作无法正常完成；
- 我能读懂 `ValueError`、`FileNotFoundError` 和 `KeyError`；
- 我能使用 `raise` 拒绝不合理输入；
- 我只捕获自己能够处理的具体异常；
- 我不会把缺失、错误和真实的 0 混在一起；
- 我知道 Pandas 的批量转换也需要明确失败规则。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>parse_positive_amount</code></summary>

float() 已经会为无法转换的文本产生 ValueError。

</details>

<details>
<summary><code>parse_optional_score</code></summary>

先处理缺失标记，再调用 float()，可以避免对 "NA" 进行转换。

</details>

<details>
<summary><code>safe_divide</code></summary>

使用 if 检查分母，再执行除法。

</details>

<details>
<summary><code>read_required_text</code></summary>

使用 try/except 捕获 FileNotFoundError，并用 raise ValueError(...) from error。

</details>
