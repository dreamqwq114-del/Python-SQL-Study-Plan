# MySQL 8.0 入门复习练习库

这是一套面向 SQL 基础不牢初学者的可运行学习材料。你学过 `SELECT`、`WHERE`、`JOIN`、`GROUP BY` 但容易忘，也可以从诊断开始按顺序复习。

第一次遇到陌生名词时，立即打开根目录 `glossary.md` 查短定义和对应章节，不要带着不理解的术语继续往下读。术语表只用于理解名词，不能代替示例和独立练习。

课程只使用 SQL，不需要 Python、Java 或其他语言。内容止于基础查询、简单子查询、非递归 CTE 和安全事务，不包含窗口函数、存储过程、触发器、游标、递归 CTE、动态 SQL、DBA 或高级调优。

## 数据库和安全边界

- 目标语法：MySQL 8.0；
- 练习数据库：`mysql_beginner_practice`；
- 禁止把脚本中的数据库名改成业务数据库；
- 整套材料不使用 `DROP DATABASE`；
- 第 9 章的修改练习默认 `ROLLBACK`。

本机最终实测环境和版本记录在 `final_audit_summary.md`。如果该文件写着“仅静态审计”或实测环境不是 MySQL 8.0，就不能声称本材料已在真实 MySQL 8.0 中全部运行通过。

历史审计中的日期、服务状态、客户端路径、数据库版本和脚本执行记录只保存在
`final_audit_summary.md`，不能代表本机此刻仍处于相同状态。每次学习前都应重新确认服务、
版本和当前数据库，并运行 `00_setup/verify_database.sql`；只有本次实际输出才能作为当前证据。

## 第一天只做这些

第一天不要一次打开全部章节，只按顺序打开：

1. `00_setup/lesson.md`
2. `00_setup/create_database.sql`
3. `00_setup/verify_database.sql`
4. `00_diagnostic/lesson.md`
5. `00_diagnostic/diagnostic.sql`

完成诊断后再读 `00_diagnostic/review.md`，最后才打开诊断答案。

## 当前学习文件与历史文件

- 当前学习主线：`00_setup/`、`00_diagnostic/`、`01_select_basics/`～
  `12_python_sql_bridge/` 和 `checkpoints/`；
- 学习记录：`progress_tracker.md`、`mistake_log.md` 和 `glossary.md`；
- 维护证据：`audit_*.md` 与 `final_audit_summary.md`，用于了解审计边界，不作为章节练习；
- 历史备份：`backup_before_refactor/` 与 `backup_before_readiness_audit/`，仅用于追溯旧版本，
  不要从中开始学习、运行脚本或填写答案。

如历史文件与当前章节冲突，以当前学习主线、实际数据库结构和本次运行结果为准。

## 普通章节的正确顺序

`lesson.md` → `exercises.sql` → `hints.md` → `answers.sql`

每章必须遵守：

1. 先完整阅读本章 lesson.md。
2. 按顺序阅读并运行 lesson.md 中的每个示例。
3. 每个示例运行前，先回答“运行前预测”。
4. 每次只复制并运行一个示例，不要整章一次执行。
5. 运行后回答“运行后观察”。
6. 完成示例后的“最小修改任务”。
7. 所有示例完成后，才打开 exercises.sql。
8. 每道练习至少独立思考 5～10 分钟。
9. 卡住后先看 hints.md。
10. 全部完成后才打开 answers.sql。
11. 真正做错的题记录到根目录 mistake_log.md。
12. 1～2 天后重新独立完成错题。

不要通过提前看答案来赶时间。如果 60 分钟没有完成，停在当前题，下次继续。

## 每章建议时间：分成学习时段

- `lesson.md` 讲解和示例：20～30 分钟；
- `exercises.sql`：每个练习时段 20～25 分钟；
- 错题整理：5～10 分钟。

一次学习时段控制在 45～60 分钟，但这不等于整章总时长。8 道题若严格按每题至少 5 分钟，练习本身需要至少 40 分钟；加上 lesson 和错题整理，整章通常需要 65～90 分钟。建议分为“lesson + 部分练习”和“剩余练习 + 错题整理”两个时段，而不是减少思考或提前看答案。

## 课程地图

