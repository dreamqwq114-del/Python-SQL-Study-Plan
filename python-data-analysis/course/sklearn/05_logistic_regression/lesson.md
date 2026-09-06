# 第 5 节：训练逻辑回归预测客户流失

## 本节解决什么实际问题

公司希望为每位客户计算流失概率，再优先联系高风险客户。逻辑回归是一种常用的二分类模型：输入客户特征，输出属于正类（这里是流失）的概率。

- **模型（model）**：从历史数据学习输入与答案关系的计算规则。
- **逻辑回归（Logistic Regression）**：把特征的加权结果转换成 0 到 1 概率的分类模型。名字有“回归”，但这里用于分类。
- **模型参数（parameter）**：模型从数据中学到的数字，例如系数。
- **超参数（hyperparameter）**：训练前由人设置的选项，例如正则化强度 `C`。

## 拟合、预测和评分

为了让输出稳定，下面使用 scikit-learn 自带的小型确定性数据：

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

X, y = make_classification(
    n_samples=60,
    n_features=3,
    n_informative=2,
    n_redundant=0,
    random_state=42,
)

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
)
model.fit(X, y)

print(model.coef_.shape)
print(round(model.score(X, y), 3))
```

预期输出：

```text
(1, 3)
0.917
```

`fit(X, y)` 让模型从特征和标签学习。`coef_` 保存三个特征的系数，所以形状是 1 行 3 列。`score` 对分类器返回准确率；这里只演示训练，不应把训练分数当成最终成绩。

## 从概率到类别

模型先计算概率，再按阈值转换成 `0/1`。默认阈值通常是 0.5：

```python
import numpy as np

probabilities = np.array([0.18, 0.49, 0.50, 0.83])
predictions = (probabilities >= 0.5).astype(int)

print(predictions.tolist())
```

预期输出：

```text
[0, 0, 1, 1]
```

降低阈值会找到更多可能流失的客户，也可能增加误报。阈值是业务决策，不应只凭习惯固定。

## 系数如何理解

在其他输入不变时，正系数通常表示特征增加会提高预测为正类的倾向，负系数表示降低。但系数的绝对值受特征尺度影响：

```python
import pandas as pd

table = pd.DataFrame(
    {
        "feature": ["age", "monthly_spending"],
        "coefficient": [-0.20, 0.75],
    }
)
table["direction"] = table["coefficient"].apply(
    lambda value: "提高流失倾向" if value > 0 else "降低流失倾向"
)
print(table["direction"].tolist())
```

预期输出：

```text
['降低流失倾向', '提高流失倾向']
```

模型系数反映数据中的关联，不证明因果关系。不能据此断言“消费额导致流失”。

## C 和 max_iter

- `C` 控制正则化的倒数。正则化会限制系数过度变大，帮助模型减少对训练数据的过度适应；`C` 越小，限制越强。
- `max_iter` 是求解器最多迭代次数。出现“未收敛”警告时，先确认数值已合理缩放，再适当增大它。
- `random_state=42` 使涉及随机过程的结果可复现。

## 常见错误

### 用训练准确率当最终结果

模型已经看过训练数据。应在独立测试集上评估。

### 忘记处理文字和缺失值

逻辑回归不能直接接收 `Suzhou` 或空值。应在管道中先填补、编码和缩放。

### 把系数当成因果证明

模型只学习相关模式，还可能受遗漏变量影响。系数用于辅助理解模型，不等于实验结论。

## 与 IOM103 原项目的对应

原项目用 `Pipeline`（按顺序连接预处理器和模型的管道对象）把预处理器与 `LogisticRegression` 组合起来，在训练集上拟合后计算多项测试指标，并与树模型比较。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 使用固定设置训练逻辑回归。
2. 使用给定的 `C` 训练不同强度的模型。
3. 把特征名和模型系数整理成表格。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""训练逻辑回归并查看预测与系数。"""

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

def train_model() -> tuple[LogisticRegression, object, object]:
    """创建确定性数据并训练逻辑回归。"""
    X, y = make_classification(
        n_samples=60,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    ).fit(X, y)
    return model, X, y

def main() -> None:
    model, X, y = train_model()
    print((model.random_state, model.max_iter))
    print(model.coef_.shape)
    print(round(model.score(X, y), 3))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/05_logistic_regression/test.py
```

## 本节检查清单

- [ ] 我知道逻辑回归在本课程中是分类模型。
- [ ] 我能区分模型参数和超参数。
- [ ] 我能解释 `fit`、类别预测和概率预测。
- [ ] 我知道训练分数不能代替测试分数。
- [ ] 我不会把系数解释成因果关系。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>train_logistic</code></summary>

model = LogisticRegression(...); model.fit(X, y)。

</details>

<details>
<summary><code>train_logistic_with_strength</code></summary>

scikit-learn 的 C 越小，正则化约束通常越强。

</details>

<details>
<summary><code>logistic_coefficient_table</code></summary>

先检查 len(feature_names) 与 model.coef_.shape[1]。

</details>
