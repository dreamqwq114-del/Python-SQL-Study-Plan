# MySQL 正确性审计报告

## 审计信息

- 审计轮次：第一轮独立正确性审计；
- 审计范围：`README.md`、`00_setup/`、`00_diagnostic/`、`01_select_basics/` 至 `10_final_practice/`、`checkpoints/`、`mistake_log.md`、`progress_tracker.md`；
- 排除范围：`backup_before_refactor/`、待清理的旧版根目录 SQL 和旧版 `answers/`；
- 目标方言：MySQL 8.0；
- 静态审计结论：未发现 SQL Server 或 PostgreSQL 专有语法混入可运行 SQL；
- 实际执行环境：XAMPP 自带 MariaDB `10.4.32-MariaDB`，客户端为 `D:\xampp\mysql\bin\mysql.exe`；
- 执行边界：只创建和访问 `mysql_beginner_practice`，未访问其他数据库，未执行 `DROP DATABASE`；
- 重要边界：本报告中的实跑结果只证明 MariaDB 10.4.32 兼容运行，不等于真实 MySQL 8.0 实跑。

## 统计汇总

- 严重：0；
- 一般：1；
- 建议：2；
- 第一轮问题合计：3；
- 第一轮问题已修复：0；
- MariaDB 执行单元：67；
- MariaDB SQL 报错：0；
- 执行后基线复核：`PASS`。

## 第一轮问题

### SQL-01：初始化脚本的 PASS 条件允许额外数据

- 文件名：`00_setup/create_database.sql`；
- 章节或题号：脚本末尾 `setup_status`，约第 201～209 行；
- 问题说明：脚本使用 `COUNT(*) >= 固定数量` 判断 `PASS`。如果学习库中存在额外部门、员工、项目或关系行，初始化脚本仍会显示 `PASS`，但紧接着的 `verify_database.sql` 会因为使用精确数量而显示 `FAIL`。两个脚本对“基线合格”的定义不一致，可能让学习者在只看初始化结果时误判数据已恢复为固定基线；
- 严重程度：一般；
- 修改建议：把初始化脚本中的五个数量条件改为精确等于固定基线，或把状态名改为只表示“最低数据已写入”，避免与 `baseline_status` 混用；
- 是否已修复：否。

### SQL-02：`VALUES(column)` 在较新的 MySQL 8.0 中已弃用

- 文件名：`00_setup/create_database.sql`；
- 章节或题号：所有 `ON DUPLICATE KEY UPDATE` 段，约第 86～197 行；
- 问题说明：`VALUES(column)` 在 MySQL 8.0 中仍可执行，但从 MySQL 8.0.20 起已标记为弃用。MariaDB 10.4.32 实测没有报错；这不是当前语法错误，但未来 MySQL 版本可能移除；
- 严重程度：建议；
- 修改建议：若只以较新的 MySQL 8.0 为目标，可改为 MySQL 支持的行别名写法；若继续兼容当前 XAMPP MariaDB，应保留现写法并在 setup 说明中标注“有效但在较新 MySQL 8.0 中会有弃用提示”；
- 是否已修复：否。

### SQL-03：`information_schema.tables.table_rows` 对 InnoDB 是估算值

- 文件名：`00_setup/verify_database.sql`；
- 章节或题号：表清单查询，约第 5～12 行；
- 问题说明：`information_schema.tables.table_rows` 对 InnoDB 通常是估算值，不适合当作精确基线。当前脚本后面已经使用 `COUNT(*)` 做精确检查，因此不会造成最终 PASS 误判，但初学者可能把前一张结果表的 `table_rows` 当作精确行数；
- 严重程度：建议；
- 修改建议：把列别名改为 `estimated_rows` 并加一条短注释，或只在表清单中显示 `table_name`，精确行数统一看后面的 `COUNT(*)`；
- 是否已修复：否。

## 已通过的静态检查

### 方言与数据库边界

- 在新结构的可运行 SQL 中未发现 `TOP`、`TRY_CAST`、`GETDATE()`、`IDENTITY`、`sys.tables`、`sys.columns`、`BEGIN TRANSACTION`、PostgreSQL `RETURNING`、`ILIKE` 或 `::` 类型转换；
- 使用了 MySQL 形式的 `LIMIT`、`CAST`、`START TRANSACTION`、`information_schema`；
- 没有可执行的 `DROP DATABASE` 或 `DROP TABLE`；
- 所有新结构 SQL 文件都包含 `USE mysql_beginner_practice;`；
- 第 9 章的可执行修改语句均使用专用练习编号、明确 `WHERE` 和事务，默认 `ROLLBACK`；
- 无 `WHERE` 的危险 `UPDATE` 只存在于注释中的改错题，明确标注“严禁实际执行”。

### 建表、约束和固定数据

