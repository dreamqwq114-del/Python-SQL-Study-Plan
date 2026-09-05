# MariaDB / MySQL 教学质量最终复审

## 最终结论

本轮独立复审了：

- `README.md`
- 诊断、10 天课程和两份阶段测试
- `hints.md`、`diagnostic_review.md`、`mistake_log.md`
- `answers/` 下全部答案
- `audit_sql_correctness.md`、`final_audit_summary.md`

首轮 MY-TQ-01～09 已全部修复。`audit_sql_correctness.md` 与 `final_audit_summary.md` 现在均为 MariaDB / MySQL 版本，执行环境、回归数量、数据库确认语句和第一天顺序前后一致。

本轮未发现新的课程教学问题。本报告只更新审计状态，没有修改其他文件。

## 首轮问题逐项复审

### MY-TQ-01：审计文档与 MariaDB 课程冲突

- 对应课程或文件：`audit_sql_correctness.md`、`final_audit_summary.md`
- 原问题说明：审计文档使用 SQL Server / T-SQL、`sqlcmd`、`DB_NAME()` 等旧结论，并与 README 记录的 MariaDB 实际执行背景冲突。
- 当前复审证据：
  - `audit_sql_correctness.md` 已完整改为 MariaDB / MySQL 报告，记录了 XAMPP MariaDB 10.4.32、`mysql.exe`、`127.0.0.1:3306`、实际执行范围、exit 0、固定基线和事务回滚验证。
  - `final_audit_summary.md` 已改为 MariaDB / MySQL 总结，记录 MariaDB 10.4.32、`mysql.exe`、`127.0.0.1:3306` 和 utf8mb4。
  - 最终总结明确记录初始化 1 个、课程与阶段测试 13 个、答案 13 个，共 27 个 SQL 文件全量回归，失败 0。
  - 第一日顺序已使用 `USE sql_beginner_practice;` 和 `SELECT DATABASE();`，并要求先确认 `baseline_status = PASS`。
  - 最终总结的问题数量为严重 2、一般 6、建议 3，共 11 项，与 MariaDB 正确性审计 2 项及本教学审计 9 项相符。
- 对初学者的影响：修复后适用数据库、真实执行证据和第一天操作一致，学习者不会再被 SQL Server 旧说明误导。
- 严重程度：严重
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-02：第 8 天概念密度高且正则符号缺少解释

- 对应课程或文件：`08_cte_exists_cast.sql`
- 原问题说明：同一天包含 CTE、EXISTS、CASE、REGEXP、CAST、IFNULL 等内容，且未解释正则符号。
- 当前复审证据：
  - 已明确拆成两个 20～30 分钟学习段：第一段练 CTE/EXISTS，第二段练 REGEXP/CAST/IFNULL。
  - 已解释 `^`、`$`、`[0-9]+` 和 `?`。
  - 已明确复杂小数正则可以直接套用，不要求背诵。
- 对初学者的影响：修复后学习边界更清楚，可以先理解“有没有”，再理解“先验证、后转换”，不必一次记住全部符号。
- 严重程度：一般
- 修改建议：无需继续修改；实际学习时仍应按文件建议分两段完成。
- 是否已修复：是

### MY-TQ-03：MariaDB `CAST` 失败行为在课程与提示中不一致

- 对应课程或文件：`08_cte_exists_cast.sql`、`hints.md`、`answers/08_answers.sql`
- 原问题说明：课程说明无效转换可能返回 0 并产生警告，提示却沿用“CAST 会报错”的 SQL Server 心智模型。
- 当前复审证据：三处均已统一说明直接 `CAST` 可能返回 0 并产生警告；提示明确要求先处理文本，再通过 `REGEXP`、`CASE` 和 `CAST` 让失败结果为 NULL。
- 对初学者的影响：修复后不会再误找 MariaDB 版 `TRY_CAST`，能够理解安全转换是一个组合步骤。
- 严重程度：一般
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-04：转换练习与阶段测试只有失败分支

- 对应课程或文件：`08_cte_exists_cast.sql`（题 9）、`checkpoint_2.sql`（题 9）及对应答案
- 原问题说明：原题直接检查纯整数，但固定电压数据没有纯整数字符串，导致转换结果全部为 NULL。
- 当前复审证据：
  - 课程题 9和阶段测试题 9都先移除 `kV`，再检查纯整数并转换。
  - 题目明确给出成功分支：`10kV`、`35kV`、`110kV`。
  - 题目明确给出失败/空值分支：`380V`、`低压` 和 NULL。
  - 两份答案均使用 `REPLACE + REGEXP + CASE + CAST` 完成上述目标。
- 对初学者的影响：修复后可以同时观察成功、失败和 NULL，错误的成功分支不再被“全是 NULL”掩盖。
- 严重程度：一般
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-05：第 8 天题 7原样复制示例，提示过度接近答案

- 对应课程或文件：`08_cte_exists_cast.sql`（示例 4、题 7）、`hints.md`
- 原问题说明：示例和题 7原来处理同一张表、同一列和同一流程，学习者只需复制。
- 当前复审证据：
  - 示例 4已改为 `'123'`、`'10kV'`、`'低压'` 三个独立字面量，让学习者先预测正则和转换结果。
  - 题 7再把相同思路应用到真实的 `project_metrics.voltage_level`。
  - 提示只给函数顺序，没有给出完整 SELECT、字段组合或正则答案。
