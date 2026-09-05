# 第三轮：运行环境、SQL 正确性与独立测评有效性审计

## 审计身份与范围

- 审计角色：独立运行环境、SQL 正确性与独立测评有效性审计员；
- 审计目录：`mysql_beginner_practice/` 当前第三轮版本；
- 排除目录：`backup_before_refactor/`、`backup_before_readiness_audit/`；
- 实际执行边界：只使用 `mysql_beginner_practice`；
- 禁止操作检查：未执行 `DROP DATABASE`，未访问或修改其他数据库；
- 审计环境：XAMPP MariaDB `10.4.32-MariaDB`，端口 `3306`；
- 执行工具：`D:\xampp\mysql\bin\mysql.exe`；
- 重要边界：这证明材料在 MariaDB 10.4.32 中实跑通过，同时完成了 MySQL 8.0 静态方言检查；不能据此声称已在真实 MySQL 8.0 服务端实跑。

## 一、数据库结构与固定数据

实际读取 `information_schema.columns` 和 `information_schema.table_constraints` 后确认：

- `departments`：3 列，主键 `department_id`；
- `employees`：7 列，主键 `employee_id`，含部门外键和经理自引用外键；
- `projects`：8 列，主键 `project_id`，含部门外键和项目经理外键；
- `project_metrics`：5 列，主键 `metric_id`，`project_id` 唯一且引用项目；
- `employee_projects`：4 列，`employee_id + project_id` 复合主键，并分别引用员工和项目；
- 建表顺序符合外键依赖；
- 表名、字段名、主键、外键、可空字段与 lesson、练习及答案中的用法一致。

固定基线实测：

| 表 | 行数 |
|---|---:|
| `departments` | 5 |
| `employees` | 20 |
| `projects` | 14 |
| `project_metrics` | 12 |
| `employee_projects` | 37 |

`verify_database.sql` 返回 `PASS`。第 9 章答案运行后、第 11 章答案运行后以及严格模式复跑结束后，固定基线均再次返回 `PASS`。

## 二、MySQL 8.0 静态方言审计

扫描了排除备份目录后的 30 个 `.sql` 文件。

以下模式在可执行 SQL 中的命中数均为 0：

- SQL Server：`TOP`、`TRY_CAST`、`GETDATE()`、`IDENTITY`、`sys.tables`、`sys.columns`、`BEGIN TRANSACTION`；
- PostgreSQL：`RETURNING`、`ILIKE`、`::类型`；
- 危险或越界：`DROP DATABASE`、`DROP TABLE`、旧库名 `sql_beginner_practice`、指向其他数据库的 `USE`；
- 无条件修改：没有发现可执行的无 `WHERE` `UPDATE` 或 `DELETE`。

材料使用的 `LIMIT`、`CAST`、`NOW()`、`START TRANSACTION`、`information_schema`、非递归 `WITH`、`COALESCE`、`EXISTS` 等均属于 MySQL 8.0 可用语法。

另外使用以下严格会话模式重新执行全部 lesson 示例和全部参考答案：

```sql
STRICT_TRANS_TABLES,
ERROR_FOR_DIVISION_BY_ZERO,
NO_ENGINE_SUBSTITUTION,
ONLY_FULL_GROUP_BY
```

严格模式共执行 68 个单元，结果为 `68 PASS / 0 FAIL`，未发现被宽松分组规则掩盖的错误。

## 三、实际运行结果

第一轮逐单元执行结果：

| 类别 | 数量 | 结果 |
|---|---:|---|
| setup 与 verify | 2 | 2 PASS |
| 第 1～10 章 lesson 可运行示例 | 54 | 54 PASS |
| diagnostic、第 1～10 章、两个 checkpoint、第 11 章参考答案文件 | 14 | 14 PASS |
| 第 9 章后固定基线 | 1 | PASS |
| 第 11 章后固定基线 | 1 | PASS |
| 合计 | 72 | 72 PASS / 0 FAIL |

结构配对检查：

- 第 1～10 章均为 8 道正式练习和 8 个练习答案；
- 80 道正式练习与 80 个答案节一一对应；
- 54 个 lesson 最小修改任务与 54 个答案节一一对应；
- 第 11 章 6 道测评题与 6 个答案节一一对应；
- 全部答案在实际数据库中无语法报错；
- JOIN 使用了明确连接条件，未发现答案中的无意笛卡尔积；
- 一对多统计题使用分组或 `COUNT(DISTINCT ...)` 控制重复；
- `COUNT(*)`、`COUNT(column)`、`IS NULL`、`COALESCE` 的使用符合题意；
- 第 9 章和第 11 章的修改答案均在事务内执行，`UPDATE`、`DELETE` 均有精确 `WHERE`，教学修改默认回滚。

## 四、IDEA 数据源配置证据

静态检查了：

- `C:\Users\12086\Desktop\IOM103_Python_Data_Analysis\.idea\dataSources.xml`
- `C:\Users\12086\Desktop\IOM103_Python_Data_Analysis\.idea\dataSources.local.xml`

