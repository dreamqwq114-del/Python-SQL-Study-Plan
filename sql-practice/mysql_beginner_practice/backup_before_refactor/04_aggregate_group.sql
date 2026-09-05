USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 4 天：聚合与分组
本课目标
1. 使用 COUNT、SUM、AVG、MIN、MAX。
2. 按一列 GROUP BY。
3. 区分 WHERE 与 HAVING。
4. 理解 COUNT(*) 与 COUNT(column)。
*/

-- 基础语法
-- SELECT 分组列, COUNT(*) FROM 表 GROUP BY 分组列;
-- WHERE 在分组前筛选行；HAVING 在分组后筛选组。

-- 可运行示例 1：员工总数；1 行，值 20。
SELECT COUNT(*) AS employee_count FROM employees;

-- 可运行示例 2：每个部门的平均工资；5 行。
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id;

-- 可运行示例 3：只保留平均工资高于 12000 的部门；预计 3 行。
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 12000;

-- 可运行示例 4：COUNT(*) 计全部项目；COUNT(end_date) 忽略 NULL。
SELECT COUNT(*) AS all_projects, COUNT(end_date) AS projects_with_end_date
FROM projects;

-- 旧知识复习
-- 题 1：查询预算最高的 3 个项目名称和预算；3 行。
-- 提示：LIMIT 与排序。TODO:

-- 题 2：查询没有结束日期的项目名称；6 行。
-- 提示：IS NULL。TODO:

-- 题 3：查询 2023 年及以后入职且工资小于 10000 的员工，按工资升序。
-- 返回 employee_name、salary；约 5 行。TODO:

-- 本课练习
-- 题 4：统计所有项目的预算总和、平均值、最小值和最大值；1 行、4 列。
-- 提示：四个聚合函数可以放在一个 SELECT。
-- TODO:

-- 题 5：按项目状态统计数量。返回 project_status、project_count；4 行。
-- TODO:

-- 题 6：按部门统计员工人数和平均工资。
-- 返回 department_id、employee_count、average_salary；5 行。
-- TODO:

-- 题 7：只统计 2022 年及以后入职的员工，再按部门分组。
-- 返回 department_id、employee_count；应只包含有符合员工的部门。
-- 提示：WHERE 写在 GROUP BY 前。
-- TODO:

-- 题 8（综合）：找出员工数至少 4 人的部门编号。
-- 返回 department_id、employee_count；4 行。
-- 提示：先分组，再用 HAVING 筛选计数结果。
-- TODO:

-- 题 9（改错）：下面 SQL 为什么报错？
-- 错误 SQL：SELECT department_id, job_title, AVG(salary)
--           FROM employees GROUP BY department_id;
-- 目标：按部门和职位统计平均工资；返回每个“部门+职位”组合。
-- 提示：SELECT 中非聚合列要在 GROUP BY 中。TODO:

-- 题 10（改错）：目标是统计全部项目数，下面 SQL 为什么只得到 8？
-- 错误 SQL：SELECT COUNT(end_date) AS project_count FROM projects;
-- 返回 project_count；正确结果应为 14。提示：COUNT(column) 会忽略 NULL。TODO:

/*
每日自检
[ ] 我能独立写聚合和分组。
[ ] 我能解释 WHERE 与 HAVING。
[ ] 我能预测分组后大致行数。
[ ] 我理解 GROUP BY 缺列的错误。
[ ] 我能说明本课还没有使用 JOIN。
[ ] 我检查了 COUNT(column) 对 NULL 的影响。
[ ] 我写下了今天最容易错的知识点。
*/
