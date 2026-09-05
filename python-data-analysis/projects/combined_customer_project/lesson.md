# 综合项目：从两张 CSV 到客户流失模型

## 项目要解决的实际问题

现在你拿到两份数据：

- `sample_customers.csv`：每位客户的年龄、城市、月消费、合同类型、流失状态等。
- `sample_orders.csv`：每笔订单的客户、数量、单价和订单状态。

业务方提出三个问题：

1. 每个城市的客户平均月消费是多少？
2. 每位客户完成了多少订单、累计消费多少？
3. 能否根据客户属性和订单行为预测客户是否会流失？

这不是一道只考某个函数的题。你要把前面课程中的路径、Pandas 清洗与合并、Matplotlib 绘图、scikit-learn 分类串成一条可重复运行的数据分析流程。

## 最终数据流

```text
客户 CSV -> 读取 -> 客户清洗 ----------------------┐
                                                  ├-> 左连接 -> 分析表
订单 CSV -> 读取 -> 筛选已完成订单 -> 每客户汇总 --┘
                                                        |
                                     ┌------------------┴------------------┐
                                     v                                     v
                              保存客户分析图                       训练流失分类管道
```

每个箭头都对应一个明确函数。这样出错时可以单独检查某一步，而不是在一段很长的脚本中寻找问题。

## 输入数据先做体检

从项目根目录运行：

```python
import pandas as pd

customers = pd.read_csv("data/sample_customers.csv")
orders = pd.read_csv("data/sample_orders.csv")

print(customers.shape)
print(orders.shape)
print(customers["customer_id"].nunique())
```

预期输出：

```text
(31, 9)
(45, 7)
30
```

客户表有 31 行，却只有 30 个不同客户编号，说明至少有重复记录。行数与客户数不是同一个概念，分析前必须检查。

## 第一步：只负责读取

`load_datasets(customer_path, order_path)` 的职责只有读取和返回两张表，不在这里清洗。分开职责有两个好处：

- 路径错误可以单独发现。
- 清洗函数可以直接接收测试构造的小表，不必每次创建文件。

`Path` 是表示文件路径的对象。项目使用相对路径，不写死用户名和盘符：

```python
from utils.paths import DATA_DIR

customer_path = DATA_DIR / "sample_customers.csv"
order_path = DATA_DIR / "sample_orders.csv"

print(customer_path.name)
print(order_path.name)
```

预期输出：

```text
sample_customers.csv
sample_orders.csv
```

路径不存在时应让 `FileNotFoundError` 暴露出来，不能悄悄创建一张空表，因为空表会让后面的错误更难理解。

## 第二步：清洗客户表

`clean_customers(customers)` 要处理五类质量问题。

### 1. 重复客户

先把 `customer_id` 转成字符串并去除首尾空格，拒绝缺失或空编号，再按规范化后的编号只保留第一条记录并重置行索引。否则 `" C001 "` 和 `"C001"` 会被误认为两个客户，后续一对一连接可能失败。这里保留第一条是项目数据契约的一部分；真实项目还应调查重复记录是否有时间先后。

```python
import pandas as pd

data = pd.DataFrame(
    {
        "customer_id": ["C001", "C001", "C002"],
        "age": [23, 23, 41],
    }
)
cleaned = data.drop_duplicates(
    subset="customer_id",
    keep="first",
).reset_index(drop=True)

print(cleaned["customer_id"].tolist())
print(cleaned.index.tolist())
```

预期输出：

```text
['C001', 'C002']
[0, 1]
```

### 2. 类别文本不统一

`" suzhou "`、`"Suzhou"` 和 `"SUZHOU"` 表示同一城市。清洗规则是：

- `gender`：去空格并转小写。
- `city`：去空格并使用首字母大写形式。
- `contract_type`：去空格并转小写。

```python
import pandas as pd

city = pd.Series([" suzhou ", "NANJING"])
normalized = city.astype("string").str.strip().str.title()
print(normalized.tolist())
```

预期输出：

```text
['Suzhou', 'Nanjing']
```

### 3. 数字可能是文本

`monthly_spending` 中有 `"unknown"`。`pd.to_numeric(errors="coerce")` 把无法转换的内容变成缺失值 `NaN`。清洗函数先保留这个缺失值，不在全体客户上计算填充值；训练分类器时，再只根据训练集学习中位数。

