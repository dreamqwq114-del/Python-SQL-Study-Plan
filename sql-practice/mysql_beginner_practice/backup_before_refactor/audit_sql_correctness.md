# MariaDB / MySQL 正确性独立审计报告

## 审计结论

- 审计对象：`mysql_beginner_practice` 当前全部课程、阶段测试、答案、初始化脚本和说明文件。
- 本报告是针对 MariaDB / MySQL 版本的全新审计，没有沿用 SQL Server / T-SQL 审计结论。
- 真实执行环境：
  - 客户端：`D:\xampp\mysql\bin\mysql.exe`
  - 服务端：MariaDB 10.4.32（XAMPP）
  - 地址：`127.0.0.1:3306`
  - 用户：本地 `root`
  - 唯一操作数据库：`sql_beginner_practice`
  - 客户端字符集：`utf8mb4`
- 独立执行结果：
  - `00_create_database.sql` 修复后实际重跑：exit 0，`baseline_status = PASS`。
  - 13 个课程/阶段测试脚本实际执行：全部 exit 0。
  - 13 个答案脚本实际执行：全部 exit 0。
  - 修复后再次执行 `09_data_modification.sql` 和 `answers/09_answers.sql`：均 exit 0。
- 最终结论：未发现尚未修复的严重、一般或建议级 SQL 正确性问题。

## 真实执行范围

### 初始化

- `00_create_database.sql`

### 课程与阶段测试（13 个）

- `00_diagnostic_test.sql`
- `01_select_basics.sql`
- `02_filter_basics.sql`
- `03_sort_date_review.sql`
- `04_aggregate_group.sql`
- `05_inner_join.sql`
- `06_left_join_duplicates.sql`
- `07_case_subquery.sql`
- `08_cte_exists_cast.sql`
- `09_data_modification.sql`
- `10_final_practice.sql`
- `checkpoint_1.sql`
- `checkpoint_2.sql`

### 答案（13 个）

- `answers/00_diagnostic_answers.sql`
- `answers/01_answers.sql` 至 `answers/10_answers.sql`
- `answers/checkpoint_1_answers.sql`
- `answers/checkpoint_2_answers.sql`

## 结构与固定数据核对

- 5 张表按依赖顺序创建：`departments` → `employees` → `projects` → `project_metrics` → `employee_projects`。
- 所有表使用 InnoDB 和 utf8mb4。
- `departments.department_id`、`employees.employee_id`、`projects.project_id`、`project_metrics.metric_id` 是主键。
- `employees.manager_id` 允许 NULL，并正确自关联 `employees.employee_id`。
- `projects.department_id`、`projects.project_manager_id`、`project_metrics.project_id` 的外键目标正确。
- `employee_projects` 正确使用 `(employee_id, project_id)` 联合主键，并分别外键关联员工和项目。
- `project_metrics.project_id` 有 UNIQUE 约束，保证一个项目最多一条指标，支持最终综合题“每项目一行”。
- 通过 `SHOW CREATE TABLE` 在真实数据库中确认了上述主键、唯一键和外键。
- 初始化重跑后的真实行数：
  - departments：5
  - employees：20
  - projects：14
  - project_metrics：12
  - employee_projects：37
- 真实基线还确认：
  - 未参与项目员工：2
  - 无员工参与项目：2
  - 无指标项目：2
  - 员工 19 工资：7200.00
  - 员工 20 工资：5000.00
  - 项目 10 状态：暂停，预算 350000.00
  - 临时部门 96、97、98、99：回滚后均不存在

## MariaDB / MySQL 方言核对

- 可执行查询使用 `LIMIT`，未使用 SQL Server 的 `TOP`；`TOP` 只出现在明确标注的改错题中。
- NULL 显示替换使用 `IFNULL`，未在可执行 SQL 中使用 `ISNULL`。
- CTE 使用 MariaDB 10.4 支持的非递归 `WITH ... AS (...)`。
- 安全类型转换使用 `CASE + REGEXP + CAST`：
  - 先用 REGEXP 验证格式；
  - 只对符合格式的值 CAST；
  - 不符合格式或 NULL 时返回 NULL。
- 第 8 天示例、题 7、题 9及阶段测试 2 的转换写法均在 MariaDB 10.4.32 中实际执行成功。
- 未发现可执行 SQL 中残留 `dbo.`、`GO`、`TRY_CAST` 或 T-SQL 方言。

## 题目与答案核对

- 诊断、第 1～10 天、checkpoint 1、checkpoint 2 的题号与答案完整对应。
- 固定数据支持所有题目，未发现无解题或题目要求的数据不存在。
- 标注的关键行数与真实固定数据一致，包括：
  - 20 名员工、14 个项目、12 条指标、37 条参与关系；
  - 18 名参加过项目的员工、2 名未参加项目的员工；
  - 12 个有参与记录的项目、2 个无参与项目；
  - 2 个无指标项目；
  - 4 个项目状态；
  - 项目 1 有 6 名参与者。
