# 第 9 节：用五个指标评价流失模型

## 本节解决什么实际问题

“模型准确率 90%”不一定代表模型好。如果 90% 客户本来就不流失，一个永远预测“不流失”的模型也有 90% 准确率，却找不到任何风险客户。本节从不同角度评价模型。

先认识四个计数：

- **TP**：实际流失，预测也流失。
- **FP**：实际未流失，却预测流失。
- **FN**：实际流失，却预测未流失。
- **TN**：实际未流失，预测也未流失。

## accuracy、precision、recall

- **准确率 accuracy** = `(TP + TN) / 全部样本`，整体猜对多少。
- **精确率 precision** = `TP / (TP + FP)`，被模型标为流失的人中有多少真的流失。
- **召回率 recall** = `TP / (TP + FN)`，真实流失客户中找回了多少。

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score

y_true = [0, 0, 1, 1]
y_pred = [0, 1, 1, 1]

print(accuracy_score(y_true, y_pred))
print(round(precision_score(y_true, y_pred), 3))
print(recall_score(y_true, y_pred))
```

预期输出：

```text
0.75
0.667
1.0
```

模型找到了全部两个流失客户，所以 recall 是 1；但把一个未流失客户误报为流失，因此 precision 只有约 0.667。

## F1 是什么

**F1 分数**是 precision 和 recall 的调和平均：`2 × precision × recall / (precision + recall)`。只有两者都高时 F1 才高。

```python
from sklearn.metrics import f1_score

y_true = [0, 0, 1, 1]
y_pred = [0, 1, 1, 1]

print(round(f1_score(y_true, y_pred), 3))
```

预期输出：

```text
0.8
```

当误报成本和漏报成本都重要时，F1 是一个有用的综合指标，但仍不能代替业务判断。

## specificity 是什么

**特异度 specificity** 衡量真实负类中有多少被正确识别，公式是
`TN / (TN + FP)`。在流失预测中，它回答“实际未流失的客户里，有多少没有被误报为
流失”。它与 recall 观察的类别方向不同：recall 关注真实正类，specificity 关注真实负类。

如果数据中没有真实负类，`TN + FP` 为 0，数学上的 specificity 没有定义。为了让本章
编程练习的返回值保持稳定，练习合同规定这种情况返回 `0.0`；解释结果时仍应说明数据中
缺少真实负类，不能把 `0.0` 当成正常业务表现。

## AUROC 是什么

**ROC 曲线**考察阈值从高到低变化时，召回正类与误报正类的关系。**AUROC** 是这条曲线下面积，衡量模型把随机一个正类排在随机一个负类前面的能力。

```python
from sklearn.metrics import roc_auc_score

y_true = [0, 0, 1, 1]
y_probability = [0.10, 0.60, 0.70, 0.90]

print(roc_auc_score(y_true, y_probability))
```

预期输出：

```text
1.0
```

虽然 0.60 按 0.5 阈值会造成一次误报，但所有正类概率仍高于所有负类概率，所以排序能力是 1.0。AUROC 用概率，不应传入已阈值化的类别标签。

## 如何选择指标

- 联系每位客户成本很高：更关心 precision，减少无效联系。
- 漏掉流失客户损失很大：更关心 recall。
- 两者都重要：同时报告 precision、recall、F1。
- 想比较不同阈值前的整体排序能力：查看 AUROC。
- 类别平衡且两种错误代价接近：accuracy 更容易解释。

## 常见错误

### 只报告 accuracy

类别不平衡时可能掩盖模型完全找不到少数类。至少同时报告 precision、recall、F1 和类别分布。

### 用类别标签计算 AUROC

AUROC 应使用正类概率或连续决策分数，否则大量排序信息已经丢失。

### 测试集只有一个类别

AUROC 需要同时存在正类和负类。应在划分时分层并检查标签；无法满足时，不应伪造 AUROC。

## 与 IOM103 原项目的对应

原项目对每个分类模型计算 Accuracy、Precision、Recall、F1 和 AUROC，并以表格比较。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 一次计算五个分类指标。
2. 比较不同阈值下的 precision、recall 和 F1。
3. 根据 TN 与 FP 计算特异度。

## 本章完整示例

下面的完整脚本把本章知识点串联起来，建议先通读再动手做练习；需要运行时可复制到文件中执行。

```python
"""在一组固定预测上计算分类指标演示。"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def demo_score_fixed_predictions() -> dict[str, float]:
    """演示五个常用二分类指标各自如何调用。"""
    actual = np.array([0, 0, 1, 1])
    predicted = np.array([0, 1, 1, 1])
    probability = np.array([0.1, 0.6, 0.7, 0.9])
    return {
        "accuracy": accuracy_score(actual, predicted),
        "precision": precision_score(actual, predicted, zero_division=0),
        "recall": recall_score(actual, predicted, zero_division=0),
        "f1": f1_score(actual, predicted, zero_division=0),
        "roc_auc": roc_auc_score(actual, probability),
    }


def main() -> None:
    for name, value in demo_score_fixed_predictions().items():
        print(name, round(value, 3))


if __name__ == "__main__":
    main()
```

运行本章测试：

```powershell
pytest course/sklearn/09_classification_metrics/test.py
```

## 本节检查清单

- [ ] 我能用 TP、FP、FN、TN 解释 accuracy、precision、recall。
- [ ] 我能解释 F1 为什么要求 precision 和 recall 同时较好。
- [ ] 我知道 AUROC 使用概率而非类别。
- [ ] 我能根据业务成本选择主要指标。
- [ ] 我知道测试集缺少一个类别时不能计算 AUROC。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>calculate_metrics</code></summary>

从 sklearn.metrics 分别导入五个函数。

</details>

<details>
<summary><code>calculate_threshold_metrics</code></summary>

先生成 y_pred，再调用三个指标函数。

</details>

<details>
<summary><code>calculate_specificity</code></summary>

confusion_matrix(..., labels=[0,1]).ravel() 得到 tn,fp,fn,tp。

</details>