- `01_select_basics`：指定列、别名、去重、计算列、排序与限制；
- `02_filter_basics`：`WHERE` 和常见条件；
- `03_sort_and_dates`：排序、日期、数值和文本条件；
- `04_aggregate_and_group`：聚合、分组和分组后筛选；
- `05_inner_join`：主外键与内连接；
- `06_left_join_and_duplicates`：保留无匹配行与 JOIN 重复；
- `07_case_and_subquery`：分类和简单子查询；
- `08_cte_exists_cast`：非递归 CTE、存在性、转换和空值替代；
- `09_data_modification`：安全的增删改与事务；
- `10_final_practice`：经营分析综合练习；
- `11_independent_readiness`：6 题、90 分钟、无提示的结课独立测评；
- `12_python_sql_bridge`：只读 SQL 导出与 Python 交叉核对；
- `checkpoints`：阶段检查；
- `progress_tracker.md`：学习进度；
- `mistake_log.md`：真正错题和间隔重做。

遇到不熟悉的名词时，先查看根目录 `glossary.md`。术语表用于快速复习，不能代替对应章节的示例和练习。

## 完整学习依赖路线

按以下顺序推进，不要跳过检查点：

1. `00_setup`：建立并验证唯一练习库；
2. `00_diagnostic`：判断哪些基础知识最薄弱；
3. 第 1～4 章：单表读取、筛选、排序、聚合与分组；
4. `checkpoints/checkpoint_1.sql`：检查单表和分组基础；
5. 第 5～8 章：JOIN、重复、NULL、CASE、子查询、CTE 和类型转换；
6. `checkpoints/checkpoint_2.sql`：检查多表和查询组合；
7. 第 9 章：安全的数据修改和事务；
8. 第 10 章：经营分析综合练习；
9. `11_independent_readiness`：不看提示的独立实践测评。

前一阶段没有完成时：

- 不打开下一阶段的答案；
- 把真实错题写入 `mistake_log.md`；
- 1～2 天后独立重做；
- 检查点正确率不足 75% 时，先回到对应章节。

## 在 DBeaver 中连接练习数据库

1. 启动 XAMPP 中的 MySQL 服务，或启动自己的 MySQL 8.0 服务。
2. 在 DBeaver 选择“新建数据库连接”。
3. 按实际服务器选择 MariaDB 或 MySQL：XAMPP 当前通常提供 MariaDB；真实 MySQL 8.0
   服务器才选择 MySQL。
4. 主机通常填 `localhost`，端口通常填 `3306`。
5. 填写自己的用户名和密码。XAMPP 本地默认配置可能使用 `root` 和空密码，但不要假设每台机器都相同。
6. 测试连接。缺少驱动时按所选服务器类型下载对应驱动。
7. 连接成功后新建 SQL 编辑器，再运行 setup 脚本。

## 在 JetBrains IDE 中配置 MySQL 数据源

不要假设历史审计时创建的数据源现在仍存在或仍可连接。可以使用以下名称帮助识别练习库，
但 Driver 和 URL 必须按本机实际运行的数据库选择：

- 名称：`mysql_beginner_practice@localhost`
- Driver：XAMPP 通常是 MariaDB；真实 MySQL 8.0 使用 MySQL；
- URL：MariaDB 通常使用 `jdbc:mariadb://localhost:3306/mysql_beginner_practice`，
  MySQL 8.0 应使用 IDE 生成的 MySQL JDBC URL；
- User：填写本机练习数据库账号；XAMPP 默认配置可能是 `root`，但必须现场确认；
- Port：`3306`

当前使用前必须重新点击 Test Connection，再运行 `SELECT VERSION()`、`SELECT DATABASE()`
和 `00_setup/verify_database.sql`。连接成功不等于已经在真实 MySQL 8.0 中验证全部材料。

如需在另一台电脑重新配置：

1. 打开 Database 工具窗口。
2. 点击 `+`，按实际服务器选择 Data Source → MariaDB 或 MySQL。
3. 填写 Host、Port、User 和 Password。
4. XAMPP 默认通常选择 MariaDB 驱动；真实 MySQL 8.0 服务器选择 MySQL 驱动。
5. 点击 Test Connection。
6. 连接成功后打开 Query Console。
7. setup 完成后，在 Schemas 中勾选 `mysql_beginner_practice` 并刷新。

## 每次先确认当前数据库

单独运行：

```sql
USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;
```

结果不是 `mysql_beginner_practice` 时，不要运行修改语句。

## 只运行当前示例或选中的 SQL

- 每次只选中一条完整语句，包括结尾分号；
- DBeaver 和 JetBrains 通常可用 `Ctrl+Enter` 执行当前语句或选中内容；
- 如果工具准备执行整份文件，先取消，再明确选中一个示例；
- `lesson.md` 中一次只复制一个 SQL 代码块。