- JOIN 条件均使用正确的主外键，没有在可执行答案中发现漏写 ON 或笛卡尔积。
- 第 6 天题 10 的部门员工计数会保留无项目员工，并避免一名员工多项目导致的重复计数。
- 最终题先按 project_id 聚合参与人数，再 LEFT JOIN 经理和指标，真实执行返回每项目一行。
- `COUNT(*)`、`COUNT(column)`、LEFT JOIN 空扩展行、NULL 和重复计数的解释与答案一致。

## DML 与事务安全核对

- 第 9 天所有实际 UPDATE 和 DELETE 前都有对应 SELECT 预览。
- 所有 UPDATE 和 DELETE 都有精确 WHERE。
- 所有练习修改都在 `START TRANSACTION` 与 `ROLLBACK` 之间。
- 没有可执行的无 WHERE UPDATE / DELETE；危险语句只作为注释中的改错题。
- 修复后，第 9 天课程和答案的所有表引用都写成 `sql_beginner_practice.表名`，即使学习者只选中一个 DML 片段，也不会修改当前连接中的其他数据库同名表。
- 真实执行后确认工资、项目状态、预算和临时部门均恢复固定基线。
- 未发现 `DROP DATABASE`、`DROP TABLE`、存储过程、触发器、游标、动态 SQL、递归 CTE 或窗口函数。

## 本轮问题清单

### 1. 逐段执行第 9 天时，未限定库名可能修改其他数据库同名表

- 文件名：`09_data_modification.sql`；`answers/09_answers.sql`
- 相关位置：两个文件中的全部 INSERT、UPDATE、DELETE 及其预览/核对 SELECT
- 问题说明：原文件开头虽有 `USE sql_beginner_practice` 和 `SELECT DATABASE()`，但第 9 天明确要求逐段选中执行。若学习者只选中中间 DML 片段，而 DBeaver 当前数据库不是练习库，原先未限定库名的语句可能作用于其他数据库中的同名表。`SELECT DATABASE()` 只显示当前库，不能在未被选中执行时提供保护。
- 严重程度：严重
- 修改建议：第 9 天课程和答案中的所有表都使用 `sql_beginner_practice.表名` 完全限定；继续保留事务、预览 SELECT、精确 WHERE 和默认 ROLLBACK。
- 是否已修复：是。两个文件的实际表引用已经全部限定到 `sql_beginner_practice`，并在真实 MariaDB 中重新执行成功。

### 2. 初始化重跑原先不能明确识别额外数据或主键漂移

- 文件名：`00_create_database.sql`
- 相关位置：固定数据事务与脚本末尾基线检查
- 问题说明：`ON DUPLICATE KEY UPDATE` 能更新或补齐固定键，但不会删除额外练习行；`project_metrics` 又同时具有主键和 project_id 唯一键，仅凭 exit 0 不能证明整个数据库仍是固定基线。原注释容易把“可重复执行”理解为“自动恢复完整固定基线”。
- 严重程度：一般
- 修改建议：明确说明脚本不会删除额外行；初始化末尾检查 5、20、14、12、37、指标键对应关系和三类无匹配数量，只有全部满足才显示 PASS。
- 是否已修复：是。脚本已加入 `baseline_status` 检查和停止提示；注释已明确“不会删除额外练习行，不是自动重置”。修复后的实际重跑显示 PASS。

## 历史 APPCRASH 复核

- 已知历史现象：首次初始化脚本为 PRIMARY KEY 显式命名时，MariaDB 10.4.32 的 `mysqld` 曾发生 APPCRASH。
- 当前脚本已移除 PRIMARY KEY 约束名称，保留普通 `PRIMARY KEY (...)` 写法；外键和项目指标唯一约束仍使用明确名称。
- XAMPP MariaDB 重启后，主 Agent 已成功重跑初始化。
- 本次独立审计再次真实重跑当前初始化脚本：exit 0、`baseline_status = PASS`，随后查询仍成功，服务保持可用。
- 以上能确认当前脚本在本次环境中重跑成功；不把单次历史崩溃原因扩大解释为所有 MariaDB 版本的通用结论。

## 数量汇总

- 本轮曾发现严重：1
- 本轮曾发现一般：1
- 本轮曾发现建议：0
- 本轮曾发现合计：2
- 已修复：2
- 未修复严重：0
- 未修复一般：0
- 未修复建议：0
- 当前未修复合计：0

## 已知边界