- 建表顺序正确：`departments` → `employees` → `projects` → `project_metrics` → `employee_projects`；
- 外键引用的父表在子表之前创建；
- `employees.manager_id` 自关联的首行先单独插入，再插入其余员工；
- 五张表字段名与全部示例、练习答案一致；
- 固定数据基线实测为：部门 5、员工 20、项目 14、项目指标 12、员工项目关系 37；
- 特意保留的数据边界实测成立：1 个部门城市为 `NULL`、6 个项目结束日期为 `NULL`、1 个项目无经理、2 名员工无参与项目、2 个项目无参与人员、2 个项目无指标；
- 固定数据能够支持 `NULL`、无匹配、INNER JOIN 丢行、LEFT JOIN 保留、一对多行数增加和重复计数等练习。

### 示例、练习和答案对应

- 第 1～10 章每章有 5 个正式可运行示例，共 50 个；
- 第 1～10 章每章有 8 道正式练习和 8 份对应参考答案，共 80 对；
- 第 1～10 章每章有 5 个最小修改任务和 5 份对应答案，共 50 对；
- 两个 checkpoint 均为 6 题，答案一一对应；
- `00_diagnostic` 的 8 道诊断题与 8 份答案一一对应；
- 所有正式示例 SQL、诊断答案、章节答案和 checkpoint 答案在 MariaDB 10.4.32 中执行时均无 SQL 报错；
- 练习文件保留作答空白，未将未完成 SQL 当作可执行答案测试。

### JOIN、重复和 NULL

- INNER JOIN 均有明确 `ON` 条件，未发现遗漏条件造成的笛卡尔积；
- 三表连接均按主键与外键逐级连接；
- 一对多计数使用了正确粒度：需要项目唯一数时使用 `COUNT(DISTINCT p.project_id)`，需要参与关系数时使用 `COUNT(ep.employee_id)`；
- LEFT JOIN 统计无匹配行时使用右表非空键计数，未使用会把空占位行计入的 `COUNT(*)`；
- LEFT JOIN 后限制右表为 110kV 的改错答案把条件放在 `ON` 中，保留全部项目；
- `COUNT(*)` 与 `COUNT(column)` 的差异、聚合函数忽略 `NULL`、`IS NULL`、`IS NOT NULL` 均使用正确；
- `EXISTS` 和 `NOT EXISTS` 子查询均与外层主键正确关联。

### 排序、分组、子查询和类型

- “最高/最低/前几条”答案均在 `LIMIT` 前给出明确 `ORDER BY`；
- 需要稳定顺序的主要查询提供了并列排序键；
- `WHERE` 用于分组前筛选，`HAVING` 用于聚合后筛选；
- 所有非聚合输出列都满足 MySQL 8.0 `ONLY_FULL_GROUP_BY` 规则；
- 标量子查询均保证一行一列；
- 非递归 CTE、`CAST(... AS CHAR)`、`COALESCE` 的用法符合 MySQL 8.0 范围；
- 未发现递归 CTE、窗口函数、存储过程、触发器、游标或动态 SQL。

## MariaDB 10.4.32 实际执行记录

执行单元按“一个示例代码块或一份完整 SQL 文件”计数：

- `00_setup/create_database.sql`：1 次，0 错误；
- `00_setup/verify_database.sql`：初始化后和全部测试后各 1 次，共 2 次，0 错误；
- 第 1～10 章 lesson 正式示例：50 个，0 错误；
- `00_diagnostic/diagnostic.sql` 与 `00_diagnostic/answers.sql`：2 份，0 错误；
- 第 1～10 章 `answers.sql`：10 份，0 错误；
- 两份 checkpoint 答案：2 份，0 错误。

合计 67 个执行单元，SQL 报错 0。全部测试完成后再次运行 `verify_database.sql`，`baseline_status` 为 `PASS`，说明第 9 章事务答案没有把临时数据留在学习库中。

## MySQL 8.0 审计边界

- 本轮对 MySQL 8.0 做了完整静态方言审计；
- 本机未发现可用的 MySQL 8.0 服务或客户端实例；
- XAMPP 实际服务是 MariaDB 10.4.32；
- 因此不能声称“已在真实 MySQL 8.0 中全部运行通过”；
- 最终交付仍应把这一限制写入 `final_audit_summary.md`。

## 第一轮结论

未发现严重问题。发现 1 个一般问题和 2 个建议问题，第一轮均尚未修复。一般问题应在交付前修复；两条建议可由主 Agent 根据“纯 MySQL 8.0”与“继续兼容本机 MariaDB 实测”的取舍决定是否采纳。

# 第二轮复核

## 复核信息

- 复核目标：确认第一轮问题是否真正处理、教学修复是否引入 SQL 问题、示例与最小修改答案是否仍一致、练习与答案是否一一对应、表名字段名和固定数据是否一致、第 9 章事务是否仍安全；
- 复核环境：XAMPP MariaDB `10.4.32-MariaDB`；
- MySQL 8.0 边界：继续只做静态方言复核，没有真实 MySQL 8.0 实例可运行；
- 数据库边界：只使用 `mysql_beginner_practice`，未访问其他数据库，未执行 `DROP DATABASE`。

## 第一轮问题最终状态

