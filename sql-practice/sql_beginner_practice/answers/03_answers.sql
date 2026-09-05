USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：BETWEEN 含边界；无 JOIN。
SELECT employee_name, salary
FROM dbo.employees
WHERE salary BETWEEN 10000 AND 14000;

-- 题 2：IN 合并两个状态条件；无 JOIN。
SELECT project_name, project_status
FROM dbo.projects
WHERE project_status IN (N'已完成', N'暂停');

-- 题 3：NULL 使用 IS NULL；无 JOIN。
SELECT department_name, city
FROM dbo.departments
WHERE city IS NULL;

-- 题 4：左闭右开避免时间边界歧义；无 JOIN。
SELECT employee_name, hire_date
FROM dbo.employees
WHERE hire_date >= '2022-01-01'
  AND hire_date < '2023-01-01'
ORDER BY hire_date ASC;

-- 题 5：先筛选再多列排序；无 JOIN，预算非 NULL。
SELECT project_name, budget, start_date
FROM dbo.projects
WHERE project_status = N'进行中'
ORDER BY budget DESC, start_date ASC;

-- 题 6：日期与数值条件同时满足；无 JOIN。
SELECT project_name, start_date, budget
FROM dbo.projects
WHERE start_date >= '2024-01-01'
  AND start_date < '2025-01-01'
  AND budget < 800000
ORDER BY budget ASC;

-- 题 7：% 表示任意长度文字；无 JOIN。
SELECT employee_name, job_title, salary
FROM dbo.employees
WHERE job_title LIKE N'%工程师%'
ORDER BY salary DESC;

-- 题 8：三个条件都用 AND；无 JOIN。
SELECT employee_name, salary, hire_date
FROM dbo.employees
WHERE department_id = 2
  AND salary > 12000
  AND hire_date < '2023-01-01'
ORDER BY salary DESC;

-- 题 9：括号明确“条件组 A 或条件 B”；无 JOIN。
-- NULL 不影响这些非空字段。
SELECT employee_name, hire_date, salary, job_title
FROM dbo.employees
WHERE (hire_date >= '2024-01-01' AND salary < 8000)
   OR job_title = N'实习生';

-- 题 10：SQL Server 用 TOP，不用 LIMIT；唯一编号作为次排序保证稳定。
-- 错误 SQL：... ORDER BY salary DESC LIMIT 3;
SELECT TOP (3) employee_name
FROM dbo.employees
ORDER BY salary DESC, employee_id ASC;
