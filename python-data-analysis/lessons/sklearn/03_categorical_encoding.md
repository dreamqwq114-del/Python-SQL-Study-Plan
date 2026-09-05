# 第 3 节：把城市等分类文字变成独热编码

## 本节解决什么实际问题

客户表中的城市、合同类型是文字，但多数机器学习模型需要数字。不能随意把 Suzhou、Shanghai、Nanjing 编成 1、2、3，因为数字大小会制造不存在的顺序。本节用独热编码把每个类别变成一个“是否属于该类别”的列。

- **分类特征（categorical feature）**：取值表示类别而非连续数量，例如城市。
- **独热编码（one-hot encoding）**：每个类别建立一个 0/1 列。
- **编码器（encoder）**：学习有哪些类别并执行转换的对象。

## 一个分类列如何编码

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

train = pd.DataFrame({"city": ["Suzhou", "Shanghai", "Suzhou"]})

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(train[["city"]])

print(encoder.get_feature_names_out(["city"]).tolist())
print(encoded.tolist())
```

预期输出：

```text
['city_Shanghai', 'city_Suzhou']
[[0.0, 1.0], [1.0, 0.0], [0.0, 1.0]]
```

`fit` 表示从训练数据学习类别；`transform` 表示按已学规则转换；`fit_transform` 是先学习再转换的简写。

## 为什么测试集只能 transform

测试集模拟未来客户，因此不能帮助决定编码列。正确顺序是：

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

train = pd.DataFrame({"city": ["Suzhou", "Shanghai"]})
test = pd.DataFrame({"city": ["Shanghai", "Wuxi"]})

encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False,
)
train_encoded = encoder.fit_transform(train[["city"]])
test_encoded = encoder.transform(test[["city"]])

print(train_encoded.tolist())
print(test_encoded.tolist())
```

预期输出：

```text
[[0.0, 1.0], [1.0, 0.0]]
[[1.0, 0.0], [0.0, 0.0]]
```

`Wuxi` 没在训练集出现，是**未知类别**。`handle_unknown="ignore"` 让它在已有城市列中全部编码为 0，而不是运行时报错。模型不会凭空学会 Wuxi，只是可以继续预测。

`sparse_output=False` 让示例返回普通二维数组。真实大表类别很多时，稀疏矩阵会更节省内存。

## 多个分类特征

`OneHotEncoder` 可以一次处理多个列。列名会包含原字段名，避免把不同字段中的相同文本混淆：

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

data = pd.DataFrame(
    {
        "city": ["Suzhou", "Shanghai"],
        "contract": ["Monthly", "Annual"],
    }
)
encoder = OneHotEncoder(sparse_output=False)
encoder.fit(data)
print(encoder.get_feature_names_out().tolist())
```

预期输出：

```text
['city_Shanghai', 'city_Suzhou', 'contract_Annual', 'contract_Monthly']
```

## 常见错误

### 分别对训练集和测试集 fit_transform

两边可能得到不同列或不同顺序，模型无法正确解释测试数据。只对训练集 `fit`，测试集只 `transform`。

### 直接用 1、2、3 编城市

模型可能错误理解成“城市 3 大于城市 1”。没有自然顺序的类别应使用独热编码。

### 忘记双层方括号

编码器需要二维输入，应写 `data[["city"]]`，不是 `data["city"]`。

## 与 IOM103 原项目的对应

原项目在分类处理管道中使用 `OneHotEncoder(handle_unknown="ignore")`。`ColumnTransformer` 叫作**列转换器**：它把指定的数值列和分类列送进不同处理流程，再把结果横向合并；原项目用它只对文字列执行独热编码。详见 [原项目分析](../../ORIGINAL_PROJECT_ANALYSIS.md)。

## 本节练习

1. 用训练城市拟合编码器并转换训练、测试数据。
2. 同时编码多个分类字段。
3. 返回编码后的完整特征名称。

## 运行命令

```powershell
python -m examples.sklearn.example_03_categorical_encoding
pytest tests/sklearn/test_sklearn_practice.py -k "03"
```

## 本节检查清单

- [ ] 我能解释为什么城市不能随意编码成 1、2、3。
- [ ] 我能说明 `fit`、`transform`、`fit_transform` 的区别。
- [ ] 我只会在训练集上学习类别。
- [ ] 我知道未知类别编码成全 0 的含义。
- [ ] 我能取出编码后的列名。
