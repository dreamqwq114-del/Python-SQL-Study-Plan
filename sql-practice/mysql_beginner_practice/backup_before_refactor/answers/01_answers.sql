USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

-- 题 1：指定 department_name；无 JOIN，重复名称若存在不会自动去重。
SELECT department_name FROM departments;

-- 题 2：指定两列；无 JOIN，salary 非 NULL。
SELECT employee_name, salary FROM employees;

-- 题 3：LIMIT 配合唯一 project_id 排序保证结果稳定；无 JOIN。
SELECT project_id, project_name
FROM projects
ORDER BY project_id
LIMIT 5;

-- 题 4：DISTINCT 合并相同职位；无 JOIN，NULL 若存在也只显示一次。
SELECT DISTINCT job_title FROM employees;

-- 题 5：AS 只改结果列名，不改表结构；无 JOIN。
SELECT project_name AS 项目名称, budget AS 项目预算
FROM projects;

-- 题 6：计算列不会修改 budget；无 JOIN，budget 非 NULL。
SELECT project_name, budget, budget * 0.05 AS budget_fee
FROM projects;

-- 题 7：ASC 从低到高；无 JOIN，employee_id 可作为同工资时的稳定次序。
SELECT employee_name, salary
FROM employees
ORDER BY salary ASC, employee_id ASC
LIMIT 4;

-- 题 8：错误 SQL 的 name 不是实际字段；应使用 employee_name。
-- 错误 SQL：SELECT name, salary FROM employees;
-- 无 JOIN；修正后每名员工一行。
SELECT employee_name, salary FROM employees;

-- 题 9：先按预算降序再取 3 行；无 JOIN，计算列不改变原值。
SELECT project_name,
       budget,
       budget * 0.15 AS management_fee_estimate
FROM projects
ORDER BY budget DESC, project_id ASC
LIMIT 3;
