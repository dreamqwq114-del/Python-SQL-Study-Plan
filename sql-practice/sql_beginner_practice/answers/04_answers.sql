USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：TOP 与降序；无 JOIN。
SELECT TOP (3) project_name, budget
FROM dbo.projects
ORDER BY budget DESC, project_id;

-- 题 2：NULL 用 IS NULL；无 JOIN。
SELECT project_name FROM dbo.projects WHERE end_date IS NULL;

-- 题 3：先筛选再排序；无 JOIN。
SELECT employee_name, salary
FROM dbo.employees
WHERE hire_date >= '2023-01-01'
  AND salary < 10000
ORDER BY salary ASC;

-- 题 4：四个聚合都在全部项目上计算；无 JOIN，budget 非 NULL。
SELECT SUM(budget) AS total_budget,
       AVG(budget) AS average_budget,
       MIN(budget) AS minimum_budget,
       MAX(budget) AS maximum_budget
FROM dbo.projects;

-- 题 5：相同状态为一组；无 JOIN，不会因其他表扩张计数。
SELECT project_status, COUNT(*) AS project_count
FROM dbo.projects
GROUP BY project_status;

-- 题 6：部门编号决定分组；无 JOIN，COUNT(*) 包含组内所有员工。
SELECT department_id,
       COUNT(*) AS employee_count,
       AVG(salary) AS average_salary
FROM dbo.employees
GROUP BY department_id;

-- 题 7：WHERE 在分组前排除旧员工；无 JOIN。
SELECT department_id, COUNT(*) AS employee_count
FROM dbo.employees
WHERE hire_date >= '2022-01-01'
GROUP BY department_id;

-- 题 8：HAVING 在分组后按 COUNT 筛选；无 JOIN。
SELECT department_id, COUNT(*) AS employee_count
FROM dbo.employees
GROUP BY department_id
HAVING COUNT(*) >= 4;

-- 题 9：错误原因是 job_title 未聚合也未分组。
-- 修正后每个“部门+职位”组合一行；无 JOIN。
SELECT department_id, job_title, AVG(salary) AS average_salary
FROM dbo.employees
GROUP BY department_id, job_title;

-- 题 10：错误 SQL 使用 COUNT(end_date)，会忽略 6 个 end_date 为 NULL 的项目。
-- 错误 SQL：SELECT COUNT(end_date) AS project_count FROM dbo.projects;
-- 目标是统计表中全部项目行，所以使用 COUNT(*)，结果为 14。
SELECT COUNT(*) AS project_count
FROM dbo.projects;
