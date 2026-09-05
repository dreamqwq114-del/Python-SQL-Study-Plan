# 第 8 节：输出类别、概率和客户预测表

## 本节解决什么实际问题

客户经理不仅需要一个“会/不会流失”的标签，还需要风险概率来决定联系顺序。0.92 和 0.51 虽然都会被默认判成流失，但前者通常更值得优先关注。

- **类别预测（class prediction）**：模型给出的离散答案，如 `0` 或 `1`。
- **预测概率（predicted probability）**：模型估计样本属于每个类别的可能性。
- **阈值（threshold）**：把概率转换成类别的分界值。

## predict 与 predict_proba

```python
import numpy as np

probability_table = np.array(
    [
        [0.80, 0.20],
        [0.45, 0.55],
        [0.10, 0.90],
    ]
)

positive_probabilities = probability_table[:, 1]
predictions = (positive_probabilities >= 0.5).astype(int)

print(positive_probabilities.tolist())
print(predictions.tolist())
```

预期输出：

```text
[0.2, 0.55, 0.9]
[0, 1, 1]
```

对于标签顺序 `[0, 1]`，`predict_proba(X)[:, 1]` 取第二列，也就是正类 `1` 的概率。真实代码应先检查 `model.classes_`，不要在标签含义未知时盲目取第二列。

## 调整阈值

```python
import numpy as np

probabilities = np.array([0.35, 0.48, 0.72])
default_labels = (probabilities >= 0.50).astype(int)
sensitive_labels = (probabilities >= 0.40).astype(int)

print(default_labels.tolist())
print(sensitive_labels.tolist())
```

预期输出：

```text
[0, 0, 1]
[0, 1, 1]
```

把阈值从 0.50 降到 0.40，会标记更多风险客户。代价是可能误报更多不会流失的人。阈值应结合联系成本和漏掉客户的损失来选择。

## 生成可交付的预测表

```python
import pandas as pd

result = pd.DataFrame(
    {
        "customer_id": ["C001", "C002", "C003"],
        "predicted_churn": [0, 1, 1],
        "churn_probability": [0.20, 0.55, 0.90],
    }
).sort_values("churn_probability", ascending=False)

print(result["customer_id"].tolist())
print(result.shape)
```

预期输出：

```text
['C003', 'C002', 'C001']
(3, 3)
```

保留客户编号是为了把结果交回业务人员，但客户编号本身不一定要进入模型特征。

## 常见错误

### 把 predict 当成概率

`predict` 返回类别，`predict_proba` 才返回概率矩阵。二者用途不同。

### 取错概率列

第二列通常对应 `model.classes_[1]`，但应检查类别顺序。若正类不是数字 1，需要按 `classes_` 找到正确列。

### 先看测试答案再调阈值

不断根据最终测试集调整阈值会让测试结果失去独立性。阈值应在训练数据内部的验证流程中确定，测试集留作最终检查。

## 与 IOM103 原项目的对应

原项目使用分类模型的标签预测计算 accuracy、precision、recall 和 F1，同时用正类概率计算 AUROC 和 ROC 曲线。详见 [原项目分析](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 同时返回类别预测和正类概率。
2. 按给定阈值把概率转成标签。
3. 把客户编号、预测标签和概率组合成结果表。

## 运行命令

```powershell
python -m examples.sklearn.example_08_predict_and_probability
pytest tests/sklearn/test_sklearn_practice.py -k "08"
```

## 本节检查清单

- [ ] 我能区分 `predict` 和 `predict_proba`。
- [ ] 我知道概率矩阵每列对应哪个类别。
- [ ] 我能用阈值生成 0/1 标签。
- [ ] 我能解释降低阈值的收益与代价。
- [ ] 我能生成包含客户编号的预测结果表。
