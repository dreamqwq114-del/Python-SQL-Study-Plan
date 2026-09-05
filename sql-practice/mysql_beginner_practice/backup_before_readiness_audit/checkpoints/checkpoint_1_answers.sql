USE mysql_beginner_practice;

-- ==================================================
-- 题 1 参考答案
-- ==================================================

SELECT
    employee_name,
    hire_date,
    salary
FROM employees
WHERE hire_date >= '2022-01-01'
ORDER BY
    hire_date DESC,
    employee_id ASC;

-- 验证：日期都不早于边界，顺序符合两个排序规则。

-- ==================================================
-- 题 2 参考答案
-- ==================================================

SELECT
    employee_id,
    employee_name,
    department_id,
    job_title,
    salary
FROM employees
WHERE (department_id = 2 AND salary >= 13000)
   OR job_title = '实习生';

-- 验证：逐行检查是否满足括号中的组合条件或实习生条件。

-- ==================================================
-- 题 3 参考答案
-- ==================================================

SELECT
    project_name,
    project_status,
    end_date
FROM projects
WHERE end_date IS NULL
  AND project_status <> '已完成';

-- 验证：end_date 全为 NULL，且没有已完成项目。

-- ==================================================
-- 题 4 参考答案
-- ==================================================

SELECT
    project_status,
    COUNT(*) AS project_count,
    AVG(budget) AS average_budget
FROM projects
GROUP BY project_status
ORDER BY project_status;

-- 验证：每种状态一行，project_count 之和等于项目总数。

-- ==================================================
-- 题 5 参考答案
-- ==================================================

SELECT
    department_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 4
ORDER BY department_id;

-- 验证：每组 employee_count 都不少于 4。

-- ==================================================
-- 题 6 参考答案
-- ==================================================

SELECT COUNT(*) AS project_count
FROM projects;

-- 原写法只统计 end_date 非 NULL 的行；COUNT(*) 才统计全部项目行。
-- 验证：与 SELECT 返回的全部项目行数比较。
