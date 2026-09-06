# 02. 列表、元组、集合与切片

## 1. 本章解决什么实际问题

一张订单表有很多列。在正式使用 Pandas 前，我们先用 Python 自带的数据结构表示几种常见数据：

- 一位客户最近浏览过的商品：数量会变化，而且有先后顺序；
- 一条订单的商品、数量、单价：位置固定，不希望随意改变；
- 两个营销名单中的客户编号：只关心是否出现，以及哪些客户重复出现。

对应的数据结构分别是列表、元组和集合。本章完成后，你可以从一组客户或订单数据中截取需要的部分、去重，以及求两个名单的交集。

---

## 2. 列表：有顺序、可以修改

列表使用方括号 `[]`。列表中的每个位置都有一个索引，索引从 `0` 开始。

```python
products = ["Pen", "Notebook", "Mouse"]

print(products[0])
print(products[1])
print(len(products))
```

运行结果：

```text
Pen
Notebook
3
```

列表是**可变的**，意思是创建后仍可以增加、删除或替换数据。

```python
products = ["Pen", "Notebook"]
products.append("Mouse")
products[0] = "Pencil"

print(products)
```

运行结果：

```text
['Pencil', 'Notebook', 'Mouse']
```

### 2.1 切片

切片用于取得列表中的一段数据。`products[start:stop]` 包含 `start`，但不包含 `stop`，这叫作“左闭右开”。

```python
products = ["Pen", "Notebook", "Mouse", "Keyboard"]

print(products[1:3])
print(products[:2])
print(products[2:])
print(products[-2:])
```

运行结果：

```text
['Notebook', 'Mouse']
['Pen', 'Notebook']
['Mouse', 'Keyboard']
['Mouse', 'Keyboard']
```

切片会创建新列表，不会删除原列表中的数据。

---

## 3. 元组：有顺序、不能修改

元组使用圆括号 `()`。它与列表一样有顺序，但创建后不能替换其中的元素。固定结构的一条记录适合使用元组。

```python
order = ("Notebook", 2, 12.5)

print(order[0])
print(order[1])
print(order[2])
```

运行结果：

```text
Notebook
2
12.5
```

可以一次把元组中的值交给多个变量，这叫作**解包**。

```python
order = ("Notebook", 2, 12.5)
product, quantity, unit_price = order

print(product)
print(quantity * unit_price)
```

运行结果：

```text
Notebook
25.0
```

左边变量的数量必须与元组元素数量相同。

---

## 4. 集合：不重复、没有固定顺序

集合使用花括号 `{}` 或 `set()` 创建。集合自动去掉重复值，适合保存“不重复的客户编号或类别”。

```python
cities = ["Suzhou", "Shanghai", "Suzhou", "Nanjing"]
unique_cities = set(cities)

print(len(unique_cities))
print("Suzhou" in unique_cities)
print(sorted(unique_cities))
```

运行结果：

```text
3
True
['Nanjing', 'Shanghai', 'Suzhou']
```

集合本身没有固定显示顺序。需要稳定输出时，可以先用 `sorted()` 排序。

两个集合共有的元素叫作**交集**：

```python
high_spending = {"C001", "C002", "C004"}
high_satisfaction = {"C002", "C003", "C004"}
both = high_spending & high_satisfaction

print(sorted(both))
```

运行结果：

```text
['C002', 'C004']
```

---

## 5. 一次串联三种结构

```python
recent_products = ["Pen", "Book", "Pen", "Mouse"]
selected = recent_products[1:]
unique_selected = set(selected)
order = ("Book", 2, 15.0)
product, quantity, price = order

print(sorted(unique_selected))
print(f"{product} 总金额：{quantity * price:.2f}")
```

运行结果：

```text
['Book', 'Mouse', 'Pen']
Book 总金额：30.00
```

数据流是：列表保存原始顺序 → 切片选择一段 → 集合去重 → 元组保存固定订单。

---

## 6. 常见错误

### 错误 1：索引超过列表范围

```python
products = ["Pen", "Book"]
print(products[2])
```

列表只有索引 `0` 和 `1`，访问 `2` 会产生 `IndexError`。先用 `len(products)` 查看长度，或使用不会因右边界过大而失败的切片。

### 错误 2：尝试修改元组

```python
order = ("Pen", 2)
order[1] = 3
```

元组不能修改，会产生 `TypeError`。如果数据确实需要频繁改变，应改用列表。

### 错误 3：依赖集合顺序

不要认为集合中“第一个元素”永远相同。集合不支持按索引读取；展示结果时使用 `sorted()`。

### 错误 4：用 `{}` 创建空集合

`{}` 创建的是空字典。空集合必须写成：

```python
empty_customers = set()
print(type(empty_customers))
```

运行结果：

```text
<class 'set'>
```

---

## 7. IOM103 对应位置

IOM103 训练脚本使用列表保存数值特征和类别特征，使用候选 `k` 值循环评估客户分群。固定的模型名称与模型对象也需要成组组织。现在不必理解模型，只需看懂这些数据为什么需要“有顺序的集合”。

对应阅读：

- 根目录 [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 的第 5、8 节；
- 原项目只读脚本 `create_preprocessor()`、`task_a2_churn_prediction()` 和 `task_b_customer_segmentation()`。

---

## 8. 本章练习

打开 `course/python/02_lists_tuples_sets/practice.py`：

1. `unique_recent_items`：切片后去重；
2. `calculate_average_score`：用列表计算平均分；
3. `unpack_order`：解包固定订单元组；
4. `find_common_customers`：求两个客户集合的交集。

先只阅读 docstring，再逐个替换 TODO。不要查看答案文件直到自己至少尝试一次。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""列表、元组、集合与切片示例。"""

def unique_recent_products(products: list[str], start: int) -> set[str]:
    """返回指定位置之后出现过的不同商品。"""
    return set(products[start:])

def main() -> None:
    products = ["Pen", "Notebook", "Pen", "Mouse"]
    order = ("Notebook", 2, 12.5)
    recent_products = unique_recent_products(products, 1)

    print("切片：", products[1:3])
    print("订单元组：", order)
    print("不同商品：", sorted(recent_products))
    print("共同客户：", sorted({"C1", "C2"} & {"C2", "C3"}))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/02_lists_tuples_sets/test.py
```

---

## 9. 本章检查清单

- 我能说出列表与元组最重要的区别；
- 我知道索引从 `0` 开始；
- 我能解释为什么切片 `1:3` 不包含索引 `3`；
- 我能用集合去重和求交集；
- 我不会依赖集合的显示顺序；
- 我能根据“是否需要修改、是否要求顺序、是否允许重复”选择数据结构。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>unique_recent_items</code></summary>

先写 items[start:]，再使用 set()。

</details>

<details>
<summary><code>calculate_average_score</code></summary>

先判断列表长度，再计算 sum(scores) / len(scores)。

</details>

<details>
<summary><code>unpack_order</code></summary>

可以写 product, quantity, price = order。

</details>

<details>
<summary><code>find_common_customers</code></summary>

集合的 & 运算或 intersection() 都可以求交集。

</details>
