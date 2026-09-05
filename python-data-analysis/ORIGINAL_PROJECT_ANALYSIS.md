# IOM103 原项目阅读总结

分析依据是只读检查 `../Project/` 下的三个原始 CSV、三份 `Data Description` PDF、`IOM103_A2_B_training_code.py`、最终 Notebook、报告草稿、`outputs/` 和 `figures/`。原项目中没有 README 和 requirements.txt。下面区分数据说明、代码事实、输出事实与业务解释；未从材料中确认的内容标为“不确定”。

## 1. 业务目标

- Task A2：预测电信客户是否流失，让企业优先联系高风险客户。入口是 `task_a2_churn_prediction()`（训练脚本第 133–276 行）。
- Task B：根据年龄、年收入、消费评分把客户分群，支持差异化营销。入口是 `task_b_customer_segmentation()`（第 302–402 行）。
- `Sales Dataset_Task A1.csv` 是另一个可选销售预测任务（1,000 行），目标是帮助零售商做订货和库存控制；但最终脚本和最终 Notebook 没有执行 A1，不能把它说成最终模型的一部分。依据是 `Data Description Task A1.pdf` 与最终代码。

## 2. 数据规模和主要字段

- A2：`Customer-Churn_Task A2.csv`，7,043 行 × 21 列；目标 `Churn` 中 No=5,174、Yes=1,869，流失率约 26.54%。
- 字段包括客户标识 `customerID`，人口属性 `gender/SeniorCitizen/Partner/Dependents`，使用时长 `tenure`，电话与网络服务字段，`Contract`、`PaymentMethod`，以及 `MonthlyCharges/TotalCharges/Churn`。
- B：`Customer Segmentation_Task B.csv`，200 行 × 5 列：`CustomerID`、`Gender`、`Age`、`Annual Income (k$)`、`Spending Score (1-100)`。
- A1：`Sales Dataset_Task A1.csv`，1,000 行 × 7 列：日期 `Date`、产品类别 `Product`、价格 `Price`、折扣 `Discount`、客户类型 `CustomerType`、营销投入 `MarketingEffort` 和目标销量 `Sales`。CSV 检查结果为无标准缺失值和无完整重复行，与 `Data Description Task A1.pdf` 一致。
- CSV 直接读取时没有标准 NA，也没有完整重复行。不过 A2 的 `TotalCharges` 是文本列，空白字符串经 `pd.to_numeric(errors="coerce")` 后才成为缺失值（第 67–73 行）。
- `Data Description Task A2.pdf` 写的是单数 `MonthlyCharge/TotalCharge`，实际 CSV 与代码使用复数 `MonthlyCharges/TotalCharges`，实现时应以真实列名为准。该 PDF 对 Churn 时间范围同时出现“last month”和“this quarter”，因此具体统计窗口不确定，不能自行断言。
- `Data Description Task B.pdf` 说明 Spending Score 是商场根据客户行为和消费情况制定的评分，但没有公开具体计算公式，所以评分生成规则不确定。

## 3. 从读取到结果的完整流程

```text
A2 CSV -> TotalCharges 转数值/中位数填充 -> 删除 ID -> Churn 映射 0/1
       -> 分层 75/25 划分 -> 数值中位数+标准化 / 类别众数+独热编码
       -> 逻辑回归、分类树、随机森林 -> predict/predict_proba
       -> AUROC/Accuracy/Precision/Recall/F1 -> ROC、混淆矩阵、特征表

B CSV  -> 选择 Age/Income/Spending -> StandardScaler
       -> k=2..10 的 KMeans -> inertia + silhouette
       -> 人工选择 k=5 -> 聚类标签 -> groupby/agg 概括 -> 业务画像与图表
```

A2 的关键函数是 `prepare_churn_data()`、`create_preprocessor()`、`calculate_model_scores()`、`get_processed_feature_names()` 和 `task_a2_churn_prediction()`。B 的关键函数是 `cluster_description()` 与 `task_b_customer_segmentation()`。最终 Notebook 共 8 个单元：单元 2 导入和路径，单元 4 为 A2，单元 6 为 B，单元 8 运行全部流程；`Untitled.ipynb` 只是 `%run IOM103_A2_B_training_code.py`。

## 4. 实际结果

- `outputs/task_a2_model_metrics.csv`：逻辑回归 AUROC 0.8460048、Recall 0.7944325；随机森林 AUROC 0.8458261，但 Accuracy 和 F1 略高；分类树 AUROC 0.8315938。因此只能说逻辑回归按 AUROC 排名第一，不能说它所有指标都最好。
- `outputs/task_b_cluster_number_evaluation.csv`：k=6 的轮廓系数 0.42743，高于 k=5 的 0.41664；代码仍在第 349–352 行明确选择 5 类，理由来自肘部形态和业务可解释性。
- 5 类画像来自 `task_b_cluster_summary.csv`：低收入低消费、年轻且促销敏感、VIP、高收入低消费潜力、年龄较高且相对稳定。聚类编号本身没有天然业务含义。

## 5. 实际用到的 Python 基础

