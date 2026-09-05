USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：按项目状态分组；无 JOIN，不会扩张计数。
SELECT project_status, COUNT(*) AS project_count
FROM dbo.projects
GROUP BY project_status;

-- 题 2：HAVING 筛选分组后的平均工资；无 JOIN。
SELECT department_id, AVG(salary) AS average_salary
FROM dbo.employees
GROUP BY department_id
HAVING AVG(salary) > 12000;

-- 题 3：LIKE 两边的 % 表示名称前后可有任意文字；无 JOIN。
SELECT project_name, budget
FROM dbo.projects
WHERE project_name LIKE N'%数据%'
ORDER BY budget DESC;

-- 题 4：JOIN 条件是员工的 department_id 对部门主键。
-- 多名员工属于同一部门，部门名会重复，但员工不会被重复。
SELECT e.employee_name, d.department_name, d.city
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d ON d.department_id = e.department_id;

-- 题 5：项目的 project_manager_id 对员工主键。
-- INNER JOIN 会排除 NULL 经理的项目 14；每个有经理项目一行。
SELECT p.project_name, e.employee_name, e.job_title
FROM dbo.projects AS p
INNER JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;

-- 题 6：关系表分别连接员工主键和项目主键。
-- 一人可参与多项目，因此员工姓名可重复；关系表字段非 NULL。
SELECT e.employee_name, p.project_name, ep.working_hours
FROM dbo.employee_projects AS ep
INNER JOIN dbo.employees AS e ON e.employee_id = ep.employee_id
INNER JOIN dbo.projects AS p ON p.project_id = ep.project_id;

-- 题 7：项目连接部门和指标；INNER JOIN 只保留有指标记录的技术部项目。
-- 当前每项目一条指标，不扩张；指标中的 NULL 会原样显示。
SELECT p.project_name, pm.management_fee, pm.investment_return_rate
FROM dbo.projects AS p
INNER JOIN dbo.departments AS d ON d.department_id = p.department_id
INNER JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
WHERE d.department_name = N'技术部';

-- 题 8：项目主键连接关系表项目外键；按项目分组。
-- INNER JOIN 排除无参与项目；COUNT 统计每条参与关系。
SELECT p.project_id, p.project_name, COUNT(ep.employee_id) AS participant_count
FROM dbo.projects AS p
INNER JOIN dbo.employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name;

-- 题 9A：错误 SQL 缺少 ON，在 SQL Server 中直接语法报错。
-- 题 9B：ON 1=1 对每对行都成立，能运行但产生 20×5=100 行笛卡尔积。
-- 修正后按 department_id 连接；一名员工只匹配一个部门，共 20 行。
SELECT e.employee_name, d.department_name
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d ON d.department_id = e.department_id;

-- 题 10：错误条件把不同含义的 employee_id 和 department_id 相连。
-- 修正后使用员工的 department_id；NULL 不影响必填外键。
SELECT e.employee_name, d.department_name
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d ON d.department_id = e.department_id;