## 查看结果表

运行 `SELECT` 后，在结果网格中检查：

- 返回列名和列数；
- 返回行数；
- `NULL` 是否符合题意；
- 是否出现重复；
- 排序方向和并列顺序；
- 无匹配的数据是否被意外漏掉。

不要逐行背答案。验证“结果特征”比记住某一份固定输出更重要。

## 查看错误信息

- 先读错误类型和行号，不要立刻打开答案；
- 检查表名、字段名、逗号、引号和关键字顺序；
- 确认当前数据库；
- 把真正的报错信息和错误 SQL 一起写入 `mistake_log.md`；
- SQL 不报错但结果不对时，也属于错题。

## 为什么运行成功不等于结果正确

以下 SQL 都可能成功执行，却回答错问题：

- 没有 `ORDER BY` 就把 `LIMIT 3` 当成“最高三条”；
- `INNER JOIN` 意外漏掉无匹配记录；
- 一对多 JOIN 后直接计数，导致重复；
- `LEFT JOIN` 后在 `WHERE` 中筛选右表，使无匹配行消失；
- 用 `COUNT(column)` 时忘记它不统计 `NULL`；
- `AND` 和 `OR` 没加括号，条件含义改变。

因此每题都要检查列、行数、`NULL`、重复、排序和无匹配数据。

## 如何使用 hints.md

1. 每题先独立思考 5～10 分钟。
2. 只看“提示 1”，再尝试。
3. 仍卡住才看“提示 2”。
4. 最后才看带省略号的局部结构。
5. 提示仍需要你自己填写字段、条件和排序。

练习题面只保留“卡住后打开 hints.md”的导航，不再重复显示具体 SQL 结构；三级提示集中放在 `hints.md`，独立测评仍然没有提示文件。

## Python–SQL 桥接

完成第 1～10 章和独立测评后，可进入 [`12_python_sql_bridge/`](12_python_sql_bridge/)。先完成无答案的 SQL 查询，把一行一项目结果从客户端导出为 CSV，再交给 Python 项目中的 `independent_readiness/bridge_analysis.py` 做粒度、类型和汇总核对。该任务只读数据库，不使用服务器端文件导出，也不把 `drop_duplicates()` 当作修复 SQL 连接错误的办法。

## 为什么不能直接打开答案

看懂一条 SQL 与独立写出一条 SQL 是两件事。提前看答案会制造“我已经会了”的错觉，并破坏“理解 → 观察 → 模仿 → 独立练习 → 错题重做”的过程。

`answers.sql` 用于核对：

- SQL 是否满足题意；
- 为什么这样写；
- 结果有什么特征；
- 应怎样验证；
- 常见错误是什么。

不要用答案覆盖自己的第一次作答。

## 如何使用 mistake_log.md

- 只有真正做错的题才记录；
- 保留自己的错误 SQL 和实际报错或错误结果；
- 写清楚错误原因，不要只复制正确答案；
- 自己设计一道同类型重做题；
- 1～2 天后不看答案重新完成。

## UPDATE 和 DELETE 为什么必须先 SELECT

`UPDATE` 和 `DELETE` 可能一次影响多行。先用相同 `WHERE` 条件运行 `SELECT`，可以确认目标行和数量。第 9 章统一使用：

1. `SELECT` 预览；
2. `START TRANSACTION`；
3. 执行修改；
4. `SELECT` 验证；
5. 默认 `ROLLBACK`。

无 `WHERE` 的 `UPDATE` 或 `DELETE` 不得实际执行。

## ROLLBACK 与 COMMIT

- `ROLLBACK`：撤销当前事务中尚未提交的修改，练习默认使用；
- `COMMIT`：永久保存当前事务中的修改，只有明确需要保留且验证无误时才使用。

执行 `COMMIT` 后，普通 `ROLLBACK` 不能再撤销已经提交的修改。

## 学完一章后

1. 更新 `progress_tracker.md`；
2. 只记录真正错题；
3. 1～2 天后重做错题；
4. 完成第 4 章后做 `checkpoint_1.sql`；
5. 完成第 8 章后做 `checkpoint_2.sql`；
6. 进入第 9 章事务练习和第 10 章综合项目；
7. 最后独立完成 `11_independent_readiness/assessment.sql`，不要打开答案文件。
8. 通过独立测评后完成 `12_python_sql_bridge/assessment.sql`，再用 Python 检查导出粒度和汇总。
