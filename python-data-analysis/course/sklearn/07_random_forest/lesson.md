# 第 7 节：让多棵树组成随机森林

## 本节解决什么实际问题

一棵决策树可能因少量样本变化就得到不同规则。随机森林训练许多彼此略有不同的树，再综合它们的结果，通常比单棵树更稳定。

- **集成学习（ensemble learning）**：组合多个模型共同做决定。
- **随机森林（random forest）**：用不同样本子集和特征子集训练多棵决策树，再投票或平均。
- **估计器（estimator）**：scikit-learn 对可训练模型的统称；森林中的每棵树也是一个估计器。

## 训练 50 棵树

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

X, y = make_classification(
    n_samples=60,
    n_features=4,
    n_informative=3,
    n_redundant=0,
    random_state=42,
)

model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
)
model.fit(X, y)

print(model.n_estimators)
print(len(model.estimators_))
print(round(float(model.feature_importances_.sum()), 3))
```

预期输出：

```text
50
50
1.0
```

`n_estimators=50` 指定森林含 50 棵树。训练完成后，`estimators_` 保存这些树。

## 多数投票的直观含义

分类森林会综合各棵树的意见：

```python
tree_votes = [1, 0, 1, 1, 0]
positive_votes = sum(tree_votes)
prediction = int(positive_votes > len(tree_votes) / 2)

print(positive_votes)
print(prediction)
```

预期输出：

```text
3
1
```

实际 `predict_proba` 会平均树给出的类别概率，不只是计算这段简单投票。

## 森林为什么具有随机性

训练每棵树时会抽取不同的样本，也会在每次分裂时只考虑部分特征。因此树之间不会完全相同。`random_state=42` 固定这些随机选择，让实验可复现。

## 树的数量如何选择

增加 `n_estimators` 通常会让结果更稳定，但训练和预测更慢。不是越多越好，应记录运行时间并比较测试表现：

```python
settings = [10, 50, 100]
estimated_relative_cost = [1, 5, 10]
print(list(zip(settings, estimated_relative_cost)))
```

预期输出：

```text
[(10, 1), (50, 5), (100, 10)]
```

这里的成本只是用于理解的相对示例，不是实际计时结果。

## 常见错误

### 忘记固定 random_state

每次运行结果可能略变，难以判断是代码变化还是随机变化。课程实验统一使用 42。

### 只看训练准确率

森林也会过拟合。候选模型应在训练数据内部使用同一验证集比较；选定模型后，才在独立测试集上做一次最终评价。

### 认为森林的重要性就是因果

森林重要性仍只是模型内部贡献，并可能偏向可分裂取值较多的特征。

## 与 IOM103 原项目的对应

原项目把随机森林作为三个候选分类器之一，在同一训练/测试划分和预处理流程下，与逻辑回归、决策树比较。详见 [原项目分析](../../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 训练含 50 棵树的固定随机森林。
2. 使用给定树数训练森林。
3. 返回按重要性降序排列的特征表。

## 运行命令

```powershell
python -m course.sklearn.07_random_forest.example
pytest course/sklearn/07_random_forest/test.py
```

## 本节检查清单

- [ ] 我能解释集成学习和随机森林。
- [ ] 我知道 `n_estimators` 表示树的数量。
- [ ] 我能说明森林为何比单棵树更稳定。
- [ ] 我会固定随机种子并在测试集评估。
- [ ] 我能在稳定性和运行成本间做选择。