### SQL-01：初始化脚本的 PASS 条件允许额外数据

- 最终状态：已修复；
- 复核证据：`00_setup/create_database.sql` 的五个基线数量条件已由 `>=` 改为精确 `=`；
- 一致性检查：该条件现在与 `00_setup/verify_database.sql` 的精确基线定义一致；
- 回归结果：修改后的初始化脚本和验证脚本在 MariaDB 10.4.32 中均执行成功，`setup_status` 与 `baseline_status` 均为 `PASS`；
- 新问题：未发现。

### SQL-02：`VALUES(column)` 在较新的 MySQL 8.0 中已弃用

- 最终状态：建议未采纳，保留现有写法；
- 原因复核：理由合理。`VALUES(column)` 在 MySQL 8.0 中仍是有效语法，只是从 8.0.20 起弃用；当前 XAMPP MariaDB 10.4.32 实测支持它，而改成较新 MySQL 的行别名写法会失去当前 MariaDB 10.4 的兼容实测能力；
- 当前影响：不会造成现有 MySQL 8.0 语法错误，也没有导致 MariaDB 实测错误；
- 后续限制：未来升级到移除该语法的 MySQL 版本时，需要再改写初始化脚本；
- 最终计数：保留为 1 条未解决“建议”，不是严重或一般问题。

### SQL-03：`information_schema.tables.table_rows` 是估算值

- 最终状态：已修复；
- 复核证据：`00_setup/verify_database.sql` 的表清单现在只显示 `table_name`；精确行数统一由后续五条 `COUNT(*)` 查询给出；
- 回归结果：修改后的验证脚本执行成功，五张表名称、精确行数和最终基线状态均正确；
- 新问题：未发现。

## 教学修复后的对应关系

- 第 1 章现有 6 个正式示例，对应 6 个最小修改答案；
- 第 2 章现有 7 个正式示例，对应 7 个最小修改答案；
- 第 6 章现有 6 个正式示例，对应 6 个最小修改答案；
- 其余七章各有 5 个正式示例和 5 个最小修改答案；
- 全课程合计 54 个正式示例和 54 个最小修改答案，编号与任务内容一一对应；
- 第 1～10 章仍各有 8 道正式练习和 8 份答案，合计 80 对，编号无缺失、无重复；
- 新增的 `SELECT *`、拆分后的 `IN`、`BETWEEN`、`LIKE`、LEFT JOIN 右表条件对比示例均使用现有真实字段；
- 第 1、2、6 章修改后的 lesson 示例与 answers 中对应 SQL 均实际执行成功；
- 未发现示例修改后答案仍停留在旧编号或旧题意的情况。

## 表、字段、JOIN 和事务复核

- 五张表及其字段与 54 个示例、80 份练习答案、两份 checkpoint 答案保持一致；
- 建表顺序和外键依赖未改变；
- 新增示例未引入错误连接条件、笛卡尔积或不正确计数；
- 第 6 章新增的两条 LEFT JOIN 对比查询含义正确：`WHERE` 版本只保留匹配行，`ON` 版本保留所有左表项目；
- 所有 GROUP BY 查询仍符合 MySQL 8.0 `ONLY_FULL_GROUP_BY` 规则；
- 第 9 章所有可执行 `UPDATE`、`DELETE` 仍使用明确 `WHERE`、修改前预览、事务内验证和默认 `ROLLBACK`；
- 第 9 章完整答案复跑后，固定基线仍为 `PASS`，没有残留专用练习行；
- 无 WHERE 的危险更新仍只存在于注释改错题中，没有变成可执行示例。

## 第二轮实际执行

按“一个正式示例代码块或一份完整 SQL 文件”为一个执行单元：

- 修改后的 `create_database.sql`：1 个；
- 修改后的 `verify_database.sql`：初始化后和全部测试后各 1 个，共 2 个；
- 第 1～10 章正式示例：54 个；
- 诊断 SQL 与诊断答案：2 个；
- 第 1～10 章完整 answers：10 个；
- 两份 checkpoint 答案：2 个。

第二轮共执行 71 个单元，SQL 报错 0。测试结束后额外查看验证结果：

- `departments`：5；
- `employees`：20；
- `projects`：14；
- `project_metrics`：12；
- `employee_projects`：37；
- `baseline_status`：`PASS`。

## 第二轮新问题

未发现第二轮新增的严重、一般或建议问题。

## 第二轮最终结论

- 第一轮严重问题：0，最终未解决 0；
- 第一轮一般问题：1，已修复 1，最终未解决 0；
- 第一轮建议问题：2，已采纳并修复 1，合理不采纳 1；
- 第二轮新增问题：0；
- 最终未解决计数：严重 0、一般 0、建议 1；
- 当前唯一保留建议是较新 MySQL 8.0 对 `VALUES(column)` 的弃用提示，不影响当前 MySQL 8.0 有效语法判断或 MariaDB 10.4.32 实测运行；
- MySQL 8.0 仍然仅完成静态方言复核，不能声称在真实 MySQL 8.0 中全部运行通过。