确认旧连接被保留：

- 名称：`sql_beginner_practice@localhost`
- UUID：`7ede2bca-84c3-444f-8e23-693424d6046a`
- URL：`jdbc:mariadb://localhost:3306/sql_beginner_practice`

确认新增连接存在且配置一致：

- 名称：`mysql_beginner_practice@localhost`
- UUID：`07c51abc-52c1-46b0-89fd-44762b2190f3`
- Driver：`mariadb`
- JDBC Driver：`org.mariadb.jdbc.Driver`
- URL：`jdbc:mariadb://localhost:3306/mysql_beginner_practice`
- User：`root`
- 配置记录的 DBMS：MariaDB `10.4.32`
- 配置记录的驱动：MariaDB Connector/J `3.5.7`，JDBC `4.2`

本独立审计角色核实了配置文件与命令行数据库，不把 XML 静态证据表述成 IDEA 界面实跑证据。IDEA “测试连接”界面和查询结果表仍应由主 Agent 的界面实测记录负责。

## 五、第 11 章独立测评验收

结构和规则检查结果：

- 目录内只有 `README.md`、`assessment.sql`、`rubric.md`、`answers.sql`，没有 `hints.md`；
- 共 6 题，总分精确为 100 分；
- 限时 90 分钟；
- 通过线 80 分；
- 第 6 题设置独立安全门槛；
- 未提交实际作答时，结论明确限定为“材料具备独立实践闭环，个人能力尚未验证”；
- `assessment.sql` 只有业务目标、返回列或结果特征、验证要求和空白作答区域；
- `assessment.sql` 没有字段拼装式提示、局部 SQL 骨架或参考答案；
- `rubric.md` 只给评分点，没有 SQL 结构；
- 6 个参考答案均在实际数据库运行通过；
- 第 6 题参考答案先确认数据库和目标行，再在事务内插入、预览、更新、验证、预览、删除、验证，最后 `ROLLBACK`；
- 第 11 章答案运行后 `department_id = 9301` 不存在，固定基线为 `PASS`。

测评覆盖情况：

1. 单表筛选、`NULL` 与稳定排序：已覆盖；
2. 聚合、`GROUP BY`、`HAVING` 与非空计数：已覆盖；
3. 三表 `INNER JOIN`：已覆盖；
4. `LEFT JOIN`、无匹配数据与重复计数：已覆盖；
5. `CASE`、标量子查询、非递归 CTE、`COALESCE`：已覆盖；
6. 修改前预览、事务、验证、`ROLLBACK`：已覆盖。

## 六、第一轮发现的问题

### 问题 1

- 文件或章节：`11_independent_readiness/assessment.sql` 第 4 题、`11_independent_readiness/answers.sql` 第 4 题；
- 问题说明：当前固定数据中，恰好只有项目 13、14 没有参与人员，也恰好只有项目 13、14 没有项目指标。因此把正确条件 `没有参与人员 OR 没有指标` 错写成 `没有参与人员 AND 没有指标`，实际仍返回完全相同的项目 `13,14`。评分者阅读 SQL 时可以识别错误，但学习者仅靠结果特征无法发现逻辑错误；
- 严重程度：一般；
- 修改建议：在不改固定基线的前提下，把第二个缺失条件改为现有数据能够形成“只缺一项”反例的指标，例如“没有参与人员或投资收益率为空”；相应显示“收益率已填/收益率缺失”，并同步修改评分规则和参考答案。当前数据中项目 12 有参与人员但收益率为空，可区分 `OR` 与 `AND`；
- 是否已修复：否（本独立角色按要求只写审计报告，不修改教材）。

### 问题 2

- 文件或章节：`00_setup/create_database.sql` 的 `ON DUPLICATE KEY UPDATE`；
- 问题说明：`VALUES(column)` 在 MySQL 8.0.20 起被标记为弃用，但在 MySQL 8.0 系列仍可用；当前写法同时兼容本机 MariaDB 10.4.32，实际运行无误；
- 严重程度：建议；
- 修改建议：保留当前跨 MySQL/MariaDB 可运行写法，并在最终限制中记录弃用警告；如果将来只面向较新的真实 MySQL 8.0，再按目标小版本改为行别名写法并重新实跑；
- 是否已修复：否。

## 七、问题计数

第一轮：

- 严重：0；
- 一般：1；
- 建议：1；
- 合计：2。

## 八、第一轮结论

- 运行环境：XAMPP MariaDB 服务、练习库、五张表、固定数据和命令行执行环境均已就绪；
- SQL 正确性：当前示例和参考答案在 MariaDB 10.4.32 中全部实跑通过，MySQL 8.0 静态方言及严格分组检查通过；
- IDEA：配置文件证明旧连接被保留且新连接参数完整；本角色没有把静态配置冒充为 IDEA 界面验证；
- 独立测评：分值、时长、通过线、安全门槛、无提示设计和参考答案均成立；
- 待修复项：第 4 题需要一个能够区分 `OR` 与 `AND` 的数据反例或题目条件；
- 能力结论：材料已经提供独立实践入口，但在学习者提交并通过实际作答前，不能判断其本人已能独立完成实践；
- 环境边界：未在真实 MySQL 8.0 服务端实跑，只有 MariaDB 10.4.32 实跑和 MySQL 8.0 静态审计。

