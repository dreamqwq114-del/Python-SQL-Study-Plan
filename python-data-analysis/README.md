# IOM103 Python 数据分析学习项目

这是一个独立的、面向基础不牢大学生的 Python 数据分析课程。课程参考 IOM103 原项目实际用到的代码、数据结构和分析流程，但不会修改原始 `IOM103/Project`。

你会从变量和表格清洗开始，逐步完成可视化、分类、聚类，最后独立完成一个“客户表 + 订单表”的综合分析项目。

## 课程结构

课程按“**主题 / 章节**”组织，并刻意减少学习时需要来回切换的文件。**正常情况下每章你只需要主动打开 3 个文件**：

```text
course/
├── python/        Python 基础，共 9 章
│   └── 01_variables_and_types/
│       ├── lesson.md      唯一需要通读的教材：讲解 + 完整示例代码 + 练习要求 + 折叠提示 + 检查清单
│       ├── practice.py    做题时打开：完整任务契约、TODO 和 NotImplementedError
│       ├── answer.py      做完或卡住才打开：参考答案，独立成文件，避免做题时顺手看到
│       └── test.py        后台自动检查，不需要阅读
├── pandas/        Pandas 数据处理，共 14 章
├── matplotlib/    Matplotlib 图表，共 6 章
└── sklearn/       scikit-learn 建模，共 15 章
projects/
└── combined_customer_project/   跨领域综合客户项目，结构与章节相同
data/                  两张教学用样例 CSV
utils/                 集中管理项目相对路径
independent_readiness/  无答案独立测评与 Python–SQL 桥接模板
tests/                 课程级完整性测试（检查配对、接口与可移植性）
```

学习节奏固定为三步：**先通读 `lesson.md`，再写 `practice.py`，最后对照 `answer.py`**；`test.py` 只负责自动检查，不用打开阅读。

### 完整示例已经放进 lesson.md

普通章节不再单独保留 `example.py`：完整示例代码直接内联在 `lesson.md` 的“本章完整示例”代码块里，读到时即可看全，需要运行时复制到文件即可。这样每章少点一个文件。

只有“确实值得单独运行的完整案例”才额外保留 `example.py`，全课程共 3 处：

- `course/python/06_modules_and_imports/example.py`（本章专门演示 `python -m` 模块运行机制）；
- `course/sklearn/11_model_comparison/example.py`（训练 / 验证 / 测试划分下的多模型对比完整工作流）；
- `projects/combined_customer_project/example.py`（端到端综合客户分析流程）。

### 提示默认折叠，不会一眼看到

每章 `lesson.md` 末尾的“本节提示（卡住时再展开）”用 `<details>` 折叠，按练习函数逐条列出最小提示；先独立思考，确实卡住再展开对应条目。答案仍然只在 `answer.py` 中，不会写进教材。

> 为什么四个主题外面多一层 `course/` 父包？因为 `pandas`、`matplotlib`、`sklearn` 同时也是第三方依赖包的名字。如果把同名目录直接放在项目根目录，本地目录会遮蔽第三方库，导致 `import pandas` 失败。统一收在 `course/` 父包下可以彻底避免命名冲突。

四个基础领域共有 44 章：

- Python：9 章、36 道练习
- Pandas：14 章、42 道练习
- Matplotlib：6 章、18 道练习
- scikit-learn：15 章、45 道练习

另有一个综合客户项目，包含 6 个流程函数。因此全课程共有 147 道函数练习。

每个编号一一对应。例如 Pandas 第 6 章，你要用到的文件都在同一目录：

```text
course/pandas/06_missing_values/
├── lesson.md      # 通读：讲解、完整示例、练习要求、折叠提示
├── practice.py    # 做题
├── answer.py      # 对答案
└── test.py        # 自动检查（无需阅读）
```

## 第一次使用

### 1. 打开正确文件夹

在 PyCharm 或 IntelliJ IDEA 中，把 `python-data-analysis` 这个目录作为项目根目录打开。

