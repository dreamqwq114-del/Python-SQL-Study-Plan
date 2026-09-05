USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

/*
第 1 天：SELECT 基础
本课目标
1. 查询指定列，而不是总写 SELECT *。
2. 使用 TOP、DISTINCT 和 AS。
3. 写一个简单计算列。
*/

-- 基础语法（只看结构）
-- SELECT 列1, 列2 FROM 表;
-- SELECT TOP (数量) 列 FROM 表 ORDER BY 排序列;
-- SELECT DISTINCT 列 FROM 表;
-- SELECT 数值列 * 数字 AS 新列名 FROM 表;
-- ORDER BY 列 ASC/DESC：本课只用它让 TOP 结果稳定，第 3 天再系统练排序。

-- 可运行示例 1：查看员工姓名和职位；结果 20 行、2 列。
SELECT employee_name, job_title FROM dbo.employees;

-- 可运行示例 2：查看工资最高的 3 名员工；结果 3 行。
SELECT TOP (3) employee_name, salary
FROM dbo.employees
ORDER BY salary DESC;

-- 可运行示例 3：查看不重复的项目状态；结果 4 行。
SELECT DISTINCT project_status FROM dbo.projects;

-- 可运行示例 4：给预算增加易懂的别名，并计算预算的 10%；结果 14 行。
SELECT project_name AS 项目名称, budget, budget * 0.10 AS 预算的百分之十
FROM dbo.projects;

-- 本课练习（共 9 题）
-- 题 1（热身）：查询所有部门名称。返回 department_name；5 行。提示：指定一列。
-- TODO:

-- 题 2（热身）：查询所有员工姓名和工资。返回 employee_name、salary；20 行。提示：两列用逗号分隔。
-- TODO:

-- 题 3：查询前 5 个项目。返回 project_id、project_name；5 行。
-- 结果必须稳定地按 project_id 最小的 5 个。提示：TOP 要配合 ORDER BY。
-- TODO:

-- 题 4：查询所有不重复的职位。返回 job_title；结果少于 20 行。
-- 提示：使用 DISTINCT。
-- TODO:

-- 题 5：查询项目名称和预算，并把列名显示为“项目名称”“项目预算”。
-- 返回 14 行、2 列。提示：使用 AS。
-- TODO:

-- 题 6：查询项目名称、原预算、预算的 5%。
-- 返回 project_name、budget、budget_fee；14 行。提示：计算列不修改原数据。
-- TODO:

-- 题 7：查询工资最低的 4 名员工。返回 employee_name、salary；4 行。
-- 提示：TOP、ORDER BY、ASC。
-- TODO:

-- 题 8（改错）：下面 SQL 会报字段不存在。说明原因并改正。
-- 错误 SQL：SELECT name, salary FROM dbo.employees;
-- 修正后返回 employee_name、salary，共 20 行。提示：核对真实字段名。
-- TODO:

-- 题 9（综合）：查询预算最高的 3 个项目，返回 project_name、
-- budget 和 budget * 0.15（别名 management_fee_estimate）；3 行。
-- 提示：组合 TOP、计算列、AS 和排序。
-- TODO:

/*
每日自检
[ ] 我能不看答案写出基础语句。
[ ] 我能解释查询目标。
[ ] 我能预测结果大致多少行。
[ ] 我理解改错题的错误原因。
[ ] 我能说明本课还没有使用 JOIN。
[ ] 我检查了 NULL 和重复值对 DISTINCT 的影响。
[ ] 我写下了今天最容易错的知识点。
*/
