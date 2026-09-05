USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：员工外键连接部门主键；每名员工一个部门。
SELECT e.employee_name, d.department_name
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d ON d.department_id = e.department_id;

-- 题 2：INNER JOIN 只统计有关系的项目；一条关系代表一名参与者。
SELECT p.project_id, p.project_name, COUNT(ep.employee_id) AS participant_count
FROM dbo.projects AS p
INNER JOIN dbo.employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name;

-- 题 3：NULL 用 IS NULL；无 JOIN。
SELECT project_name, budget
FROM dbo.projects
WHERE end_date IS NULL
ORDER BY budget DESC;

-- 题 4：部门在左边会全部保留；一部门多员工会让部门名重复。
-- 若部门无员工，employee_name 为 NULL。
SELECT d.department_name, e.employee_name
FROM dbo.departments AS d
LEFT JOIN dbo.employees AS e ON e.department_id = d.department_id;

-- 题 5：右表主键为 NULL 表示没有参与关系。
SELECT p.project_id, p.project_name
FROM dbo.projects AS p
LEFT JOIN dbo.employee_projects AS ep ON ep.project_id = p.project_id
WHERE ep.project_id IS NULL;

-- 题 6：项目左连接指标；右表主键为 NULL 表示没有指标。
SELECT p.project_id, p.project_name
FROM dbo.projects AS p
LEFT JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.project_id IS NULL;

-- 题 7：LEFT JOIN 保留 project_manager_id 为 NULL 的项目。
-- 每项目最多一个经理，不会扩张行。
SELECT p.project_name, e.employee_name AS manager_name
FROM dbo.projects AS p
LEFT JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;

-- 题 8：员工放左边保留未参与者；COUNT(右表主键) 对无匹配行计 0。
-- 一人多项目会增加计数，这正是项目数。
SELECT e.employee_id, e.employee_name, COUNT(ep.project_id) AS project_count
FROM dbo.employees AS e
LEFT JOIN dbo.employee_projects AS ep ON ep.employee_id = e.employee_id
GROUP BY e.employee_id, e.employee_name;

-- 题 9：错误原因是 WHERE 要求右表费用非 NULL，排除了无匹配项目。
-- 把费用条件放 ON，只控制右表匹配；左表 14 个项目仍保留。
SELECT p.project_name, pm.management_fee
FROM dbo.projects AS p
LEFT JOIN dbo.project_metrics AS pm
    ON pm.project_id = p.project_id
   AND pm.management_fee > 0.15;

-- 题 10：错误 SQL 不需要 employee_projects；该 JOIN 会让一人多项目重复，
-- INNER JOIN 还会排除员工 19、20。最基础写法只连接部门与员工。
SELECT d.department_name,
       COUNT(e.employee_id) AS employee_count
FROM dbo.departments AS d
LEFT JOIN dbo.employees AS e ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name;

-- 可选理解：若为了观察重复而保留关系表，必须 LEFT JOIN 保留无项目员工，
-- 再按员工编号去重计数。本课程优先使用上面的基础写法。
SELECT d.department_name,
       COUNT(DISTINCT e.employee_id) AS employee_count
FROM dbo.departments AS d
LEFT JOIN dbo.employees AS e ON e.department_id = d.department_id
LEFT JOIN dbo.employee_projects AS ep ON ep.employee_id = e.employee_id
GROUP BY d.department_id, d.department_name;