不要只打开某个 `.py` 文件，也不要把上一级文件夹当成 Python 模块。

### 2. 选择项目解释器

课程在 Python 3.12 上完成全量验证；`requirements.txt` 同时限制了依赖的大版本范围，避免未来自动安装到接口不兼容的版本。

PowerShell 中可以验证：

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import pandas, matplotlib, sklearn; print('环境正常')"
```

通过 Git 克隆到新电脑时，`.venv` 不会包含在仓库中；请在项目根目录创建 Python 3.12 虚拟环境并安装依赖：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. 确认当前目录

以下命令都必须在项目根目录执行，也就是能直接看到 `README.md`、`course` 和 `projects` 的位置。

## 每一章的固定学习方法

以 Python 第 1 章为例。

### 第一步：通读 lesson.md

打开 `course/python/01_variables_and_types/lesson.md`。

讲解、准确输出、常见错误和“本章完整示例”代码块都在这一个文件里。先自己读懂教程中的短代码与完整示例，确认实际输出和文档一致；普通章节无需再去找单独的示例文件。

少数保留了 `example.py` 的章节（如模块导入章），才需要从项目根目录按模块运行完整案例：

```powershell
python -m course.python.06_modules_and_imports.example
```

使用 `python -m ...` 是按模块运行。它能让项目根目录中的包和相对路径被稳定找到。

### 第二步：只编辑练习

```text
course/python/01_variables_and_types/practice.py
```

每个函数的 docstring 已写明背景、参数、返回值、两个示例和特殊情况（练习文件不直接给提示，最小提示统一放在本 `lesson.md` 末尾的折叠区）。只在当前函数中把 `TODO` 和 `NotImplementedError` 替换成自己的实现，不要改函数名、参数或测试；一个文件中可以先完成部分函数，剩余函数继续保留模板标记。做题时如果卡住，回到 `lesson.md` 末尾展开对应函数的折叠提示。

### 第三步：运行本章测试

```powershell
pytest course/python/01_variables_and_types/test.py
```

未完成时显示 `XFAIL` 是正常状态，含义是“这个练习还在等待实现”。完成正确后，同一项会变成 `PASSED`；出现 `FAILED` 时，根据失败信息修改练习。

### 第四步：最后才看答案

先独立尝试、阅读失败信息并修改。确实卡住后再打开同目录的 `course/python/01_variables_and_types/answer.py`。

比较思路后关闭答案，回到 practice 自己重新写一遍，不要直接复制。更多使用约定见 [ANSWER_GUIDE.md](ANSWER_GUIDE.md)。

## 推荐学习顺序

### 第一阶段：Python

变量与类型 → 容器 → 字典 → 判断与循环 → 函数 → 模块 → 路径 → 异常 → 基础类

```powershell
pytest course/python
```

### 第二阶段：Pandas

构造表 → 读取 → 检查 → 选择 → 过滤 → 缺失值 → 类型 → 统计 → 分组 → 合并 → 映射 → 字符串 → 日期 → 保存

```powershell
pytest course/pandas
```

### 第三阶段：Matplotlib

Figure/Axes → 折线图 → 柱状图 → 直方图 → 散点图 → 布局与保存

```powershell
pytest course/matplotlib
```

绘图练习必须保存图片并关闭 Figure。测试会在临时目录检查文件存在且非空，不会污染项目。

### 第四阶段：scikit-learn

`X/y` → 划分 → 分类编码 → 标准化 → 三种分类器 → 预测 → 指标 → 比较 → 过拟合与泄漏 → KMeans → 肘部法 → 轮廓系数

```powershell
pytest course/sklearn
```

所有随机流程固定 `random_state=42`。每篇教程都会解释首次出现的模型术语，不要求你预先懂机器学习。

### 第五阶段：综合客户项目

先读 `projects/combined_customer_project/lesson.md`。

这是少数保留独立完整案例的地方，可运行完整流程示例：

```powershell
python -m projects.combined_customer_project.example
```

然后依次实现 `projects/combined_customer_project/practice.py`。

只测试综合项目：

```powershell
pytest projects/combined_customer_project/test.py
```

## 无提示独立测评与 SQL 桥接

完成章节练习后，再进入 [`independent_readiness/`](independent_readiness/)。其中的 `assessment.py` 是无答案起始模板，`rubric.md` 只定义可观察结果；不要把独立测评当成另一组可用答案练习。

同目录的 [`bridge_contract.md`](independent_readiness/bridge_contract.md) 和 `bridge_analysis.py` 与 SQL 学习材料的 `12_python_sql_bridge/` 配套：先从数据库导出一行一项目的结果，再用 Python 检查粒度、类型、项目数和预算汇总。SQL 导出结果与 Python 汇总不一致时，应回到连接和重复问题排查，不能先删掉重复行。

## 测试结果怎么读

只统计 147 个答案契约与 147 个练习契约时，初始结果是：

```text
147 passed, 147 xfailed
```

- 147 个 `passed`：参考答案通过契约，说明题目和测试一致。
- 147 个 `xfailed`：你的 147 个练习还保留 `NotImplementedError`。

当你完成一个练习，它对应的 `xfailed` 应变成 `passed`。全部独立完成后，练习与答案合计应至少有 294 个通过项，且不再有练习 `xfailed`。

运行全部测试：

```powershell
pytest
```

`pytest.ini` 已固定使用 `--import-mode=importlib`，并把章节内的 `test.py` 纳入收集，因此在项目根目录直接运行 `pytest` 即可，无需额外参数。

课程完整性测试还会检查 44 组章节是否一一对应、练习与答案接口是否一致、普通章是否把完整示例与折叠提示收进了 `lesson.md`、保留的 `example.py` 与答案是否泄露 TODO、练习函数的模板标记是否与实现状态一致，以及是否出现硬编码绝对路径或禁用依赖。

因此直接运行当前仓库的完整 `pytest` 时，还会多出 15 个课程完整性通过项，初始总结果是：

```text
162 passed, 147 xfailed
```

全部 147 个练习都独立完成并通过后，完整仓库应为：

```text
309 passed
```

## 常见问题

### `ModuleNotFoundError`

先确认终端位于项目根目录。普通章的示例直接看 `lesson.md` 代码块即可；只有保留 `example.py` 的章节才需要用 `python -m 包.模块` 运行，不要从子文件夹直接运行文件。章节目录名以数字开头属于正常设计，章节内部使用相对导入，运行时统一用 `python -m course.<主题>.<章节>.<文件>`。

### IDE 显示“没有 Python SDK”

给项目模块选择 `.venv\Scripts\python.exe`。安装 Python 插件只增加 IDE 的 Python 功能，不会自动给每个模块分配解释器。

### 测试显示 XFAIL

这不是环境坏了。打开对应 practice，确认 TODO 是否还在。只有你完成函数后它才会执行真实断言。

### 图片没有弹窗

课程要求保存图片，不要求弹窗。查看测试临时结果或自己指定的输出路径；函数会主动关闭 Figure。

### 模型分数不高

教学 CSV 只有 30 位去重后的客户，目的在于练习完整流程，不用于证明商业模型效果。先检查数据流、泄漏和指标含义，不要为了提高一次分数删除测试或偷看标签。

## 原项目与保留文件

- [原项目流程分析](ORIGINAL_PROJECT_ANALYSIS.md)：说明课程内容如何对应 IOM103。
- [参考答案使用说明](ANSWER_GUIDE.md)：答案与练习的配合方式。
- `data/`：课程样例数据，不在练习中修改。
- `utils/paths.py`：集中管理项目相对路径。
- `python_data_analysis_basics_before_restructure_20260726_152557.zip`：重构前源码备份，不包含 `.venv` 和缓存。
- 原始 `IOM103/Project`：始终保持只读。
