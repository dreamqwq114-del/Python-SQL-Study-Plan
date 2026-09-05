USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

/*
第 8 天：CTE、EXISTS 与类型转换入门
本课目标
1. 使用一次非递归 CTE，让查询分成两小步。
2. 用 EXISTS / NOT EXISTS 判断“有没有”。
3. 用 TRY_CAST 安全尝试转换。
4. 主要使用 ISNULL 替换显示用 NULL。
*/

-- 基础语法
-- ;WITH 名称 AS (SELECT ...) SELECT ... FROM 名称;
-- WHERE EXISTS (SELECT 1 FROM 相关表 WHERE 连接条件)
-- TRY_CAST(值 AS 类型)：失败时返回 NULL，不让整条查询报错。
-- ISNULL(值, 替代值)：值为 NULL 时显示替代值。

-- 可运行示例 1：CTE 先取高预算项目，再查询；预计 4 行。
;WITH high_budget_projects AS
(
    SELECT project_id, project_name, budget
    FROM dbo.projects
    WHERE budget >= 800000
)
SELECT project_id, project_name, budget
FROM high_budget_projects;

-- 可运行示例 2：查询至少参加一个项目的员工；预计 18 行。
SELECT e.employee_name
FROM dbo.employees AS e
WHERE EXISTS
(
    SELECT 1 FROM dbo.employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 可运行示例 3：查询没有参与项目的员工；结果 2 行。
SELECT e.employee_name
FROM dbo.employees AS e
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 可运行示例 4：先用 REPLACE 去掉 kV，再尝试转为小数；预计 12 行。
-- DECIMAL(10, 2) 表示最多 10 位数字，其中小数点后保留 2 位。
-- “低压”“380V”和 NULL 转换失败或无值时，voltage_number 为 NULL。
SELECT voltage_level,
       TRY_CAST(REPLACE(voltage_level, N'kV', N'') AS DECIMAL(10, 2)) AS voltage_number
FROM dbo.project_metrics;

-- 可运行示例 5：没有电压信息时显示“未填写”。COALESCE 也能替换 NULL，
-- 本课只重点练 ISNULL；预计 12 行，其中 1 行显示“未填写”。
SELECT metric_id, ISNULL(voltage_level, N'未填写') AS voltage_display
FROM dbo.project_metrics;

-- 旧知识复习
-- 题 1：用 CASE 把工资分为 >=15000 的“高”和其他“普通”。
-- 返回 employee_name、salary_level；20 行。TODO:

-- 题 2：查询高于平均预算的项目。
-- 返回 project_name、budget；7 行。提示：标量子查询。TODO:

-- 题 3：找无指标项目；提示：LEFT JOIN。结果 2 行。TODO:

-- 本课练习
-- 题 4：用 CTE 先选“进行中”项目，再显示 project_name、budget；5 行。
-- 提示：CTE 内只做筛选，外层只取列。TODO:

-- 题 5：用 EXISTS 查询至少有一名员工参与的项目。
-- 返回 project_id、project_name；12 行。TODO:

-- 题 6：用 NOT EXISTS 查询没有任何员工参与的项目。
-- 返回 project_id、project_name；2 行。TODO:

-- 题 7：尝试去掉 voltage_level 中的“kV”后转为 DECIMAL。
-- 返回 voltage_level、voltage_number；“低压”和“380V”等不能转换时为 NULL。
-- 提示：模仿示例 4，REPLACE 只是先做固定的文字清理。TODO:

-- 题 8：显示项目名称和经理编号；无经理时显示 0。
-- 返回 project_name、manager_id_display；14 行。提示：ISNULL。TODO:

-- 题 9（改错）：下面 CAST 遇到“低压”会报错。
-- 错误 SQL：SELECT CAST(voltage_level AS INT) FROM dbo.project_metrics;
-- 目标：转换失败时返回 NULL，不中断查询。TODO:

-- 题 10（改错）：下面 EXISTS 没有关联外层员工，只要关系表有一行，
-- 就会返回所有员工。
-- SELECT e.employee_name FROM dbo.employees AS e
-- WHERE EXISTS (SELECT 1 FROM dbo.employee_projects AS ep);
-- 请补上外层与内层的关联条件；应返回 18 名参与过项目的员工。TODO:

/*
每日自检
[ ] 我能写非递归 CTE、EXISTS 和 TRY_CAST。
[ ] 我能解释 EXISTS 检查“有没有”。
[ ] 我能预测 NOT EXISTS 返回 2 行。
[ ] 我理解 TRY_CAST 失败返回 NULL。
[ ] 我能说明 EXISTS 中的连接条件。
[ ] 我检查了 NULL 和重复行。
[ ] 我写下了今天最容易错的知识点。
*/
