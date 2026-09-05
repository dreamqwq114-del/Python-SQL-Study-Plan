USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
阶段测试 1：第 4 天后完成
范围：SELECT、WHERE、ORDER BY、NULL、COUNT、SUM、AVG、GROUP BY、HAVING。
共 10 题。这里不提供详细提示，也不使用 JOIN。
*/

-- 题 1：查询工资最高的 5 名员工。
-- 返回 employee_name、salary；5 行。
-- TODO:

-- 题 2：查询 2024 年开始且预算在 300000～800000 之间的项目。
-- 返回 project_name、start_date、budget；按预算降序。
-- TODO:

-- 题 3：查询没有结束日期的项目。
-- 返回 project_id、project_name、end_date；6 行。
-- TODO:

-- 题 4：统计员工总数、最低工资、最高工资和平均工资。
-- 返回 1 行、4 列。
-- TODO:

-- 题 5：按职位统计人数。
-- 返回 job_title、employee_count；每个职位一行。
-- TODO:

-- 题 6：按部门统计工资总额和平均工资。
-- 返回 department_id、salary_sum、average_salary；5 行。
-- TODO:

-- 题 7：统计每个项目状态的项目数和平均预算。
-- 返回 project_status、project_count、average_budget；4 行。
-- TODO:

-- 题 8：找出平均工资至少 12000 的部门编号。
-- 返回 department_id、average_salary。
-- TODO:

-- 题 9：只统计 2022 年及以后入职的员工，找出人数至少 2 人的部门。
-- 返回 department_id、employee_count。
-- TODO:

-- 题 10（改错）：修正下面 SQL，使其按状态统计预算总额并只保留总额大于 1000000 的组。
-- 错误 SQL：SELECT project_status, SUM(budget) FROM projects
--           WHERE SUM(budget) > 1000000 GROUP BY project_status, budget;
-- TODO:
