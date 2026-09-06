# 01. 变量与数据类型

## 1. 本章解决什么实际问题

假设你拿到一张订单表，其中一行数据是：

```text
商品名称：Python 入门书
单价："39.90"
数量："2"
是否会员：True
优惠券：None
```

这里的 `"39.90"` 和 `"2"` 看起来像数字，但引号表示它们目前是文本。Python 不能直接用文本完成金额计算。我们需要：

1. 用变量保存每一项数据；
2. 判断数据属于什么类型；
3. 把文本形式的数字转换成真正的数字；
4. 计算订单金额；
5. 把结果整理成容易阅读的一句话。

本章最终要完成的结果类似：

```text
商品：Python 入门书，数量：2，单价：39.90 元，总金额：79.80 元
```

这些操作看起来简单，却是后面读取 CSV、清洗表格和计算统计指标的基础。

---

## 2. 变量是什么

变量可以理解成一个“有名字的数据盒子”。变量名写在等号左边，数据写在等号右边。这个过程叫作**赋值**，也就是把右边的数据交给左边的变量名保存。

```python
student_name = "Lin"
score = 78

print(student_name)
print(score)
```

运行结果：

```text
Lin
78
```

变量保存的数据可以改变。再次给同一个变量赋值，旧值会被新值替换，这叫作**重新赋值**。

```python
score = 78
print(score)

score = 82
print(score)
```

运行结果：

```text
78
82
```

变量名应该说明数据的含义。数据分析代码中，`order_price` 比 `x` 更容易理解。

```python
order_price = 39.90
order_quantity = 2
order_amount = order_price * order_quantity

print(order_amount)
```

运行结果：

```text
79.8
```

---

## 3. Python 常见数据类型

数据类型表示“这个数据是什么，以及可以对它做什么操作”。本章先学习五种常见类型。

### 3.1 `int`：整数

`int` 是 integer（整数）的缩写，适合保存没有小数部分的数字，例如学生人数、商品数量和客户年龄。

```python
student_count = 35
order_quantity = 2
customer_age = 21

print(student_count)
print(order_quantity)
print(customer_age)
```

运行结果：

```text
35
2
21
```

### 3.2 `float`：浮点数

`float` 用来保存带小数的数据，例如成绩、商品单价和客户月消费。

```python
average_score = 82.5
unit_price = 39.90
monthly_spending = 268.75

print(average_score)
print(unit_price)
print(monthly_spending)
```

运行结果：

```text
82.5
39.9
268.75
```

Python 打印 `39.90` 时会显示为 `39.9`。数值没有改变，只是末尾的零没有显示。

### 3.3 `str`：字符串

`str` 是 string（字符串）的缩写，用来保存文本。字符串需要放在单引号或双引号中。

```python
student_id = "S2026001"
product_name = "Python 入门书"
city = "Suzhou"

print(student_id)
print(product_name)
print(city)
```

运行结果：

```text
S2026001
Python 入门书
Suzhou
```

`"100"` 是字符串，`100` 才是整数。它们看起来相似，但能做的操作不同。

### 3.4 `bool`：布尔值

`bool` 是 boolean（布尔值）的缩写，只有 `True` 和 `False` 两个值，适合表示“是或否”。

```python
is_member = True
has_refund = False

print(is_member)
print(has_refund)
```

运行结果：

```text
True
False
```

在客户数据中，`True` 可以表示客户已经流失，`False` 可以表示客户仍然活跃。

### 3.5 `None`：暂时没有数据

`None` 表示“当前没有值”。它不等于数字 `0`，也不等于空字符串 `""`。

```python
coupon_code = None
missing_score = None

print(coupon_code)
print(missing_score)
```

运行结果：

```text
None
None
```

在表格数据中，`None` 常用来表示某个单元格暂时缺少数据。

### 3.6 使用 `type()` 检查类型

`type()` 是 Python 自带的检查工具，它会告诉我们一个值或变量属于什么数据类型。

```python
order_quantity = 2
unit_price = 39.90
product_name = "Python 入门书"
is_member = True
coupon_code = None

print(type(order_quantity))
print(type(unit_price))
print(type(product_name))
print(type(is_member))
print(type(coupon_code))
```

运行结果：

```text
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
<class 'NoneType'>
```

这里的 `class` 暂时可以理解成“类别”。例如 `<class 'float'>` 表示这个数据是浮点数。

---

## 4. 类型转换

