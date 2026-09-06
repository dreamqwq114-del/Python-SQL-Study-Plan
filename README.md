# Python-SQL-Study-Plan

面向数据分析初学者的自学仓库，包含两条相互衔接的学习线：**Python 数据分析**与 **SQL 查询基础**。两条线都按“先读教材 → 动手练习 → 对照答案 → 自动检查”的节奏组织，适合基础不牢、需要循序渐进的学习者。

## 目录导航

```text
Python-SQL-Study-Plan/
├── python-data-analysis/   Python 数据分析课程（pandas / matplotlib / scikit-learn）
└── sql-practice/           SQL 入门练习
    ├── mysql_beginner_practice/   MySQL 8.0，按章节组织（主推版本）
    └── sql_beginner_practice/     SQL Server / T-SQL，按天组织的等价练习
```

## 一、Python 数据分析：`python-data-analysis/`

从变量和表格清洗开始，逐步完成数据处理、可视化、分类与聚类，最后做一个“客户表 + 订单表”的综合分析项目。

- 主题与章数：Python 基础 9 章、Pandas 14 章、Matplotlib 6 章、scikit-learn 15 章，共 44 章、147 道练习，外加 1 个综合项目。
- 按“主题 / 章节”组织，四个主题统一收在 `course/` 父包下（避免 `pandas`、`matplotlib`、`sklearn` 这些目录名遮蔽同名第三方库）。
- **每章学习时只需主动打开 3 个文件**：
  - `lesson.md`：唯一需要通读的教材，知识讲解、完整示例代码、练习要求和末尾折叠提示都在里面；
  - `practice.py`：做题时打开，只含题目契约和 `TODO`，不含直接提示；
  - `answer.py`：做完或卡住才打开，答案独立成文件。
  - `test.py` 是后台自动检查文件，不需要阅读。
- 普通章节的示例已内联进 `lesson.md`；只有 3 个“值得单独运行的完整案例”保留 `example.py`（模块导入机制、多模型对比、综合项目）。
- 学习提示统一折叠在每章 `lesson.md` 末尾的 `<details>` 区，默认看不到，卡住再展开。

快速开始与完整说明见 [python-data-analysis/README.md](python-data-analysis/README.md)。在 `python-data-analysis/` 目录下：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
pytest
```

## 二、SQL 练习：`sql-practice/`

### `mysql_beginner_practice/`（主推，MySQL 8.0）

按章节组织，每章一个目录，内部固定为 `lesson.md`（讲解）、`exercises.sql`（练习）、`hints.md`（提示）、`answers.sql`（答案），学习时同样在一个文件夹内完成：

```text
00_setup → 00_diagnostic → 01_select_basics → … → 10_final_practice
→ 11_independent_readiness → 12_python_sql_bridge
```

其中 `12_python_sql_bridge` 与 Python 部分的 `independent_readiness/` 配套，用来把 SQL 导出结果交给 Python 校验，实现两条学习线的衔接。开始前先读 [mysql_beginner_practice/README.md](sql-practice/mysql_beginner_practice/README.md)，术语见同目录 `glossary.md`。

### `sql_beginner_practice/`（SQL Server / T-SQL）

同一套知识点的 SQL Server / T-SQL 版本，按 10 天练习的扁平文件组织（`01_select_basics.sql` … `10_final_practice.sql`，答案在 `answers/`）。使用 DBeaver + 本地 SQL Server 练习，说明见 [sql_beginner_practice/README.md](sql-practice/sql_beginner_practice/README.md)。

## 推荐学习顺序

1. 先学 `sql-practice/mysql_beginner_practice/`（或对应的 T-SQL 版本），掌握查询、聚合、连接与子查询；
2. 再学 `python-data-analysis/` 的 Python 基础与 Pandas；
3. Matplotlib、scikit-learn 按顺序推进；
4. 最后通过 Python 的综合项目与 `12_python_sql_bridge` 把 SQL 和 Python 串起来。

两条线也可以独立学习，不存在强制先后。

## 约定

- 所有练习都在**本地练习数据库 / 练习数据**上进行，严禁连接或修改任何业务数据库。
- SQL 修改类语句默认放在事务中并 `ROLLBACK`；Python 练习只读取 `data/` 样例数据，不改动原始数据。
- 答案用于对照，不建议在独立尝试前直接查看。
