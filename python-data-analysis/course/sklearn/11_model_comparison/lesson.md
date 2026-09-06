# 第 11 节：公平比较多个分类模型

## 本节解决什么实际问题

逻辑回归容易解释，决策树规则直观，随机森林通常更稳定。不能凭模型名字选择，也不能让不同模型使用不同数据。公平比较要求它们经历相同的数据划分、预处理和评价标准。

- **基线模型（baseline model）**：用于比较的简单起点，例如逻辑回归。
- **候选模型（candidate model）**：准备在相同任务上比较的模型。
- **模型比较（model comparison）**：在相同数据和指标下评估多个候选模型。
- **验证集（validation set）**：从训练数据中留出、用于比较模型和调整设置的数据；最终测试集仍保持未使用。

## 先统一比较规则

下面用一张已算好的结果表演示如何排序：

```python
import pandas as pd

results = pd.DataFrame(
    {
        "model": ["Logistic Regression", "Decision Tree", "Random Forest"],
        "accuracy": [0.81, 0.78, 0.84],
        "roc_auc": [0.86, 0.75, 0.89],
    }
)
ranked = results.sort_values(
    ["roc_auc", "accuracy"],
    ascending=False,
).reset_index(drop=True)

print(ranked["model"].tolist())
print(ranked.loc[0, "model"])
```

预期输出：

```text
['Random Forest', 'Logistic Regression', 'Decision Tree']
Random Forest
```

这里先按 AUROC 排序，若相同再看 accuracy。实际项目必须在建模前说明主要指标，不能看完结果后才挑对自己最有利的规则。

## 公平比较的数据流

```python
models = ["Logistic Regression", "Decision Tree", "Random Forest"]
shared_rules = {
    "same_fit_rows": True,
    "same_validation_rows": True,
    "same_target": True,
    "same_metrics": True,
}

print(len(models))
print(all(shared_rules.values()))
```

预期输出：

```text
3
True
```

所有候选模型应使用同一组 `X_fit`、`X_validation`、`y_fit`、`y_validation`。需要缩放的模型可以在各自管道中缩放，但验证信息不能进入 `fit`。选好模型后，可以在完整训练数据上重新拟合，最终测试集只用于一次正式评价。

## 选择模型不只看最高分

假设两个模型分数接近，还应考虑：

- 解释成本：业务人员能否理解决策。
- 运行成本：训练和预测需要多长时间、多少内存。
- 稳定性：换一批数据后结果是否大幅变化。
- 错误成本：模型的 FP、FN 是否符合业务需求。
- 维护成本：流程是否容易复现和更新。

```python
best_auc = 0.891
simpler_auc = 0.889
print(round(best_auc - simpler_auc, 3))
```

预期输出：

```text
0.002
```

0.002 的差距未必足以抵消更高的解释和维护成本。最终决定要把统计表现和业务限制一起写清。

## 常见错误

### 每个模型使用不同划分

分数差异可能来自验证样本难度不同。应只划分一次，再把相同拟合集和验证集传给所有模型。

### 在测试集上反复挑模型和调参数

测试集逐渐参与了选择，最终分数会偏乐观。参数选择应使用训练集内部的验证，测试集留作最终评价。

### 只保留最佳模型结果

应保留完整比较表和选择理由，让别人能复核判断。

## 与 IOM103 原项目的对应

原项目在同一预处理和划分下训练 Logistic Regression、Decision Tree 和 Random Forest，计算五个指标，并按 AUROC 选择模型。不过它使用同一测试集完成模型选择和最终汇报，最终数字可能略偏乐观；更规范的课程流程会在训练集内部验证，最后才使用测试集。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 在同一拟合集和验证集上训练并比较逻辑回归与决策树。
2. 按指定主指标和次指标给模型排名。
3. 返回得分最高的模型名称，并处理空结果。

## 运行命令

```powershell
python -m course.sklearn.11_model_comparison.example
pytest course/sklearn/11_model_comparison/test.py
```

## 本节检查清单

- [ ] 我知道所有候选模型必须使用同一验证集。
- [ ] 我能区分验证集与最终测试集的职责。
- [ ] 我能先确定主要指标，再比较结果。
- [ ] 我能生成和排序模型比较表。
- [ ] 我不会在最终测试集上反复调参。
- [ ] 我能结合解释性、成本和错误类型选择模型。

---

## 本节提示（卡住时再展开）

<details>
<summary>全部展开</summary>

下面按练习函数列出最小提示，先独立思考，确实卡住再展开对应条目。

</details>

<details>
<summary><code>compare_models</code></summary>

对每个模型 fit、predict、predict_proba，再把字典加入列表。

</details>

<details>
<summary><code>rank_models</code></summary>

sort_values(metric, ascending=False).reset_index(drop=True)。

</details>

<details>
<summary><code>select_best_model_name</code></summary>

results[metric].idxmax() 返回第一个最大值的索引标签。

</details>
