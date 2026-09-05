USE mysql_beginner_practice;

-- ==================================================
-- 诊断 1 参考答案
-- ==================================================

SELECT
    employee_name,
    job_title
FROM employees;

-- 核对：只有两列，并包含所有员工。

-- ==================================================
-- 诊断 2 参考答案
-- ==================================================

SELECT
    employee_name,
    salary
FROM employees
WHERE salary >= 12000
ORDER BY
    salary DESC,
    employee_id ASC;

-- 核对：没有低于 12000 的薪资，顺序从高到低。

-- ==================================================
-- 诊断 3 参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    end_date
FROM projects
WHERE end_date IS NULL;

-- 核对：end_date 应全部为 NULL；不能使用 = NULL。

-- ==================================================
-- 诊断 4 参考答案
-- ==================================================

SELECT
    department_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
ORDER BY department_id;

-- 核对：每个 department_id 一行，各组人数之和等于员工总数。

-- ==================================================
-- 诊断 5 参考答案
-- ==================================================

SELECT
    e.employee_name,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON d.department_id = e.department_id;

-- 核对：每名员工匹配一个部门，没有无意义的行数膨胀。

-- ==================================================
-- 诊断 6 参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON ep.employee_id = e.employee_id
WHERE ep.employee_id IS NULL;

-- 核对：只返回没有项目参与记录的员工，不应出现重复。

-- ==================================================
-- 诊断 7 参考答案
-- ==================================================

SELECT
    project_name,
    CASE
        WHEN budget >= 800000 THEN '高'
        ELSE '普通'
    END AS budget_level
FROM projects;

-- 核对：每个项目一行，budget_level 不应为 NULL。

-- ==================================================
-- 诊断 8 参考答案
-- ==================================================

SELECT
    employee_id,
    employee_name,
    salary
FROM employees
WHERE employee_id = 20;

-- 核对：这里只预览目标行，不执行 UPDATE。