- 导入、常量、函数、返回值、字典、列表、循环、条件、`range`、`hasattr`、f-string、上下文路径判断和主入口。
- 示例位置：模型字典与循环第 169–203 行；聚类 k 循环第 316–324 行；业务画像 if 条件第 284–299 行；`if __name__ == "__main__"` 第 412–413 行。

## 6. 实际用到的 Pandas

- `read_csv`、`to_numeric(errors="coerce")`、`fillna`、`median`、`drop`、`map`、`select_dtypes`、`tolist`。
- `DataFrame`、`groupby`、`mean`、`sort_values`、`reset_index`、`melt`、`agg`、`apply(axis=1)`、`round`、`head`、`to_string`、`to_csv(index=False)`。
- 典型位置：A2 清洗第 66–79 行；合同流失率第 143–149 行；模型指标表第 204–205 行；B 分群汇总第 355–369 行。

## 7. 实际用到的 Matplotlib/绘图

- Matplotlib：`figure`、`plot`、`title`、`xlabel`、`ylabel`、`ylim`、`legend`、`tight_layout`、`savefig`、`close`。
- 原项目还用 Seaborn 的 `barplot`、`heatmap`、`lineplot`、`scatterplot` 和 `set_theme`。新学习库按要求只教 Matplotlib/Pandas `.plot()`，不新增 Seaborn 依赖。
- 图表输出包括合同流失率、ROC 曲线、混淆矩阵、预测特征、肘部法、轮廓系数、聚类散点和群组画像。

## 8. 实际用到的 scikit-learn

- 预处理：`SimpleImputer`、`OneHotEncoder`、`StandardScaler`、`ColumnTransformer`、`Pipeline`。
- 划分与模型：`train_test_split`、`LogisticRegression`、`DecisionTreeClassifier`、`RandomForestClassifier`、`KMeans`。
- 指标：`accuracy_score`、`precision_score`、`recall_score`、`f1_score`、`roc_auc_score`、`roc_curve`、`auc`、`confusion_matrix`、`classification_report`、`silhouette_score`。

## 9. 适合现在学习的内容

优先掌握 `read_csv -> 检查 shape/dtypes -> 清洗 -> X/y -> split -> 只在训练集 fit -> predict/predict_proba -> 多指标解释`。随后学习 `groupby/agg`、图表选择、KMeans、肘部法与轮廓系数。这些内容已拆到本项目的 Python、Pandas、Matplotlib 和 sklearn 示例中。

## 10. 暂时不必深入

暂不深入复杂 Pipeline 设计、交叉验证调参、概率阈值优化、模型校准、SHAP、统计推断、深度学习、部署和生产监控。原项目的 `ColumnTransformer + Pipeline` 先理解输入输出与防泄漏作用即可。

## 11. 最难解释的代码

- 第 82–107 行：按 dtype 分数值/类别列，再把两个子 Pipeline 放入 `ColumnTransformer`。
- 第 125–130、253–269 行：从独热编码器恢复处理后特征名，并让系数/特征重要性与名称对齐。
- 第 210–269 行：按 AUROC 选模型，再根据模型是否有 `feature_importances_` 决定解释方式。
- 第 355–369 行：命名聚合、lambda 性别计数以及逐行 `apply(cluster_description)`。

## 12. 原项目可改进处

- 数据泄漏：`TotalCharges` 的中位数在划分训练/测试集前用全量数据计算（第 70–73 行）。更规范的做法是只把文本转成数值，把填充值交给 Pipeline 在训练集学习。
- 测试集兼任模型选择和最终报告：第 202–212 行在同一测试集比较并选择最佳模型，会使最终数字略乐观；更规范做法是交叉验证或训练/验证/测试三段。
- 重复代码：训练脚本和 Notebook 单元 2/4/6/8 基本重复，后续修改容易不同步。
- 预处理器对象在三个 Pipeline 中复用（第 167、194–199 行），虽然每次使用相同训练数据重拟合，结果可运行，但结构较脆弱；每个模型单独创建预处理器或用克隆更清楚。
- `warnings.filterwarnings` 全局隐藏指定 KMeans 警告，可能让初学者错过环境问题。
- `cluster_description()` 的阈值是人工规则，业务依据不确定；画像是解释层，不是 KMeans 自动输出。
- 路径总体使用 `pathlib`，但同时为脚本和 Notebook写了 `__file__`/cwd 分支，且存在只负责 `%run` 的 Notebook，入口略显分散。
- 字段说明与实际 CSV 存在单复数差异，Churn 时间口径在说明 PDF 内也不一致；报告或面试表达应明确以实际数据列和已验证代码为准。

## 13. 最优先掌握的知识点

1. DataFrame、Series、列选择、shape、dtype 与缺失值。
2. `TotalCharges` 的“空白文本 -> 数值 NaN -> 训练集填充”全过程。
3. X 是二维特征、y 是一维标签，ID 和标签为何不进入 X。
4. 分层划分，以及 fit 只能学习训练集。
5. `predict`、`predict_proba[:, 1]` 和 Accuracy/Precision/Recall/F1/AUROC 的区别。
6. 类别编码与标准化。
7. KMeans 为什么需要缩放，以及“聚类编号不等于业务名称”。
