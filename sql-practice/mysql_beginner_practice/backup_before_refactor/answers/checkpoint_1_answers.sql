USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

-- 题 1：LIMIT 配合稳定排序；无 JOIN。
SELECT employee_name, salary
FROM employees
ORDER BY salary DESC, employee_id
LIMIT 5;

-- 题 2：日期与预算同时筛选；无 JOIN。
SELECT project_name, start_date, budget
FROM projects
WHERE start_date >= '2024-01-01'
  AND start_date < '2025-01-01'
  AND budget BETWEEN 300000 AND 800000
ORDER BY budget DESC;

-- 题 3：NULL 用 IS NULL；无 JOIN。
SELECT project_id, project_name, end_date
FROM projects
WHERE end_date IS NULL;

-- 题 4：全部聚合返回一行；salary 非 NULL。
SELECT COUNT(*) AS employee_count,
       MIN(salary) AS minimum_salary,
       MAX(salary) AS maximum_salary,
       AVG(salary) AS average_salary
FROM employees;

-- 题 5：职位分组；无 JOIN，相同职位合并。
SELECT job_title, COUNT(*) AS employee_count
FROM employees
GROUP BY job_title;

-- 题 6：按部门分组；无 JOIN。
SELECT department_id,
       SUM(salary) AS salary_sum,
       AVG(salary) AS average_salary
FROM employees
GROUP BY department_id;

-- 题 7：按状态分组，不受其他表重复影响。
SELECT project_status,
       COUNT(*) AS project_count,
       AVG(budget) AS average_budget
FROM projects
GROUP BY project_status;

-- 题 8：HAVING 筛选分组后的平均值。
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) >= 12000;

-- 题 9：WHERE 先筛日期，HAVING 再筛组内人数。
SELECT department_id, COUNT(*) AS employee_count
FROM employees
WHERE hire_date >= '2022-01-01'
GROUP BY department_id
HAVING COUNT(*) >= 2;

-- 题 10：错误在于聚合条件放 WHERE，且多分组了 budget。
-- 修正后每个状态一行；无 JOIN。
SELECT project_status, SUM(budget) AS total_budget
FROM projects
GROUP BY project_status
HAVING SUM(budget) > 1000000;
