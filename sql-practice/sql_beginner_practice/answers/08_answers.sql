USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：CASE 两档分类；无 JOIN。
SELECT employee_name,
       CASE WHEN salary >= 15000 THEN N'高' ELSE N'普通' END AS salary_level
FROM dbo.employees;

-- 题 2：标量子查询返回一个平均预算；无 JOIN。
SELECT project_name, budget
FROM dbo.projects
WHERE budget > (SELECT AVG(budget) FROM dbo.projects);

-- 题 3：LEFT JOIN 后检查指标主键 NULL；结果为两个无指标项目。
SELECT p.project_id, p.project_name
FROM dbo.projects AS p
LEFT JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.project_id IS NULL;

-- 题 4：CTE 只是给第一步结果命名，不递归；无 JOIN。
;WITH active_projects AS
(
    SELECT project_name, budget
    FROM dbo.projects
    WHERE project_status = N'进行中'
)
SELECT project_name, budget
FROM active_projects;

-- 题 5：EXISTS 内层用 project_id 关联外层；只判断是否存在，不扩张行。
SELECT p.project_id, p.project_name
FROM dbo.projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM dbo.employee_projects AS ep
    WHERE ep.project_id = p.project_id
);

-- 题 6：NOT EXISTS 保留没有关系行的项目；不会产生重复。
SELECT p.project_id, p.project_name
FROM dbo.projects AS p
WHERE NOT EXISTS
(
    SELECT 1
    FROM dbo.employee_projects AS ep
    WHERE ep.project_id = p.project_id
);

-- 题 7：先去掉 kV，再安全转换；“低压”“380V”等失败时为 NULL。
SELECT voltage_level,
       TRY_CAST(REPLACE(voltage_level, N'kV', N'') AS DECIMAL(10, 2)) AS voltage_number
FROM dbo.project_metrics;

-- 题 8：ISNULL 只替换 NULL 经理编号；无 JOIN。
SELECT project_name, ISNULL(project_manager_id, 0) AS manager_id_display
FROM dbo.projects;

-- 题 9：CAST 遇到不可转换文字会报错；TRY_CAST 失败返回 NULL。
-- 错误 SQL：SELECT CAST(voltage_level AS INT) FROM dbo.project_metrics;
SELECT voltage_level, TRY_CAST(voltage_level AS INT) AS voltage_as_int
FROM dbo.project_metrics;

-- 题 10：错误子查询没有引用外层员工，所以对所有员工结果相同。
-- 用 employee_id 关联后，EXISTS 每名员工独立判断；不扩张重复。
SELECT e.employee_name
FROM dbo.employees AS e
WHERE EXISTS
(
    SELECT 1
    FROM dbo.employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);
