# 03. 字典：用字段名组织一条数据

## 1. 本章解决什么实际问题

列表可以保存一行客户数据：

```python
customer = ["C001", "Suzhou", 188.5]
```

但只看这一行，很难知道三个位置分别表示什么。如果使用字典：

```python
customer = {
    "customer_id": "C001",
    "city": "Suzhou",
    "monthly_spending": 188.5,
}
```

字段名和数据放在一起，更接近 CSV 表头与一行数据的关系。本章将使用字典表示客户记录、读取字段、修改字段，并统计类别次数。

---

## 2. 键和值

字典保存“键 → 值”的对应关系。键通常是字段名，值是实际数据。

```python
customer = {
    "customer_id": "C001",
    "city": "Suzhou",
    "monthly_spending": 188.5,
}

print(customer["customer_id"])
print(customer["monthly_spending"])
```

运行结果：

```text
C001
188.5
```

同一个字典的值可以属于不同类型。字段名必须唯一；重复写同一个键时，后面的值会覆盖前面的值。

---

## 3. 添加、修改和删除字段

字典是可变的，可以通过键添加或修改数据。

```python
customer = {"customer_id": "C001", "city": "Suzhou"}
customer["monthly_spending"] = 188.5
customer["city"] = "Shanghai"

print(customer)
```

运行结果：

```text
{'customer_id': 'C001', 'city': 'Shanghai', 'monthly_spending': 188.5}
```

删除字段可以使用 `del`：

```python
customer = {"customer_id": "C001", "temporary_note": "check"}
del customer["temporary_note"]

print(customer)
```

运行结果：

```text
{'customer_id': 'C001'}
```

---

## 4. `[]` 与 `get()` 的区别

如果字段必须存在，使用方括号。字段不存在时会产生 `KeyError`，帮助我们尽早发现数据结构错误。

```python
customer = {"customer_id": "C001"}
print(customer["customer_id"])
```

运行结果：

```text
C001
```

如果字段允许缺失，可以使用 `get()` 并提供默认值：

```python
customer = {"customer_id": "C001"}

print(customer.get("city"))
print(customer.get("city", "Unknown"))
```

运行结果：

```text
None
Unknown
```

不要对所有字段都使用默认值。`customer_id` 缺失通常代表数据有问题，应让错误暴露出来。

---

## 5. 遍历字典

`keys()` 返回键，`values()` 返回值，`items()` 同时返回键和值。

```python
sales = {"Pen": 30.0, "Book": 80.0}

for product, amount in sales.items():
    print(f"{product}: {amount:.2f}")
```

运行结果：

```text
Pen: 30.00
Book: 80.00
```

---

## 6. 用字典统计类别

合同类型列表中同一类别会重复出现。字典可以保存每个类别的计数。

```python
contracts = ["Monthly", "Yearly", "Monthly", "Two-year", "Monthly"]
counts = {}

for contract in contracts:
    counts[contract] = counts.get(contract, 0) + 1

print(counts)
```

运行结果：

```text
{'Monthly': 3, 'Yearly': 1, 'Two-year': 1}
```

第一次遇到 `"Monthly"` 时，`get("Monthly", 0)` 返回 `0`；之后每次都在已有计数上加一。

---

## 7. 合并两个按商品汇总的字典

```python
january = {"Pen": 10.0, "Book": 20.0}
february = {"Pen": 5.0, "Mouse": 30.0}
totals = january.copy()

for product, amount in february.items():
    totals[product] = totals.get(product, 0) + amount

print(totals)
print(january)
```

运行结果：

```text
{'Pen': 15.0, 'Book': 20.0, 'Mouse': 30.0}
{'Pen': 10.0, 'Book': 20.0}
```

先使用 `copy()`，因此合并过程不会修改一月原始数据。

---

## 8. 常见错误

### 错误 1：访问不存在的必需字段

```python
customer = {"city": "Suzhou"}
print(customer["customer_id"])
```

会产生 `KeyError`。如果字段确实必须存在，应回到数据来源修正；如果字段本来允许缺失，再考虑 `get()`。

### 错误 2：把键和值写反

正确形式是 `"字段名": 数据`，不是 `数据: "字段名"`。字段名应稳定，数据值可以变化。

### 错误 3：遍历字典时直接修改大小

在 `for key in dictionary` 中删除键可能产生错误。需要删除多个字段时，先把要删除的键整理到另一个列表。

### 错误 4：合并时覆盖而不是累加

`totals.update(february)` 会让二月的 `"Pen"` 覆盖一月金额。如果业务目标是合计，必须显式相加。

---

## 9. IOM103 对应位置

IOM103 Task A2 使用模型名称对应模型对象，并把每个模型的 accuracy、recall、F1 和 AUROC 组织成记录，最后形成比较表。字典正是“有名称的字段和值”的基础。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 3、8 节；
- 原项目只读脚本中的 `calculate_model_scores()` 与 `task_a2_churn_prediction()`。

---

## 10. 本章练习

打开 `course/python/03_dictionaries/practice.py`：

1. `count_categories`：统计类别次数；
2. `build_customer_record`：创建客户字典；
3. `get_required_value`：读取必需字段；
4. `merge_monthly_sales`：合并两个月销售额。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""使用字典表示记录并统计类别示例。"""

def count_contracts(contracts: list[str]) -> dict[str, int]:
    """统计每种合同类型的客户数。"""
    counts: dict[str, int] = {}
    for contract in contracts:
        counts[contract] = counts.get(contract, 0) + 1
    return counts

def main() -> None:
    customer = {
        "customer_id": "C001",
        "city": "Suzhou",
        "monthly_spending": 188.5,
    }
    contracts = ["Monthly", "Yearly", "Monthly", "Two-year"]

    print("客户编号：", customer["customer_id"])
    print("城市：", customer.get("city"))
    print("合同统计：", count_contracts(contracts))
    print("字段：", list(customer.keys()))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/03_dictionaries/test.py
```

---

## 11. 本章检查清单

- 我能解释键和值分别代表什么；
- 我能创建、读取、修改字典字段；
- 我知道 `record[key]` 与 `record.get(key)` 的区别；
- 我能用 `items()` 同时遍历键和值；
- 我能用字典完成类别计数；
- 我知道什么时候应复制字典，避免修改原始数据。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>count_categories</code></summary>

dictionary.get(value, 0) 可以提供初始计数 0。

</details>

<details>
<summary><code>build_customer_record</code></summary>

字典字面量写成 {"key": value}。

</details>

<details>
<summary><code>get_required_value</code></summary>

record[key] 与 record.get(key) 在字段缺失时行为不同。

</details>

<details>
<summary><code>merge_monthly_sales</code></summary>

可以先复制 january，再遍历 february 并使用 get() 累加。

</details>