## 九、第二轮复核

### 复核对象

主 Agent 已针对第一轮“一般”问题同步修改：

- `11_independent_readiness/assessment.sql` 第 4 题；
- `11_independent_readiness/rubric.md` 第 4 题评分点；
- `11_independent_readiness/answers.sql` 第 4 题参考答案。

第二轮重点复核题面、评分点、答案、实际结果、重复计数、`NULL` 判断、提示泄漏和事务后基线。

### 第一轮问题 1 复核

- 原问题：正确的 `OR` 与错误的 `AND` 在原固定数据中返回同样结果；
- 修改结果：题目现在要求返回“没有参与人员”或“投资收益率为空”的项目，并显示 `participant_count` 与 `roi_status`；
- 题面与评分一致：评分规则明确检查不重复人数、收益率缺失状态、`OR` 条件、无重复和排序；
- 答案与题面一致：
  - `LEFT JOIN employee_projects` 保留无人参与的项目；
  - `LEFT JOIN project_metrics` 保留没有指标行的项目；
  - `COUNT(DISTINCT ep.employee_id)` 控制一对多连接造成的重复计数；
  - `MAX(pm.investment_return_rate) IS NULL` 同时识别没有指标行和收益率字段为空；
  - `HAVING ... = 0 OR ... IS NULL` 与业务条件一致；
- MariaDB 实测结果：

| project_id | participant_count | roi_status |
|---:|---:|---|
| 12 | 1 | 收益率缺失 |
| 13 | 0 | 收益率缺失 |
| 14 | 0 | 收益率缺失 |

- 反例有效性：
  - 正确 `OR` 返回 `12,13,14`；
  - 错误 `AND` 只返回 `13,14`；
  - 项目 12 构成“有参与人员但收益率缺失”的独立反例，学习者现在能通过结果发现逻辑错误；
- 修复是否引入新问题：未发现；
- 最终状态：已修复。

### 无提示泄漏复核

- `assessment.sql` 仍为 6 题；
- 去除注释后，文件只有 `USE mysql_beginner_practice;` 和 `SELECT DATABASE()`，六个作答区均为空；
- 题面没有 `SELECT ... FROM ...` 局部骨架、连接字段拼装或参考 SQL；
- 第 4 题增加的是可验证结果特征，没有泄露 `LEFT JOIN`、聚合表达式或完整条件写法；
- 目录内仍不存在 `hints.md`；
- `rubric.md` 只有评分维度，没有参考 SQL。

### 答案与基线复跑

- `11_independent_readiness/answers.sql`：MariaDB 10.4.32 实跑退出码 0；
- 同一答案在 `ONLY_FULL_GROUP_BY` 等严格模式下复跑：退出码 0；
- 第 4 题每个项目一行，项目 12 的人数为 1，项目 13、14 的人数为 0，无错误重复；
- `MAX(pm.investment_return_rate) IS NULL` 正确处理项目指标不存在和收益率字段为 `NULL` 两种情况；
- 第 6 题仍以 `ROLLBACK` 结束；
- 答案复跑后的五表固定基线：`PASS`。

### 第一轮问题 2 决定

- `VALUES(column)` 建议不修改；
- 原因：当前写法在 MariaDB 10.4.32 实跑通过，在 MySQL 8.0 中仍可运行但较新小版本会给弃用提示；直接改为 MySQL 新行别名写法会降低与当前 XAMPP MariaDB 的兼容性；
- 处理方式：作为已知兼容性限制保留，不属于当前语法错误；
- 最终状态：未采纳修改，保留为建议。

## 十、第二轮计数与最终状态

第二轮复核结果：

- 复核第一轮问题：2；
- 已修复：1；
- 合理保留为已知限制：1；
- 新发现严重：0；
- 新发现一般：0；
- 新发现建议：0。

最终未解决计数：

- 严重：0；
- 一般：0；
- 建议：1；
- 合计：1。

## 十一、第二轮最终结论

- 第一轮唯一“一般”问题已真正修复，修改未引入新的 SQL、重复或 `NULL` 处理问题；
- 第 11 章题面、评分规则和参考答案一致；
- 结课答案在 MariaDB 10.4.32 和严格分组模式下均运行通过；
- 第 11 章执行后固定基线保持 `PASS`；
- 测评仍为 6 题、100 分、90 分钟、80 分通过，并保留第 6 题安全门槛；
- 没有 `hints.md`，作答文件没有答案或 SQL 骨架泄漏；
- 当前环境与材料可以直接用于练习和测评；
- 仍需保留的唯一建议是 `VALUES(column)` 的 MySQL 新版本弃用提示；
- 未在真实 MySQL 8.0 服务端实跑的边界不变；
- 学习者未提交实际测评作答前，个人独立实践能力仍应标记为“尚未验证”。
