# 第 6 节：用决策树学习判断规则

## 本节解决什么实际问题

业务人员常会问：“模型为什么认为这位客户会流失？”决策树把判断写成一连串条件，例如“合同期短吗”“月消费额高吗”，因此比许多模型更容易解释。

- **决策树（decision tree）**：不断按特征阈值把样本分组的模型。
- **根节点（root node）**：最上方的第一次判断。
- **内部节点（internal node）**：中间的判断条件。
- **叶节点（leaf node）**：不再分裂、给出预测结果的位置。
- **树深度（depth）**：从根节点到最远叶节点经过的层数。

## 训练一棵有限深度的树

```python
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=60,
    n_features=3,
    n_informative=2,
    n_redundant=0,
    random_state=42,
)

model = DecisionTreeClassifier(
    max_depth=3,
    random_state=42,
)
model.fit(X, y)

print(model.max_depth)
print(model.get_depth())
print(round(float(model.feature_importances_.sum()), 3))
```

预期输出：

```text
3
3
1.0
```

`max_depth=3` 是训练前设置的上限；`get_depth()` 是训练后实际得到的深度。特征重要性经过归一化，总和为 1。

## 树怎样做一次判断

下面不是训练代码，而是一个两层树可能表达的业务规则：

```python
contract_months = 1
monthly_spending = 520

if contract_months <= 1:
    if monthly_spending > 400:
        prediction = 1
    else:
        prediction = 0
else:
    prediction = 0

print(prediction)
```

预期输出：

```text
1
```

真实决策树会从数据中自动选择特征和阈值，而不是由人手写这些条件。

## 特征重要性是什么

树在分裂时会选择最能减少类别混杂的特征。`feature_importances_` 汇总每个特征对这些分裂的贡献：

```python
import pandas as pd

importance = pd.DataFrame(
    {
        "feature": ["age", "monthly_spending", "contract_months"],
        "importance": [0.10, 0.65, 0.25],
    }
).sort_values("importance", ascending=False)

print(importance["feature"].tolist())
```

预期输出：

```text
['monthly_spending', 'contract_months', 'age']
```

重要性高表示模型经常依赖它做有效分裂，不表示它在现实中导致流失，也不表示关系一定是正向。

## 为什么要限制深度

树越深，规则越细，甚至可能为单个训练客户建立专门规则。这会提高训练分数，却降低处理新客户的能力。`max_depth` 是控制复杂度的超参数。

## 常见错误

### 不限制树的复杂度

树可能记住噪声。可以限制 `max_depth`、`min_samples_split` 或 `min_samples_leaf`，并在训练数据内部的验证集上比较候选设置；最终测试集只评价选定设置一次。

### 认为树完全不需要预处理

树通常不需要标准化，普通字符串仍必须编码。现代 scikit-learn 的 `DecisionTreeClassifier` 可以原生处理数值 `NaN`，但并非所有候选模型都支持；本课程仍统一使用缺失值填补器（imputer），让三种分类器共享明确、可复现的缺失值规则。

### 把重要性当成因果

特征重要性只是模型内部的分裂贡献。相关特征还可能互相分摊重要性。

## 与 IOM103 原项目的对应

原项目训练了限制深度的 `DecisionTreeClassifier`，计算测试指标，并提取经过预处理后的特征重要性。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 训练 `max_depth=3` 的固定决策树。
2. 根据给定深度训练树，比较模型复杂度。
3. 把特征名和重要性整理成降序表。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""训练深度受限的客户分类决策树。"""

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

def train_tree() -> DecisionTreeClassifier:
    """训练 max_depth=3 的确定性决策树。"""
    X, y = make_classification(
        n_samples=60,
        n_features=3,
        n_informative=2,
        n_redundant=0,
        random_state=42,
    )
    return DecisionTreeClassifier(
        max_depth=3,
        random_state=42,
    ).fit(X, y)

def main() -> None:
    model = train_tree()
    print((model.max_depth, model.random_state))
    print(model.get_depth())
    print(round(float(model.feature_importances_.sum()), 3))

if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/06_decision_tree/test.py
```

## 本节检查清单

- [ ] 我能用节点、分裂、叶节点解释决策树。
- [ ] 我能区分最大深度和实际深度。
- [ ] 我知道限制深度是为了减少过拟合。
- [ ] 我能按特征重要性排序。
- [ ] 我不会把重要性误写成因果结论。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>train_tree</code></summary>

创建分类器后调用 fit(X, y)。

</details>

<details>
<summary><code>train_tree_with_depth</code></summary>

限制深度是控制模型复杂度的一种方法。

</details>

<details>
<summary><code>tree_importance_table</code></summary>

使用 model.feature_importances_。

</details>
