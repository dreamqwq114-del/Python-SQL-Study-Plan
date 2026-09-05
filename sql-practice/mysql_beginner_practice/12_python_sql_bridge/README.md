# Python–SQL 桥接实践

本目录把 SQL 查询结果交给 Python 做第二次检查。目标不是比较哪种语言更好，而是训练“先明确数据粒度，再交叉验证结果”的工作流。

## 前置条件

- 完成第 1～10 章和 `11_independent_readiness`；
- `00_setup/verify_database.sql` 显示 `PASS`；
- 当前数据库必须是 `mysql_beginner_practice`；
- 本目录没有 `hints.md` 或参考答案，建议限时 60 分钟。

## 工作流

1. 复制 `assessment.sql` 为自己的作答文件，只填写空白位置。
2. 分别运行三个 `SELECT`，先检查列数、行数、重复和 `NULL`。
3. 在 IntelliJ IDEA 或其他数据库客户端中把第 1 题结果导出为 `project_analysis.csv`，不要使用服务器端 `INTO OUTFILE`。
4. 把 CSV 放到 Python 项目的 `independent_readiness/`，复制 `bridge_analysis.py` 为 `submission_bridge.py` 并完成 Python 检查。
5. 记录 SQL 与 Python 的项目数、状态分布和预算合计；不一致时回到连接粒度排查。

## 安全边界

- 只读查询，不修改数据库；
- 不允许为消除重复直接 `drop_duplicates()`，必须先证明 SQL 结果是一行一项目；
- 不要把 SQL 结果当成“已经正确”，Python 端仍需验证列类型、唯一性和无参与项目是否存在。

## 交付物

- SQL 作答文件；
- `project_analysis.csv`；
- Python 桥接脚本及终端输出；
- 一段简短说明：SQL 的粒度是什么、Python 如何验证它、若不一致优先检查什么。

