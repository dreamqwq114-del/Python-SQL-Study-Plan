USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 3 天：排序、日期与综合筛选
本课目标
1. 使用单列和多列排序。
2. 写清日期、字符串和数值条件。
3. 综合复习 SELECT 与 WHERE。
*/

-- 基础语法
-- ORDER BY 列1 ASC, 列2 DESC;
-- WHERE 日期列 >= '2024-01-01' AND 日期列 < '2025-01-01';

-- 可运行示例 1：先按部门升序，再按工资降序；结果 20 行。
SELECT employee_name, department_id, salary
FROM employees
ORDER BY department_id ASC, salary DESC;

-- 可运行示例 2：查询 2024 年开始的项目；结果 6 行。
SELECT project_name, start_date
FROM projects
WHERE start_date >= '2024-01-01' AND start_date < '2025-01-01'
ORDER BY start_date;

-- 可运行示例 3：预算至少 700000 的项目，预算从高到低；结果 5 行。
SELECT project_name, budget
FROM projects
WHERE budget >= 700000
ORDER BY budget DESC;

-- 可运行示例 4：名称包含“数据”的项目；结果 2 行。
SELECT project_name FROM projects WHERE project_name LIKE '%数据%';

-- 旧知识复习
-- 题 1：查询工资在 10000～14000 之间的员工姓名和工资；8 行。
-- 提示：BETWEEN。TODO:

-- 题 2：查询已完成或暂停的项目名称和状态；5 行。
-- 提示：IN。TODO:

-- 题 3：查询没有城市信息的部门；1 行。
-- 返回 department_name、city。提示：IS NULL。TODO:

-- 本课练习
-- 题 4：查询 2022 年入职的员工，按 hire_date 从早到晚。
-- 返回 employee_name、hire_date；4 行。提示：用左闭右开的日期范围。
-- TODO:

-- 题 5：查询所有进行中项目，先按预算降序，再按开始日期升序。
-- 返回 project_name、budget、start_date；5 行。
-- TODO:

-- 题 6：查询 2024 年开始、预算低于 800000 的项目。
-- 返回 project_name、start_date、budget；3 行，并按预算升序。
-- TODO:

-- 题 7：查询职位名称中包含“工程师”的员工，按工资降序。
-- 返回 employee_name、job_title、salary；6 行。
-- TODO:

-- 题 8（综合）：查询技术部（department_id=2）中工资 12000 以上、
-- 2023 年以前入职的员工，返回 employee_name、salary、hire_date；
-- 约 4 行，工资高者在前。提示：组合多个 AND。
-- TODO:

-- 题 9（改错）：目标是找“2024 年入职且工资低于 8000”或“实习生”。
-- 错误 SQL 的日期只约束低工资员工，没有清楚表达整体逻辑：
-- SELECT employee_name FROM employees
-- WHERE hire_date >= '2024-01-01' AND salary < 8000 OR job_title = '实习生';
-- 请加括号表达目标，并返回 employee_name、hire_date、salary、job_title。
-- TODO:

-- 题 10（改错）：下面 SQL 使用了 SQL Server 写法。
-- 错误 SQL：SELECT TOP (3) employee_name FROM employees ORDER BY salary DESC;
-- 改为 MariaDB/MySQL 写法，稳定返回工资最高的 3 人。TODO:

/*
每日自检
[ ] 我能独立写排序和日期范围。
[ ] 我能解释查询目标。
[ ] 我能预测大致行数。
[ ] 我理解 LIMIT 与 SQL Server TOP 的区别。
[ ] 我能说明本课还没有使用 JOIN。
[ ] 我检查了 NULL、日期边界和括号。
[ ] 我写下了今天最容易错的知识点。
*/
