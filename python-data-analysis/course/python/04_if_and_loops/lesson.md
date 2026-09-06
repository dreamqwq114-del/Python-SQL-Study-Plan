# 04. 条件判断与循环：让分析规则重复执行

## 1. 本章解决什么实际问题

假设业务部门给出客户消费分组规则：

- 月消费小于 100：低消费；
- 100 到 499.99：中消费；
- 500 及以上：高消费。

只有一位客户时，可以判断一次；有几千位客户时，就需要把判断放进循环。本章学习如何使用 `if` 表达业务规则，使用 `for` 对多条数据重复执行规则。

---

## 2. 布尔表达式

比较运算会得到 `True` 或 `False`：

```python
amount = 120

print(amount < 100)
print(amount >= 100)
print(amount == 120)
print(amount != 120)
```

运行结果：

```text
False
True
True
False
```

注意：`=` 是赋值，`==` 才是判断两个值是否相等。

---

## 3. `if`、`elif` 和 `else`

```python
amount = 220

if amount < 100:
    level = "low"
elif amount < 500:
    level = "medium"
else:
    level = "high"

print(level)
```

运行结果：

```text
medium
```

Python 从上往下检查条件，遇到第一个为 `True` 的分支后就不再检查后续分支。

### 3.1 边界为什么重要

当 `amount` 等于 `100` 时，第一个条件 `amount < 100` 是 False，因此进入 `medium`。当金额等于 `500` 时，第二个条件也不成立，因此进入 `high`。

```python
for amount in [99, 100, 499.99, 500]:
    if amount < 100:
        level = "low"
    elif amount < 500:
        level = "medium"
    else:
        level = "high"
    print(amount, level)
```

运行结果：

```text
99 low
100 medium
499.99 medium
500 high
```

---

## 4. 使用 `for` 循环多条数据

```python
statuses = ["Yes", "No", "Yes", "No"]
churned_count = 0

for status in statuses:
    if status == "Yes":
        churned_count += 1

print(churned_count)
```

运行结果：

```text
2
```

`status` 每轮取得列表中的一个值。`+= 1` 等价于 `churned_count = churned_count + 1`。

---

## 5. 跳过缺失值

`continue` 表示立即结束本轮循环，进入下一轮。

```python
scores = [4, None, 2, 5]
total = 0
count = 0

for score in scores:
    if score is None:
        continue
    total += score
    count += 1

print(total / count)
```

运行结果：

```text
3.6666666666666665
```

不能把 `None` 与数字相加，所以先跳过缺失值。

---

## 6. 找到结果后提前结束

`enumerate()` 同时提供索引和值。找到第一笔大额订单后，可以使用 `break` 或直接 `return`。

```python
amounts = [20, 150, 80, 600]
threshold = 100
found_index = None

for index, amount in enumerate(amounts):
    if amount > threshold:
        found_index = index
        break

print(found_index)
```

运行结果：

```text
1
```

---

## 7. 组合条件

`and` 要求两个条件都成立，`or` 要求至少一个成立，`not` 表示取反。

```python
age = 35
spending = 520

is_target_customer = age >= 30 and spending >= 500
print(is_target_customer)
```

运行结果：

```text
True
```

复杂条件应拆成有含义的变量，避免一行写太多比较。

---

## 8. 常见错误

### 错误 1：缩进不一致

属于 `if` 或 `for` 的代码必须使用一致缩进，项目统一使用 4 个空格。

### 错误 2：边界重复或遗漏

不要写 `amount <= 100` 后又写 `amount >= 100`，这样 `100` 同时满足两个描述。先明确每个边界归属，再写条件。

### 错误 3：循环中忘记更新计数

只判断 `status == "Yes"` 而没有 `count += 1`，最终计数永远是 0。

### 错误 4：把 `None` 当成 0

缺失值和真实的 0 含义不同。只有业务明确要求时，才能用 0 替代缺失。

---

## 9. IOM103 对应位置

IOM103 Task A2 使用循环对 Logistic Regression、Decision Tree 和 Random Forest 执行相同的训练与评估；Task B 使用循环计算 `k=2..10` 的 inertia 和 silhouette score。循环让同一流程应用于不同候选模型或参数。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 3、8 节；
- 原项目只读脚本 `task_a2_churn_prediction()` 和 `task_b_customer_segmentation()`。

---

## 10. 本章练习

打开 `course/python/04_if_and_loops/practice.py`：

1. `classify_spending`：实现三个金额区间；
2. `count_churned`：循环验证并统计状态；
3. `calculate_valid_average`：跳过缺失值；
4. `find_first_large_order`：查找第一个超过阈值的位置。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""条件判断与循环的基础演示。"""


def demo_letter_grade(score: float) -> str:
    """把考试分数换算成等级，仅演示 if/elif/else 的判断顺序。"""
    if score >= 90:
        return "A"
    if score >= 60:
        return "B"
    return "C"


def main() -> None:
    for score in [55, 72, 96]:
        print(f"{score} 分 -> {demo_letter_grade(score)}")

    total = 0
    for number in range(1, 6):
        total += number
    print("1 到 5 求和：", total)


if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/04_if_and_loops/test.py
```

---

## 11. 本章检查清单

- 我知道 `=` 与 `==` 的区别；
- 我能根据明确边界写 `if/elif/else`；
- 我能逐步判断 99、100、500 分别进入哪个分支；
- 我能用 `for` 遍历列表并累计结果；
- 我知道何时使用 `continue` 和 `break`；
- 我能处理空列表和全部缺失的情况。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>classify_spending</code></summary>

先处理错误输入，再按从小到大的边界写 if/elif/else。

</details>

<details>
<summary><code>count_churned</code></summary>

循环中可以先验证当前值，再使用 if 判断是否需要计数。

</details>

<details>
<summary><code>calculate_valid_average</code></summary>

同时维护 total 和 count，只有值不是 None 时才更新它们。

</details>

<details>
<summary><code>find_first_large_order</code></summary>

enumerate() 能同时得到索引和金额，找到后可以立即 return。

</details>