```python
import pandas as pd

values = pd.Series(["100", "unknown", "300"])
numeric = pd.to_numeric(values, errors="coerce")

print(numeric.dropna().tolist())
print(int(numeric.isna().sum()))
```

预期输出：

```text
[100.0, 300.0]
1
```

如果整列都无法转换，函数必须抛出 `ValueError`，提醒使用者检查数据，而不是继续训练。

**中位数（median）**是排序后位于中间的数，比平均数更不容易被极端值拉动。它会在后面的数值处理管道中由训练集计算，再用于训练集和测试集，避免测试信息提前进入模型。

### 4. 日期格式混合

日期列同时出现 `2025-01-12`、`2024/03/18`、`18-04-2024` 和坏日期。使用 `format="mixed"` 逐项识别格式，`errors="coerce"` 把不可能日期变成 `NaT`。

`NaT` 是 Pandas 对缺失时间的表示，类似数值列的 `NaN`。

```python
import pandas as pd

dates = pd.Series(["2025-01-12", "18-04-2024", "bad-date"])
parsed = pd.to_datetime(
    dates,
    format="mixed",
    errors="coerce",
    dayfirst=True,
)

print(parsed.dt.year.fillna(0).astype(int).tolist())
print(int(parsed.isna().sum()))
```

预期输出：

```text
[2025, 2024, 0]
1
```

### 5. 标签转成 0/1

`churn` 是模型要预测的标签。本项目规定 `No -> 0`、`Yes -> 1`。映射后必须检查缺失，避免 `"Maybe"` 被悄悄变成空值。

## 第三步：把订单汇总到客户级

客户表是一位客户一行，订单表是一笔订单一行。直接连接会让有多笔订单的客户重复，所以要先汇总。

本项目只把 `Completed` 视为已完成订单；`Cancelled` 和 `Returned` 不计入消费统计。订单金额为：

```text
order_total = quantity * unit_price
```

```python
import pandas as pd

orders = pd.DataFrame(
    {
        "customer_id": ["C001", "C001", "C002"],
        "order_id": ["O1", "O2", "O3"],
        "order_total": [20.0, 30.0, 99.0],
    }
)
summary = orders.groupby("customer_id").agg(
    order_count=("order_id", "nunique"),
    total_order_spending=("order_total", "sum"),
    average_order_value=("order_total", "mean"),
)

print(summary.loc["C001"].tolist())
```

预期输出：

```text
[2.0, 50.0, 25.0]
```

数量必须是非负整数，单价不能为负；缺失或无穷数值也必须尽早抛出 `ValueError`。不要把未知单价悄悄汇总成零消费，也不要生成没有业务意义的负消费。

## 第四步：左连接保留所有客户

**左连接（left join）**保留左表的全部客户，再把右表中匹配的订单统计接过来。没有已完成订单的客户也有分析价值，因此订单统计填 0。

```python
import pandas as pd

customers = pd.DataFrame({"customer_id": ["C001", "C002"]})
summary = pd.DataFrame(
    {
        "customer_id": ["C001"],
        "order_count": [2],
    }
)
merged = customers.merge(summary, on="customer_id", how="left")
merged["order_count"] = merged["order_count"].fillna(0).astype(int)

print(merged["order_count"].tolist())
```

预期输出：

```text
[2, 0]
```

`validate="one_to_one"` 是连接安全检查：两张表都应每个客户一行。如果出现重复客户，让 Pandas 立即报错，避免行数悄悄膨胀。

## 第五步：保存客户分析图

图中包含：

1. 各城市平均月消费柱状图。
2. 未流失与流失客户人数柱状图。

绘图函数必须：

- 自动创建输出父目录。
- 使用 `figure.savefig(...)` 保存。
- 不调用 `plt.show()`。
- 在 `finally` 中 `plt.close(figure)`，即使保存失败也不遗留 Figure。

这使函数能在 PyCharm、终端和 pytest 中稳定运行。

## 第六步：建立无泄漏分类管道

模型输入包括：

- 数值特征：年龄、月消费、满意度、订单数、累计订单消费、平均订单金额。
- 分类特征：性别、城市、合同类型。
- 标签：`churn`。

三个新对象的职责是：

