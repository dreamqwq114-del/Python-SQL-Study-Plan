USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：部门连接员工后按部门分组；当前每员工只属于一个部门。
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM dbo.departments AS d
LEFT JOIN dbo.employees AS e ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name;

-- 题 2：相同 JOIN 条件；AVG 忽略 NULL 工资，当前工资均非 NULL。
SELECT d.department_name, AVG(e.salary) AS average_salary
FROM dbo.departments AS d
LEFT JOIN dbo.employees AS e ON e.department_id = d.department_id
GROUP BY d.department_id, d.department_name;

-- 题 3：错误 SQL 使用 INNER JOIN，会排除 project_manager_id 为 NULL 的项目。
-- 错误 SQL：SELECT p.project_name, e.employee_name
-- FROM dbo.projects AS p
-- INNER JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;
-- 修正：LEFT JOIN 保留无经理项目；ISNULL 只改变显示文字。
SELECT p.project_name, ISNULL(e.employee_name, N'未分配') AS manager_name
FROM dbo.projects AS p
LEFT JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;

-- 题 4：只连接参与关系，COUNT(右表主键) 对无参与项目返回 0；
-- COUNT(*) 会把 LEFT JOIN 产生的空扩展行也计成 1。
-- 若以后连接另一张一对多明细，应先聚合或 COUNT(DISTINCT employee_id)。
SELECT p.project_name, COUNT(ep.employee_id) AS participant_count
FROM dbo.projects AS p
LEFT JOIN dbo.employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name;

-- 题 5：NOT EXISTS 只判断是否有关系，不扩张员工行。
SELECT e.employee_id, e.employee_name
FROM dbo.employees AS e
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 题 6：NOT EXISTS 按 project_id 判断；返回无关系的项目 13、14。
SELECT p.project_id, p.project_name
FROM dbo.projects AS p
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.employee_projects AS ep
    WHERE ep.project_id = p.project_id
);

-- 题 7：项目连接指标；INNER JOIN 排除无指标项目，NULL 费用不满足 >。
SELECT p.project_name, pm.management_fee
FROM dbo.projects AS p
INNER JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.management_fee > 0.15;

-- 题 8：标量子查询的 AVG 自动忽略 NULL；INNER JOIN 只保留有指标项目。
SELECT p.project_name, pm.investment_return_rate
FROM dbo.projects AS p
INNER JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.investment_return_rate >
(
    SELECT AVG(investment_return_rate)
    FROM dbo.project_metrics
);

-- 题 9：从 projects 单表分组，不受关系表重复影响。
SELECT project_status, COUNT(*) AS project_count
FROM dbo.projects
GROUP BY project_status;

-- 题 10：每条指标一行；乘 100 后 NULL 仍为 NULL。
SELECT p.project_name,
       pm.investment_return_rate * 100 AS return_percentage
FROM dbo.project_metrics AS pm
INNER JOIN dbo.projects AS p ON p.project_id = pm.project_id;

-- 题 11：先判断 NULL，再按高到低判断门槛，避免提前命中。
SELECT p.project_name,
       pm.investment_return_rate,
       CASE
           WHEN pm.investment_return_rate IS NULL THEN N'未知'
           WHEN pm.investment_return_rate >= 0.0850 THEN N'高'
           WHEN pm.investment_return_rate >= 0.0700 THEN N'中'
           ELSE N'低'
       END AS return_level
FROM dbo.project_metrics AS pm
INNER JOIN dbo.projects AS p ON p.project_id = pm.project_id;

-- 题 12：先在 CTE 中把一对多关系压成每项目一行，再连接其他表。
-- LEFT JOIN 保留无经理、无指标和无参与者项目；当前固定数据返回 14 行。
;WITH participant_counts AS
(
    SELECT project_id, COUNT(*) AS participant_count
    FROM dbo.employee_projects
    GROUP BY project_id
)
SELECT p.project_name,
       d.department_name,
       ISNULL(e.employee_name, N'未分配') AS manager_name,
       ISNULL(pc.participant_count, 0) AS participant_count,
       pm.management_fee,
       pm.investment_return_rate,
       pm.voltage_level,
       p.project_status
FROM dbo.projects AS p
INNER JOIN dbo.departments AS d ON d.department_id = p.department_id
LEFT JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id
LEFT JOIN participant_counts AS pc ON pc.project_id = p.project_id
LEFT JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
ORDER BY p.project_id;

/*
题 12 核对说明
A. 一对多 JOIN 会让“一”侧的一行分别匹配“多”侧的多行，所以项目名可能重复。
B. 用 SELECT COUNT(*) FROM dbo.projects; 得到 14，再确认最终查询也是 14 行。
C. 参与人数在 CTE 中连接其他表之前已经按 project_id 聚合，不会被后续连接重复统计。
D. 无经理或无指标仍是合法项目经营状态，使用 LEFT JOIN 才不会误删这些项目。
*/