- 对初学者的影响：修复后形成“短例理解规则 → 真实列迁移应用”的两步练习，不再是原样抄写。
- 严重程度：一般
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-06：第 5～8 天部分复习题缺少返回列或预计结果

- 对应课程或文件：`05_inner_join.sql`、`06_left_join_duplicates.sql`、`07_case_subquery.sql`、`08_cte_exists_cast.sql`
- 原问题说明：若干旧知题没有同时给出返回列、行数或关键结果特征。
- 当前复审证据：
  - 第 5 天旧知题 2已补 `department_id、average_salary；预计 3 行`。
  - 第 6 天旧知题 3已补 `project_name、budget、end_date；6 行，end_date 均为 NULL`。
  - 第 7 天旧知题 1～2已补返回列、行数和关键记录。
  - 第 8 天旧知题 3已补 `project_id、project_name；2 行，应为项目 13、14`。
- 对初学者的影响：修复后每题都有可核对目标，不必猜测需要保留哪些列。
- 严重程度：一般
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-07：诊断题残留中文字符串 `N` 前缀提示

- 对应课程或文件：`00_diagnostic_test.sql`（题 7）
- 原问题说明：提示“中文字符串前可写 N”，容易让学习者沿用 SQL Server 习惯。
- 当前复审证据：提示已改为“utf8mb4 数据库中，中文字符串直接使用单引号”，不再出现 `N` 前缀。
- 对初学者的影响：修复后方言说明与 MariaDB 课程答案一致。
- 严重程度：建议
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-08：事务课混用 `BEGIN` 与 `START TRANSACTION`

- 对应课程或文件：`09_data_modification.sql`、`hints.md`
- 原问题说明：模板使用 `START TRANSACTION`，题目和提示却写 `BEGIN`。
- 当前复审证据：第 9 天题 4及 `hints.md` 均已统一为 `START TRANSACTION、INSERT、SELECT、ROLLBACK`。
- 对初学者的影响：修复后练习关键词与可运行示例一致，不再需要额外猜测两种写法的关系。
- 严重程度：建议
- 修改建议：无需继续修改。
- 是否已修复：是

### MY-TQ-09：NULL 与空字符串没有跨 3 个日期主动复习

- 对应课程或文件：`02_filter_basics.sql`、`07_case_subquery.sql`、`09_data_modification.sql`、对应答案和提示
- 原问题说明：该易混点原来只在第 2、9 天出现，中间缺少第三次提取。
- 当前复审证据：
  - 第 2 天示例明确说明 NULL 不是空字符串。
  - 第 7 天旧知题 3要求同时使用 `IS NULL` 与 `= ''`，并要求预测当前只有 NULL。
  - 第 9 天旧知题 2再次完成同类辨析。
  - 第 7 天答案和两处提示均已同步。
- 对初学者的影响：修复后该知识点在三个日期重复出现，间隔复习要求已满足。
- 严重程度：建议
- 修改建议：无需继续修改。
- 是否已修复：是

## 全量复审通过项

- README 足以指导初学者启动 XAMPP MySQL、在 DBeaver 创建 MariaDB/MySQL 连接、填写地址端口、测试连接、打开 SQL 文件、选中语句运行和确认当前数据库。
- README 已说明 `baseline_status` 必须为 `PASS`，并警告 FAIL 时停止，不会误导学习者自动删除已有数据。
- 可执行课程和答案使用 `LIMIT`、`IFNULL`、`START TRANSACTION`；未发现 `dbo.`、`GO`、`ISNULL`、`TRY_CAST`、`THROW` 等 T-SQL 残留。
- `TOP` 只用于 SQL Server 对比与改错，不出现在 MariaDB 正确答案。
- 第 1～9 天均为 9～10 题，第 10 天为 12 题且分两轮；第 8 天也拆成两个学习段，45～60 分钟负荷已有明确控制。
- 第 1 天有 2 道热身，第 2～9 天有 3 道旧知复习；LIKE、NOT、NULL/空字符串等基础点有跨日期回顾。
- 提示文件按日期和题号组织，没有粘贴完整 SQL；阶段测试提示保持为思考方向。
- 答案均位于 `answers/`，逐题有中文说明；JOIN、NULL、重复计数和改错题解释总体符合初学者需要。
- 诊断测试没有使用子查询、CTE、EXISTS、REGEXP 或类型转换。
- checkpoint 1只覆盖第 1～4 天内容；checkpoint 2覆盖第 5～8 天的 JOIN、CASE、子查询、CTE、EXISTS、安全转换和 NULL 处理。
- 最终综合题只使用前面已教学的知识。
- 未发现窗口函数、存储过程、触发器、游标、动态 SQL、递归 CTE、高级优化或 DBA 管理内容。
- `audit_sql_correctness.md` 已提供 MariaDB 10.4.32 的真实执行证据，并明确实际范围与已知边界。

## 最终数量汇总

### 首轮问题

- 严重：1
- 一般：5
- 建议：3
- 合计：9

### 当前状态

- 已完全修复：9
- 部分修复但仍存在：0
- 新发现问题：0

### 最终未修复

- 严重：0
- 一般：0
- 建议：0
- 未修复合计：0

## 审计边界

本轮独立进行了教学质量静态复审，没有再次执行全部 SQL。MariaDB 实际执行结论来自本轮读取的 `audit_sql_correctness.md` 与 `final_audit_summary.md`；两者均记录 MariaDB 10.4.32、27 个 SQL 文件全量回归且失败 0。教学质量复审当前未发现尚未修复的严重、一般或建议问题。
