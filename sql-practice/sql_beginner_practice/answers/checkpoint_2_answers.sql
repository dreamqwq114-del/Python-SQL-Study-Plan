USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：员工 department_id 连接部门主键；每名员工一行。
SELECT e.employee_name, d.department_name, d.city
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d ON d.department_id = e.department_id;

-- 题 2：LEFT JOIN 保留无经理项目；经理 NULL 时姓名也为 NULL。
SELECT p.project_name, e.employee_name AS manager_name
FROM dbo.projects AS p
LEFT JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;

-- 题 3：LEFT JOIN 后检查右表主键 NULL；不产生重复。
SELECT e.employee_id, e.employee_name
FROM dbo.employees AS e
LEFT JOIN dbo.employee_projects AS ep ON ep.employee_id = e.employee_id
WHERE ep.employee_id IS NULL;

-- 题 4：项目放左边；COUNT(右表主键) 让无参与项目计 0。
SELECT p.project_name, COUNT(ep.employee_id) AS participant_count
FROM dbo.projects AS p
LEFT JOIN dbo.employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name;

-- 题 5：CASE 两档分类；无 JOIN。
SELECT project_name, budget,
       CASE WHEN budget >= 800000 THEN N'高' ELSE N'普通' END AS budget_level
FROM dbo.projects;

-- 题 6：标量子查询返回一个平均值；salary 非 NULL。
SELECT employee_name, salary
FROM dbo.employees
WHERE salary > (SELECT AVG(salary) FROM dbo.employees);

-- 题 7：非递归 CTE 先筛选，再由外层读取。
;WITH pending_projects AS
(
    SELECT project_id, project_name, budget
    FROM dbo.projects
    WHERE project_status = N'待启动'
)
SELECT project_id, project_name, budget
FROM pending_projects;

-- 题 8：EXISTS 按 employee_id 关联，只判断存在性，不扩张行。
SELECT e.employee_id, e.employee_name
FROM dbo.employees AS e
WHERE EXISTS
(
    SELECT 1 FROM dbo.employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 题 9：TRY_CAST 转换失败返回 NULL，而不是中断查询。
SELECT voltage_level, TRY_CAST(voltage_level AS INT) AS voltage_as_int
FROM dbo.project_metrics;

-- 题 10：右表费用条件放 ON 才保留全部左表项目；ISNULL 显示 0。
-- 原 WHERE 写法排除了无匹配和不满足费用条件的项目。
SELECT p.project_name, ISNULL(pm.management_fee, 0) AS management_fee
FROM dbo.projects AS p
LEFT JOIN dbo.project_metrics AS pm
    ON pm.project_id = p.project_id
   AND pm.management_fee > 0.15;