类型转换就是把一种类型的数据变成另一种类型。

从 CSV、网页表格或 `input()` 读取数据时，数字经常先以字符串形式进入 Python。例如表格中看到的 `39.90`，读入后可能实际是 `"39.90"`。计算前必须先转换。

### 4.1 使用 `int()` 转成整数

```python
quantity_text = "2"
quantity = int(quantity_text)

print(quantity)
print(type(quantity))
```

运行结果：

```text
2
<class 'int'>
```

字符串两边有空格时，`int()` 也能正常转换：

```python
age_text = " 21 "
age = int(age_text)

print(age)
```

运行结果：

```text
21
```

### 4.2 使用 `float()` 转成浮点数

```python
price_text = "39.90"
price = float(price_text)

print(price)
print(type(price))
```

运行结果：

```text
39.9
<class 'float'>
```

### 4.3 使用 `str()` 转成字符串

```python
student_id_number = 2026001
student_id_text = str(student_id_number)

print(student_id_text)
print(type(student_id_text))
```

运行结果：

```text
2026001
<class 'str'>
```

### 4.4 转换可能失败

只有内容符合数字格式的字符串才能转换。下面的代码会故意报错：

```python
price_text = "39.90元"
price = float(price_text)
```

结果最后会出现：

```text
ValueError: could not convert string to float: '39.90元'
```

`ValueError` 表示“值的内容不符合要求”。`float()` 认识 `"39.90"`，但不认识带有“元”的 `"39.90元"`。一种修改方法是先让数据只保留数字：

```python
price_text = "39.90"
price = float(price_text)

print(price)
```

运行结果：

```text
39.9
```

---

## 5. 使用 f-string 生成结果文本

f-string 是一种把变量放进字符串的写法。在字符串前写字母 `f`，再把变量放进 `{}` 中。

### 例 1：生成成绩信息

```python
student_name = "Lin"
score = 82.5
result = f"学生 {student_name} 的成绩是 {score} 分"

print(result)
```

运行结果：

```text
学生 Lin 的成绩是 82.5 分
```

### 例 2：生成订单摘要

```python
product_name = "Python 入门书"
quantity = 2
unit_price = 39.90
total_amount = quantity * unit_price

summary = (
    f"商品：{product_name}，数量：{quantity}，"
    f"单价：{unit_price:.2f} 元，总金额：{total_amount:.2f} 元"
)

print(summary)
```

运行结果：

```text
商品：Python 入门书，数量：2，单价：39.90 元，总金额：79.80 元
```

`:.2f` 表示把浮点数显示成两位小数。它只控制显示格式，不会把原变量变成字符串。

---

## 6. 常见错误

### 错误 1：字符串和数字直接相加

错误代码：

```python
price_text = "39.90"
delivery_fee = 5
total = price_text + delivery_fee
```

原因：`price_text` 是字符串，`delivery_fee` 是整数。Python 不知道这里要拼接文本还是进行数学加法。

修改方法：

```python
price_text = "39.90"
delivery_fee = 5
total = float(price_text) + delivery_fee

print(total)
```

运行结果：

```text
44.9
```

### 错误 2：字符串无法转换

错误代码：

```python
quantity_text = "two"
quantity = int(quantity_text)
```

原因：`"two"` 不是 Python 能识别的整数格式，因此会出现 `ValueError`。

修改方法：

```python
quantity_text = "2"
quantity = int(quantity_text)

print(quantity)
```

运行结果：

```text
2
```

### 错误 3：变量未定义

错误代码：

```python
print(order_total)
```

如果此前没有给 `order_total` 赋值，Python 会出现 `NameError`。它表示当前找不到这个变量名。

修改方法：

```python
order_total = 79.80
print(order_total)
```

运行结果：

```text
79.8
```

还要注意变量名必须完全一致。`order_total` 和 `order_Total` 是两个不同的名字。

---

## 7. IOM103 对应位置

IOM103 原始客户流失数据中，`tenure` 是整数，`MonthlyCharges` 是浮点数，
`customerID` 和 `Contract` 是字符串，`Churn` 是 Yes/No 文本。
`TotalCharges` 看起来像金额，但原始表中包含空白文本，所以脚本必须先把它转换为
数值。变量、类型和转换正是后续清洗的起点。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 2、3、5 节；
- 原项目只读脚本 `prepare_churn_data()` 中 `TotalCharges` 的转换。

---

## 8. 章节小练习

