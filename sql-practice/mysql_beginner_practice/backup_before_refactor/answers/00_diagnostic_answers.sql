USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

-- 题 1：指定列即可；无 JOIN、无重复扩张，city 的 NULL 会原样显示。
SELECT department_id, department_name, city FROM departments;

-- 题 2：WHERE 在原表行上筛选；无 JOIN，salary 非 NULL。
SELECT employee_name, salary FROM employees WHERE salary > 12000;

-- 题 3：NULL 要用 IS NULL；无 JOIN，结果是唯一的最高负责人。
SELECT employee_id, employee_name FROM employees WHERE manager_id IS NULL;

-- 题 4：DESC 从高到低；无 JOIN，每名员工一行。
SELECT employee_name, salary FROM employees ORDER BY salary DESC;

-- 题 5：COUNT(*) 统计所有行，不受列中 NULL 影响；无 JOIN。
SELECT COUNT(*) AS employee_count FROM employees;

-- 题 6：每个状态一组；无 JOIN，相同状态被合并统计。
SELECT project_status, COUNT(*) AS project_count
FROM projects
GROUP BY project_status;

-- 题 7：N 表示 Unicode 字符串；无 JOIN、无 NULL 影响。
SELECT project_name, project_status
FROM projects
WHERE project_status = '进行中';

-- 题 8：日期可直接比较；无 JOIN，边界包含 2023-01-01。
SELECT employee_name, hire_date
FROM employees
WHERE hire_date >= '2023-01-01';

-- 题 9：JOIN 条件是相同 department_id；一个员工只属于一个部门，不会扩张。
SELECT e.employee_name, d.department_name
FROM employees AS e
INNER JOIN departments AS d ON d.department_id = e.department_id;

-- 题 10：错误 SQL 使用 = NULL；任何值与 NULL 的等号比较都不是 TRUE。
-- 错误 SQL：SELECT employee_name FROM employees WHERE manager_id = NULL;
-- 修正：无 JOIN；IS NULL 会返回 manager_id 缺失的员工。
SELECT employee_name FROM employees WHERE manager_id IS NULL;
