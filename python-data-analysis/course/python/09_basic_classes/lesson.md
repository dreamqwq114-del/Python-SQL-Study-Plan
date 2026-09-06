# 09. 基础类：把数据和相关操作放在一起

## 1. 本章解决什么实际问题

客户名称与月消费总是一起出现，年消费和客户描述也依赖这两个值。可以继续使用字典和独立函数，但当“数据”和“使用这些数据的操作”关系稳定时，可以定义类：

```text
Customer
├── name
├── monthly_spending
├── annual_spending()
└── describe()
```

**类**是创建对象的规则，**对象**是根据类创建的一份具体数据。本章只学习理解 scikit-learn 所需的基础类概念，不深入继承等高级内容。

---

## 2. 定义类和创建对象

```python
class Customer:
    def __init__(self, name, monthly_spending):
        self.name = name
        self.monthly_spending = monthly_spending

customer = Customer("Alice", 188.5)

print(customer.name)
print(customer.monthly_spending)
```

运行结果：

```text
Alice
188.5
```

- `Customer(...)` 创建对象；
- `__init__` 在创建时设置初始状态；
- `self` 代表当前这个对象；
- `self.name` 是对象的属性。

---

## 3. 给类添加方法

定义在类中的函数叫作**方法**。

```python
class Customer:
    def __init__(self, name, monthly_spending):
        self.name = name
        self.monthly_spending = monthly_spending

    def annual_spending(self):
        return self.monthly_spending * 12

    def describe(self):
        return f"{self.name}: {self.monthly_spending:.2f}"

customer = Customer("Alice", 188.5)
print(customer.describe())
print(customer.annual_spending())
```

运行结果：

```text
Alice: 188.50
2262.0
```

调用方法时写 `customer.describe()`，Python 会自动把 `customer` 作为 `self`。

---

## 4. 在构造时验证数据

```python
class Order:
    def __init__(self, product_name, quantity, unit_price):
        if product_name == "":
            raise ValueError("商品名不能为空")
        if quantity < 0 or unit_price < 0:
            raise ValueError("数量和单价不能小于 0")
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    def total(self):
        return self.quantity * self.unit_price

order = Order("Book", 2, 12.0)
print(order.total())
```

运行结果：

```text
24.0
```

构造时验证后，对象内部就不会保存明显无效的负数量。

---

## 5. 一个类可以创建多个对象

```python
class Customer:
    def __init__(self, name, spending):
        self.name = name
        self.spending = spending

first = Customer("Alice", 100)
second = Customer("Bob", 250)

print(first.name, first.spending)
print(second.name, second.spending)
```

运行结果：

```text
Alice 100
Bob 250
```

两个对象拥有独立状态，修改 `first` 不会自动改变 `second`。

---

## 6. 从多行数据创建对象

```python
class Customer:
    def __init__(self, name, spending):
        self.name = name
        self.spending = spending

rows = [("Alice", 100), ("Bob", 250)]
customers = []

for name, spending in rows:
    customers.append(Customer(name, spending))

print(customers[0].name)
print(customers[1].name)
```

运行结果：

```text
Alice
Bob
```

这展示了表格行如何转换为对象。Pandas 分析通常仍以 DataFrame 为主，不需要把每一行都变成类。

---

## 7. 为什么这对 scikit-learn 有用

后面会看到：

```python
model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

`LogisticRegression` 是类，`model` 是对象；`fit()` 和 `predict()` 是方法。`fit()` 后模型对象会保存从训练数据学到的状态。

你不需要自己实现模型类，但需要看懂“创建对象 → 调用方法 → 对象状态改变”。

---

## 8. 常见错误

### 错误 1：忘记 `self`

类中实例方法的第一个参数必须是 `self`，访问属性也要写 `self.name`。

### 错误 2：只创建类，没有创建对象

`Customer.describe()` 缺少具体客户状态。应先 `customer = Customer(...)`，再调用 `customer.describe()`。

### 错误 3：方法名后忘记括号

`customer.describe` 是方法本身，`customer.describe()` 才会执行并得到字符串。

### 错误 4：保存外部可变列表引用

对象需要独立保存成绩时，使用 `list(scores)` 创建副本，避免外部 `append()` 意外改变对象。

---

## 9. IOM103 对应位置

IOM103 中的编码器、缩放器、分类模型和 KMeans 都是对象；Pipeline 是把多个处理步骤按顺序连接起来的“管道对象”。脚本先创建对象，再调用 `fit()`、`transform()`、`predict()` 或 `predict_proba()`。本章的 Customer 很简单，但对象使用方式相同。

对应阅读：

- [ORIGINAL_PROJECT_ANALYSIS.md](../../../ORIGINAL_PROJECT_ANALYSIS.md) 第 8、11 节；
- 原项目只读脚本中的 `Pipeline(...)`、模型构造和 `.fit()` 调用。

---

## 10. 本章练习

打开 `course/python/09_basic_classes/practice.py`：

1. `Customer`：客户属性、年消费和描述；
2. `Order`：订单属性、总金额和描述；
3. `ScoreSummary`：保存成绩副本并计算统计量；
4. `build_customers`：把多行元组转换为对象。
### 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""使用基础类封装客户数据和行为示例。"""

class Customer:
    """保存客户名称和月消费。"""

    def __init__(self, name: str, monthly_spending: float) -> None:
        self.name = name
        self.monthly_spending = monthly_spending

    def annual_spending(self) -> float:
        """返回十二个月的消费金额。"""
        return self.monthly_spending * 12

    def describe(self) -> str:
        """返回客户摘要。"""
        return f"{self.name}: {self.monthly_spending:.2f}"

def main() -> None:
    customers = [
        Customer("Alice", 188.5),
        Customer("Bob", 250.0),
    ]

    for customer in customers:
        print(customer.describe())
        print(f"年消费：{customer.annual_spending():.2f}")

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/python/09_basic_classes/test.py
```

---

## 11. 本章检查清单

- 我能区分类与对象；
- 我知道 `__init__` 负责建立初始状态；
- 我能解释 `self` 表示当前对象；
- 我能创建对象、读取属性和调用方法；
- 我知道方法名后需要括号才会执行；
- 我能看懂 scikit-learn 的“创建模型 → fit → predict”对象流程。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>build_customers</code></summary>

在循环中调用 Customer(name, spending)，再 append 到结果列表。

</details>