对应练习文件：

```text
course/python/01_variables_and_types/practice.py
```

练习中会看到函数开头 `def convert_age(age_text: str) -> int:`，下一行还有三引号包住的题目说明。

- `def` 表示“定义一个可以重复使用的任务”，这里的任务名是 `convert_age`；
- `age_text` 是调用函数时传入的数据；
- `: str` 是**类型提示**，说明这里期望收到字符串；
- `-> int` 也是类型提示，说明这个函数应该返回整数；
- 三引号中的文字叫作 **docstring（函数说明）**，用来告诉你题目背景和要求。

类型提示只帮助人阅读代码，不会自动完成转换。真正的转换仍然需要你在函数内部编写。

### 练习 1：转换客户年龄

- 输入：表示年龄的字符串 `age_text`
- 输出：整数年龄
- 示例：输入 `"21"`，输出 `21`
- 特殊情况：`" 0 "` 应输出 `0`；负数或非数字文本应报错

### 练习 2：转换商品价格

- 输入：表示价格的字符串 `price_text`
- 输出：浮点数价格
- 示例：输入 `"39.90"`，输出 `39.9`
- 特殊情况：`"0"` 应输出 `0.0`；负数或带单位的文本应报错

### 练习 3：计算订单金额

- 输入：单价字符串 `unit_price_text` 和数量字符串 `quantity_text`
- 输出：单价乘数量得到的浮点数
- 示例：输入 `"12.50"` 和 `"4"`，输出 `50.0`
- 特殊情况：数量为 `"0"` 时输出 `0.0`；负数或错误格式应报错

### 练习 4：生成订单摘要

- 输入：商品名、数量字符串和单价字符串
- 输出：包含商品、数量、单价和总金额的文本
- 示例：输入 `"Notebook"`、`"2"`、`"12.50"`，输出  
  `商品：Notebook，数量：2，单价：12.50 元，总金额：25.00 元`
- 特殊情况：数量为 `"0"` 时，总金额显示为 `0.00 元`

练习文件中的 `TODO` 表示需要你填写的位置。`NotImplementedError` 表示这道题目前故意没有实现；写完代码后应删除或替换这一行。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""变量、数据类型、类型转换与 f-string 演示。"""


def demo_type_conversion() -> None:
    """演示字符串与数字之间的类型转换。"""
    count_text = "12"
    price_text = "3.5"
    count = int(count_text)
    price = float(price_text)
    print("数量翻倍：", count * 2)
    print("价格类型：", type(price).__name__)
    print(f"小计：{count * price:.2f}")


def main() -> None:
    demo_type_conversion()
    is_registered = False
    remark = None
    print("布尔类型：", type(is_registered).__name__)
    print("空值类型：", type(remark).__name__)


if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/01_variables_and_types/test.py
```

第一次运行时出现 `XFAIL`，表示练习仍未完成。`pytest` 是自动检查练习结果的工具；你暂时不需要理解它的内部原理。

---

## 9. 本章检查清单

完成练习后，请逐项确认：

- [ ] 看到 `"25"` 时，我能判断它是字符串，而不是整数。
- [ ] 我能用变量保存客户年龄、商品价格和订单数量。
- [ ] 我能解释 `int`、`float`、`str`、`bool` 和 `None` 分别适合保存什么数据。
- [ ] 我能用 `type()` 检查一个变量的类型。
- [ ] 我能把 `"21"` 转成整数 `21`。
- [ ] 我能把 `"39.90"` 转成浮点数 `39.9`。
- [ ] 我知道 `"39.90元"` 为什么不能直接传给 `float()`。
- [ ] 我能先转换单价和数量，再计算订单总金额。
- [ ] 我能用 f-string 生成包含变量的成绩或订单文本。
- [ ] 我能读懂变量未定义、错误类型相加和转换失败的原因。
- [ ] 运行第一章测试后，四道练习不再显示 `XFAIL`。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>convert_age</code></summary>

先使用 int() 完成类型转换，再判断结果是否小于 0。

</details>

<details>
<summary><code>convert_price</code></summary>

使用 float() 转换，再检查得到的价格是否小于 0。

</details>

<details>
<summary><code>calculate_order_amount</code></summary>

分别使用 float() 和 int()，不要直接把两个字符串相乘。

</details>

<details>
<summary><code>build_order_summary</code></summary>

f-string 中的 {value:.2f} 可以把浮点数显示成两位小数。

</details>
