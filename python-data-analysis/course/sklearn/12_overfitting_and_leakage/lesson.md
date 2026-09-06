# 第 12 节：识别过拟合和数据泄漏

## 本节解决什么实际问题

模型在课堂数据上达到 99% 准确率，却在新客户上只有 70%，通常不是“训练得特别好”，而是过度记住了训练样本。另一种危险是测试信息提前进入训练流程，使测试成绩虚高。本节学会区分并避免这两类问题。

- **过拟合（overfitting）**：模型把训练数据中的偶然噪声也当成规律，训练表现很好，新数据表现明显下降。
- **欠拟合（underfitting）**：模型过于简单，训练集和测试集表现都差。
- **数据泄漏（data leakage）**：训练过程使用了在真实预测时不该知道的信息。
- **验证（validation）**：在训练数据内部比较设置的过程；最终测试集不参与调参。

## 用训练与测试差距检查过拟合

```python
train_accuracy = 0.98
test_accuracy = 0.72
gap = train_accuracy - test_accuracy

print(round(gap, 2))
print(gap > 0.10)
```

预期输出：

```text
0.26
True
```

这里把 0.10 当作教学示例阈值。真实项目没有通用的“超过多少一定过拟合”，应结合数据量、指标波动和业务容忍度判断。

## 常见泄漏一：先缩放后划分

错误流程是：

```text
全体 X -> fit_transform -> train_test_split
```

正确流程是：

```text
全体 X -> train_test_split -> scaler.fit(X_train)
                            -> scaler.transform(X_train)
                            -> scaler.transform(X_test)
```

用代码表示核心原则：

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

X_train = np.array([[10.0], [20.0], [30.0]])
X_test = np.array([[100.0]])

scaler = StandardScaler()
train_scaled = scaler.fit_transform(X_train)
test_scaled = scaler.transform(X_test)

print(scaler.mean_.tolist())
print(np.round(test_scaled, 3).tolist())
```

预期输出：

```text
[20.0]
[[9.798]]
```

均值只来自训练值 10、20、30，没有使用测试值 100。

## 常见泄漏二：输入中包含未来答案

预测客户是否流失时，以下字段可能泄漏：

- 已经写明 `churn` 的标签列。
- 流失之后才产生的“账号关闭日期”。
- 由全体数据预先计算、含测试标签的信息。

```python
available_before_prediction = [
    "age",
    "monthly_spending",
    "contract_type",
]
available_after_churn = ["account_closed_date"]

print(len(available_before_prediction))
print(available_after_churn)
```

预期输出：

```text
3
['account_closed_date']
```

判断标准不是“这个字段相关性高不高”，而是实际预测时能否合法获得。

## Pipeline 为什么有帮助

`Pipeline` 把预处理和模型绑成一个对象。调用 `fit(X_train, y_train)` 时，缩放、编码和模型都只从训练集学习；调用 `predict(X_test)` 时，只复用已学规则。这能降低手工顺序出错的风险。

## 常见错误

### 训练分数高就宣布成功

应同时汇报训练和测试分数，并检查差距。

### 测试集反复参与参数选择

多次查看测试成绩再改模型，也是一种信息泄漏。使用训练集内部验证，最后只用测试集做一次正式评价。

### 删除所有复杂模型就能避免过拟合

模型过简会欠拟合。应通过限制复杂度、增加有效数据、验证和正则化寻找平衡。

## 与 IOM103 原项目的对应

原项目使用 `Pipeline` 把 `ColumnTransformer` 与模型连接；管道中的编码、填补和缩放参数会在训练集上学习。但它在划分前已经用全体数据的中位数填补 `TotalCharges`，这是一个轻微的数据泄漏例外。更规范的做法是划分前只把该列转成数值，把中位数填补完全交给训练管道；本课程综合项目采用了这种做法。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 返回训练准确率、测试准确率和差值。
2. 根据给定差值阈值判断是否可能过拟合。
3. 只用训练集拟合缩放器，再转换测试集。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""比较训练/测试分数，并只用训练集拟合缩放器。"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

def evaluate_tree() -> tuple[float, float, float]:
    """返回训练分数、测试分数和泄漏安全的测试缩放值。"""
    X, y = make_classification(
        n_samples=80,
        n_features=4,
        n_informative=3,
        n_redundant=0,
        random_state=42,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        stratify=y,
        random_state=42,
    )
    model = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
    scaler = StandardScaler().fit(X_train)
    scaled_test = scaler.transform(X_test)
    return (
        model.score(X_train, y_train),
        model.score(X_test, y_test),
        float(np.mean(scaled_test)),
    )

def main() -> None:
    train_score, test_score, test_mean = evaluate_tree()
    print((round(train_score, 3), round(test_score, 3)))
    print(round(train_score - test_score, 3))
    print(round(test_mean, 3))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/12_overfitting_and_leakage/test.py
```

## 本节检查清单

- [ ] 我能区分过拟合、欠拟合和数据泄漏。
- [ ] 我会同时查看训练与测试表现。
- [ ] 我能判断某列在预测时是否真正可用。
- [ ] 我只用训练集拟合预处理器。
- [ ] 我知道测试集不能反复用于模型选择。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>compare_train_test_accuracy</code></summary>

score(X, y) 对分类器默认返回准确率。

</details>

<details>
<summary><code>detect_overfitting</code></summary>

先逐个验证范围，再进行差值比较。

</details>

<details>
<summary><code>scale_without_leakage</code></summary>

scaler.fit(X_train) 后分别调用 transform。

</details>