- `SimpleImputer` 是**缺失值填补器**：数值流程从训练列学习中位数，分类流程从训练列学习众数，再用同一规则处理验证或测试数据。
- `ColumnTransformer` 是**列转换器**：把数值列和分类列送进不同处理流程，再把转换结果横向合并。
- `Pipeline` 是**管道**：把预处理与模型按顺序连接成一个可统一 `fit`、`predict` 的对象。

训练流程：

1. 先按 75%/25% 分层划分。
2. 数值管道在训练集上学习中位数和标准化参数。
3. 分类管道在训练集上学习众数和独热编码类别。
4. `ColumnTransformer` 把两条管道应用到不同列。
5. `Pipeline` 连接预处理与逻辑回归。
6. 只在 `X_train, y_train` 上 `fit`。
7. 在 `X_test` 上计算 accuracy、precision、recall、F1 和 AUROC。

这个管道能保证预测时按相同顺序复用训练规则，也降低数据泄漏风险。

指标字典的接口固定为：

```python
metrics = {
    "accuracy": 0.75,
    "precision": 0.67,
    "recall": 0.80,
    "f1": 0.73,
    "roc_auc": 0.82,
}

print(list(metrics))
print(all(0 <= value <= 1 for value in metrics.values()))
```

预期输出：

```text
['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
True
```

这些数字只是接口示例，不是样例数据的实际模型成绩。小数据上的一次分数波动较大，不能当作可靠商业结论。

## 如何完成练习

打开 [combined_customer_project.py](practice.py)，按数据流一次只实现一个函数：

1. 完成 `load_datasets`，只运行读取测试。
2. 完成 `clean_customers`，打印行数、类型、缺失和唯一值。
3. 完成 `summarize_orders`，手算一个两订单示例再对比输出。
4. 完成 `merge_customer_summary`，确认行数仍为 30。
5. 完成 `create_customer_figure`，检查文件存在、非空、Figure 已关闭。
6. 最后完成 `train_churn_classifier`，逐步检查划分、管道和指标。

不要一次复制全部参考答案。pytest 的失败信息会指向当前不符合契约的函数。

## 常见错误

### 清洗函数直接修改输入表

这会让后续调试无法比较原始数据。每个转换函数先 `copy()`，测试也会检查原表未变。

### 先连接订单明细再汇总

客户会因多笔订单重复，分类模型也会把同一客户当成多个样本。先按客户汇总，再一对一连接。

### 把取消和退货订单当成已完成消费

本项目契约明确只统计 `Completed`。如果业务规则改变，应同时修改题目、答案和测试。

### 在划分前填补、编码或缩放

测试数据会参与学习预处理参数，造成数据泄漏。让 Pipeline 只在训练集上 `fit`。

### 把测试分数当成部署效果

本项目只有 30 位清洗后客户，用于练习完整流程，不足以证明模型可以上线。真实应用需要更多数据、时间外验证、公平性和监控。

## 与 IOM103 原项目的对应

综合项目复用了 IOM103 中出现的核心流程：读取 CSV、清理数值与类别、客户级汇总、合并、Matplotlib 输出、训练/测试划分、`ColumnTransformer`、`Pipeline`、逻辑回归和分类指标。样例数据和函数是独立教学材料，不修改原始 `IOM103/Project`。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 运行命令

从项目根目录运行完整示例：

```powershell
python -m projects.combined_customer_project.example
```

只测试综合项目：

```powershell
pytest projects/combined_customer_project/test.py
```

未完成的六个练习会显示 6 个 `XFAIL`。当你全部实现正确后，应变成 6 个 practice `PASSED`。

## 最终交付检查清单

- [ ] 我能从两张 CSV 解释每一列的业务含义和数据粒度。
- [ ] 我能识别重复、类别不统一、无效数字、坏日期和缺失值。
- [ ] 我能说明为什么只统计 Completed 订单。
- [ ] 我能手算订单金额、总消费和平均订单金额。
- [ ] 我能解释为什么要先汇总再左连接。
- [ ] 我能保存图片并确认没有遗留打开的 Figure。
- [ ] 我能列出模型的数值特征、分类特征和标签。
- [ ] 我能解释先划分、后拟合预处理器如何避免泄漏。
- [ ] 我能解释五个测试指标，而不是只报告 accuracy。
- [ ] 我能在不看答案的情况下按六个函数独立完成整个流程。
