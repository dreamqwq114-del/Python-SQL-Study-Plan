# 05. 函数：把重复分析步骤变成可复用工具

## 1. 本章解决什么实际问题

订单金额公式是：

```text
数量 × 单价 × (1 - 折扣)
```

如果每处理一条订单都重新写公式，容易出现复制错误。函数可以给一段计算起名字，让不同数据重复使用同一规则。本章会定义函数、传入参数、返回结果，并理解默认参数。

---

## 2. 定义和调用函数

`def` 表示定义函数。函数名后面的变量是参数，`return` 把结果交回调用位置。

```python
def calculate_order_total(quantity, unit_price):
    total = quantity * unit_price
    return total

result = calculate_order_total(3, 20)
print(result)
```

运行结果：

```text
60
```

定义函数时不会自动执行函数体。只有写出 `calculate_order_total(...)` 才叫作**调用函数**。

---

## 3. 参数与返回值

参数是函数需要的输入，返回值是函数完成计算后提供的输出。

```python
def calculate_growth_rate(old_value, new_value):
    rate = (new_value - old_value) / old_value * 100
    return rate

growth = calculate_growth_rate(100, 125)
print(growth)
```

运行结果：

```text
25.0
```

`print()` 只是显示数据，`return` 才能让其他代码继续使用结果。

```python
def wrong_total(quantity, price):
    print(quantity * price)

result = wrong_total(2, 10)
print(result)
```

运行结果：

```text
20
None
```

函数没有写 `return` 时，返回值是 `None`。

---

## 4. 默认参数

没有折扣的订单最常见，可以给 `discount` 默认值 `0.0`。

```python
def calculate_order_total(quantity, unit_price, discount=0.0):
    return quantity * unit_price * (1 - discount)

print(calculate_order_total(2, 15))
print(calculate_order_total(3, 20, 0.1))
```

运行结果：

```text
30.0
54.0
```

有默认值的参数必须放在没有默认值的参数之后。

---

## 5. 一次返回多个结果

函数可以返回元组：

```python
def summarize_scores(scores):
    minimum = min(scores)
    maximum = max(scores)
    average = sum(scores) / len(scores)
    return minimum, maximum, average

low, high, mean = summarize_scores([60, 80, 100])
print(low)
print(high)
print(mean)
```

运行结果：

```text
60
100
80.0
```

调用者可以整体接收元组，也可以立即解包。

---

## 6. 局部变量

函数内部创建的变量通常只在函数中存在：

```python
def calculate_total(quantity, price):
    total = quantity * price
    return total

order_total = calculate_total(2, 12.5)
print(order_total)
```

运行结果：

```text
25.0
```

函数外不能直接使用内部的 `total`。这能减少不同计算之间互相覆盖变量的风险。

---

## 7. 函数应完成一件清楚的事

下面的函数只负责生成客户标签：

```python
def format_customer_label(customer_id, city="Unknown"):
    cleaned_id = customer_id.strip()
    cleaned_city = city.strip()
    if cleaned_city == "":
        cleaned_city = "Unknown"
    return f"{cleaned_id} - {cleaned_city}"

print(format_customer_label(" C001 ", " Suzhou "))
print(format_customer_label("C002"))
```

运行结果：

```text
C001 - Suzhou
C002 - Unknown
```

读取文件、清洗所有列、训练模型和保存图片不应全部塞进一个巨大函数。后面的综合项目会把流程拆成多个小函数。

---

## 8. 常见错误

### 错误 1：忘记 `return`

函数虽然打印了正确数字，调用者仍然得到 `None`。需要继续计算或测试的结果必须返回。

### 错误 2：调用时参数顺序错误

`calculate_order_total(20.0, 3)` 会把单价当数量。参数名应表达含义；复杂调用可以使用关键字：`calculate_order_total(quantity=3, unit_price=20.0)`。

### 错误 3：默认参数放错位置

```python
def broken(discount=0.0, quantity):
    return quantity
```

这会产生 `SyntaxError`。没有默认值的参数必须在前。

### 错误 4：没有检查除数

增长率公式的旧值不能为 0，否则会产生 `ZeroDivisionError`。函数契约应说明可接受的输入。

---

## 9. IOM103 对应位置

IOM103 训练脚本没有把整个项目写成一长段，而是拆成 `prepare_churn_data()`、`create_preprocessor()`、`calculate_model_scores()`、`cluster_description()` 等函数。每个函数接收明确输入并返回中间结果。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 3、11 节；
- 原项目只读脚本中的上述函数定义。

---

## 10. 本章练习

打开 `course/python/05_functions/practice.py`：

1. `calculate_order_total`：默认折扣参数；
2. `calculate_growth_rate`：计算百分比变化；
3. `summarize_scores`：一次返回三个统计量；
4. `format_customer_label`：清理参数并返回文本。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""函数、参数与返回值示例。"""

def calculate_order_total(
    quantity: int,
    unit_price: float,
    discount: float = 0.0,
) -> float:
    """返回应用折扣后的订单金额。"""
    return quantity * unit_price * (1 - discount)

def calculate_growth_rate(old_value: float, new_value: float) -> float:
    """返回百分数形式的增长率。"""
    return (new_value - old_value) / old_value * 100

def main() -> None:
    regular_total = calculate_order_total(2, 15.0)
    discounted_total = calculate_order_total(3, 20.0, 0.1)
    growth_rate = calculate_growth_rate(100.0, 125.0)

    print(f"无折扣金额：{regular_total:.2f}")
    print(f"折扣后金额：{discounted_total:.2f}")
    print(f"销售增长率：{growth_rate:.1f}%")

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/05_functions/test.py
```

---

## 11. 本章检查清单

- 我能区分定义函数与调用函数；
- 我能解释参数和返回值；
- 我知道 `print()` 不能代替 `return`；
- 我能设置并使用默认参数；
- 我能用元组返回多个结果；
- 我能把重复公式提取成单一职责函数。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>calculate_order_total</code></summary>

默认参数让调用者在没有折扣时可以省略第三个参数。

</details>

<details>
<summary><code>calculate_growth_rate</code></summary>

函数返回数字，不要在返回值中添加百分号字符串。

</details>

<details>
<summary><code>summarize_scores</code></summary>

min()、max()、sum() 和 len() 可以分别完成所需计算。

</details>

<details>
<summary><code>format_customer_label</code></summary>

先用 strip() 得到清理后的两个变量，再处理空城市。

</details>