- `baseline_status` 是查询结果，不会把 mysql 客户端 exit code 改成非 0；学习者必须确认看到 PASS，再开始课程。
- 本报告只验证了本地 `sql_beginner_practice`，没有读取或修改其他数据库。
- 本报告不声称覆盖其他 MariaDB / MySQL 版本、其他 SQL mode 或远程业务服务器。

---

## 第二轮最终正确性复核

### 复核范围与环境

- 复核日期：当前最终文件状态。
- 真实环境：`D:\xampp\mysql\bin\mysql.exe`，MariaDB 10.4.32，`127.0.0.1:3306`，本地 root。
- 唯一读取和执行的数据库：`sql_beginner_practice`。
- 重点文件：
  - `07_case_subquery.sql`
  - `answers/07_answers.sql`
  - `08_cte_exists_cast.sql`
  - `answers/08_answers.sql`
  - `checkpoint_2.sql`
  - `answers/checkpoint_2_answers.sql`
  - `hints.md`
- 本轮只更新本报告，没有修改课程、答案或提示文件。

### 真实执行结果

- `07_case_subquery.sql`：exit 0。
- `answers/07_answers.sql`：exit 0。
- `08_cte_exists_cast.sql`：exit 0。
- `answers/08_answers.sql`：exit 0。
- `checkpoint_2.sql`：exit 0。
- `answers/checkpoint_2_answers.sql`：exit 0。
- 6 个受影响 SQL 文件全部在 MariaDB 10.4.32 中实际执行成功。

### 第 7 天题答复核

- 题 1 要求返回未参与项目的员工 19、20；答案使用 LEFT JOIN 后检查右表主键 NULL，题答一致。
- 题 2 要保留全部 14 个项目和 NULL 经理；答案以项目为左表连接员工，题答一致。
- 新题 3 明确区分 NULL 与空字符串；答案使用 `city IS NULL OR city = ''`，当前固定数据返回 1 行，题面、答案和 `hints.md` 一致。
- 题 8 要求工资高于公司平均值且职位精确为“工程师”；答案使用标量 AVG 子查询和职位条件，固定数据返回 3 行。
- 其余 CASE、IN 子查询、标量子查询和改错题未发现字段、条件、行数或 MariaDB 语法不一致。

### 第 8 天转换复核

- 新示例 4 分别使用 `'123'`、`'10kV'`、`'低压'` 演示成功和失败分支：
  - `'123'` 匹配纯整数 REGEXP，CAST 成功；
  - `'10kV'` 和 `'低压'` 不匹配，CASE 返回 NULL；
  - 实际执行 exit 0。
- 题 7：
  - 先用 REPLACE 去掉 `kV`；
  - 再用 REGEXP 检查整数或小数格式；
  - 符合时 CAST 为 DECIMAL，不符合时返回 NULL；
  - 答案与题面及提示一致。
- 题 9：
  - 先去掉 `kV`；
  - 再检查纯整数格式；
  - `10kV`、`35kV`、`110kV` 转换成功；
  - `380V`、“低压”和 NULL 返回 NULL；
  - 答案与题面一致。
- 对固定 12 条指标的独立复验结果：
  - 总行数：12；
  - 成功转换：6 行；
  - 返回 NULL：6 行；
  - `SHOW WARNINGS` 未返回转换警告。
- `IFNULL`、CTE、EXISTS、NOT EXISTS 的题面和答案均未发现新问题。

### checkpoint 2 复核

- 题 9 已同步改为“去掉 kV 后检查纯整数并转换”。
- 答案使用与第 8 天题 9 相同的 `REPLACE + REGEXP + CASE + CAST` 逻辑。
- 题面所列成功值和失败值与真实执行结果一致。
- 题 1～8、题 10 的 JOIN、计数、CASE、CTE、EXISTS、IFNULL 和 NULL 处理未受此次修改破坏。

### hints.md 对应关系

- 第 7 天题 3 的 NULL / 空字符串三层提示与新题一致。
- 第 8 天题 7、题 9 的 REPLACE、REGEXP、CASE、CAST 提示与答案一致。
- checkpoint 2 题 9 的提示没有泄露完整 SQL，也没有指向旧版“不去掉 kV”的写法。
- 未发现题号错位、旧题残留或答案与提示冲突。

### 第二轮问题与数量

- 新发现严重问题：0。
- 新发现一般问题：0。
- 新发现建议问题：0。
- 第二轮未修复严重：0。
- 第二轮未修复一般：0。
- 第二轮未修复建议：0。
- 第二轮当前未修复合计：0。

### 第二轮结论

最终当前文件中的第 7 天、第 8 天、checkpoint 2、对应答案和 `hints.md` 已通过题答一致性复核；受影响的 6 个 SQL 文件在 MariaDB 10.4.32 中均 exit 0。成功转换、失败返回 NULL 和无警告分支符合题面，未引入新的 SQL 正确性或安全问题。
