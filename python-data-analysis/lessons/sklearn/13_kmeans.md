# 第 13 节：用 KMeans 给客户分群

## 本节解决什么实际问题

客户表可能没有“高价值客户”“价格敏感客户”这样的现成答案，但公司仍想按年龄、收入、消费水平发现相似群体。KMeans 不需要标签，会根据特征距离把客户分成若干组。

- **无监督学习（unsupervised learning）**：数据没有正确标签，算法从特征结构中寻找模式。
- **聚类（clustering）**：把相似样本分到同一组。
- **KMeans**：指定组数 `k`，反复更新每组中心并分配最近样本的聚类算法。
- **质心（centroid）**：一个簇在各特征上的平均位置。
- **簇标签（cluster label）**：算法给每组的编号，如 0、1、2。

## 一个二维客户分群

```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array(
    [
        [20.0, 100.0],
        [21.0, 110.0],
        [50.0, 500.0],
        [51.0, 510.0],
    ]
)

model = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=20,
)
labels = model.fit_predict(X)

print(len(labels))
print(sorted(np.bincount(labels).tolist()))
print(model.cluster_centers_.shape)
```

预期输出：

```text
4
[2, 2]
(2, 2)
```

`n_clusters=2` 要求分成两组；`fit_predict` 同时拟合并返回每行的簇编号；两个质心、两个特征，所以中心形状是 `(2, 2)`。

## KMeans 的循环

1. 初始化 `k` 个质心。
2. 把每个客户分配给距离最近的质心。
3. 用每组客户的平均位置更新质心。
4. 重复分配和更新，直到变化很小或达到迭代上限。

`n_init=20` 表示从 20 组不同初始中心开始运行，保留其中较好的结果，减少一次随机初始化带来的偶然性。

## 为什么聚类前常要标准化

如果收入范围是几万，而消费评分只有 1 到 100，欧氏距离会几乎被收入主导：

```python
income_difference = 20000
score_difference = 40
print(income_difference / score_difference)
```

预期输出：

```text
500.0
```

标准化让各特征按自身波动范围参与距离计算。没有标准化的聚类可能只是“按最大数字的列分组”。

## 簇编号没有业务顺序

簇 0 不代表最差，簇 2 也不代表最好。更换随机种子或数据后编号可能互换。应计算每个簇的平均年龄、收入、消费等，再根据画像命名。

```python
cluster_profiles = {
    0: "年轻、消费较高",
    1: "年长、消费较低",
}
print(cluster_profiles[0])
```

预期输出：

```text
年轻、消费较高
```

名称来自特征汇总，不来自编号本身。

## 常见错误

### 直接聚类未缩放数据

大尺度列会控制距离。先检查量纲，并对用于距离的连续特征标准化。

### 把簇编号当预测等级

编号只是名称。先做簇画像，再写业务解释。

### 把客户 ID 放入聚类

编号之间的距离没有业务意义，会扭曲分组。只使用有含义的行为和属性特征。

## 与 IOM103 原项目的对应

原项目选择 Age、Annual Income 和 Spending Score，先用 `StandardScaler` 标准化，再用 `KMeans(random_state=42, n_init=20)` 聚类，最后按原始单位汇总簇画像。详见 [原项目分析](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 按给定 `k` 拟合确定性 KMeans。
2. 给客户表增加 `cluster` 列。
3. 把质心整理成带特征名的 DataFrame。

## 运行命令

```powershell
python -m examples.sklearn.example_13_kmeans
pytest tests/sklearn/test_sklearn_practice.py -k "13"
```

## 本节检查清单

- [ ] 我能区分监督学习和无监督学习。
- [ ] 我能解释 KMeans 的分配与更新循环。
- [ ] 我知道为什么距离型算法常要标准化。
- [ ] 我能读取标签和质心的形状。
- [ ] 我不会给簇编号附加天然好坏含义。
