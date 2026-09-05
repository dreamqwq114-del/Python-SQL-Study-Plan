USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

-- 题 1：LIMIT 与工资降序；无 JOIN，不受 NULL 影响。
SELECT employee_name, salary
FROM employees
ORDER BY salary DESC, employee_id
LIMIT 2;

-- 题 2：DISTINCT 去重，多个部门的上海只显示一次；NULL 也作为一个结果。
SELECT DISTINCT city FROM departments;

-- 题 3：计算列；无 JOIN，预算非 NULL。
SELECT project_name, budget, budget * 0.20 AS estimated_cost
FROM projects;

-- 题 4：BETWEEN 包含两个边界；无 JOIN。
SELECT employee_name, salary
FROM employees
WHERE salary BETWEEN 9000 AND 12000;

-- 题 5：IN 表示两个允许值；无 JOIN，department_id 非 NULL。
SELECT employee_id, department_id
FROM employees
WHERE department_id IN (2, 3);

-- 题 6：两个条件必须同时成立；无 JOIN。
SELECT employee_name, hire_date, salary
FROM employees
WHERE hire_date >= '2024-01-01'
  AND salary < 8000;

-- 题 7：<> 排除工程师；无 JOIN，job_title 非 NULL。
SELECT employee_name, job_title
FROM employees
WHERE job_title <> '工程师';

-- 题 8：NULL 用 IS NULL；无 JOIN。
SELECT project_name, project_status, end_date
FROM projects
WHERE project_status = '待启动'
  AND end_date IS NULL;

-- 题 9：错误原因是 AND 先于 OR，原式会保留技术部全部员工。
-- 无 JOIN；括号先限定部门，再同时检查工资。
SELECT employee_name, department_id, salary
FROM employees
WHERE department_id IN (2, 4)
  AND salary >= 12000;

-- 题 10：错误 SQL 的 = NULL 不会得到 TRUE；应使用 IS NULL。
-- 错误 SQL：SELECT project_name FROM projects WHERE end_date = NULL;
SELECT project_name, end_date
FROM projects
WHERE end_date IS NULL;
