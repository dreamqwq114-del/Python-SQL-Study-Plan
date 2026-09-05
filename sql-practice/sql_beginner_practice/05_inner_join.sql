USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

/*
第 5 天：INNER JOIN
本课目标
1. 根据主键、外键连接表。
2. 使用两表和三表 INNER JOIN。
3. 理解别名与 JOIN 条件。
4. 识别漏写条件造成的大量组合行。
*/

-- 基础语法
-- FROM 左表 AS a
-- INNER JOIN 右表 AS b ON b.外键 = a.主键

-- 可运行示例 1：员工及所属部门；20 行。
SELECT e.employee_name, d.department_name
FROM dbo.employees AS e
INNER JOIN dbo.departments AS d ON d.department_id = e.department_id;

-- 可运行示例 2：项目及所属部门；14 行。
SELECT p.project_name, d.department_name
FROM dbo.projects AS p
INNER JOIN dbo.departments AS d ON d.department_id = p.department_id;

-- 可运行示例 3：员工、参与项目和角色；37 行，一名员工可出现多次。
SELECT e.employee_name, p.project_name, ep.role_name
FROM dbo.employee_projects AS ep
INNER JOIN dbo.employees AS e ON e.employee_id = ep.employee_id
INNER JOIN dbo.projects AS p ON p.project_id = ep.project_id;

-- 可运行示例 4：项目和项目经理；预计 13 行，项目 14 因经理为 NULL 不出现。
SELECT p.project_name, e.employee_name AS manager_name
FROM dbo.projects AS p
INNER JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;

-- 旧知识复习
-- 题 1：按项目状态统计数量。
-- 返回 project_status、project_count；4 行。提示：GROUP BY 后 COUNT(*)。TODO:

-- 题 2：找出平均工资高于 12000 的部门编号和平均工资。
-- 提示：GROUP BY 与 HAVING。TODO:

-- 题 3：查询名称中包含“数据”的项目，按预算降序。
-- 返回 project_name、budget；2 行。提示：LIKE 两边使用 %。TODO:

-- 本课练习
-- 题 4：查询每位员工及其部门城市。
-- 返回 employee_name、department_name、city；20 行。
-- 提示：employees.department_id 连接 departments.department_id。
-- TODO:

-- 题 5：查询每个有经理的项目及经理职位。
-- 返回 project_name、employee_name、job_title；13 行。
-- 提示：project_manager_id 连接 employee_id。
-- TODO:

-- 题 6：查询员工参与的项目和工时。
-- 返回 employee_name、project_name、working_hours；37 行。
-- 提示：先从关系表连接两边。
-- TODO:

-- 题 7：查询技术部负责的项目及其指标。
-- 返回 project_name、management_fee、investment_return_rate；
-- 只显示有指标的技术部项目，约 3 行。需要 projects、departments、project_metrics。
-- TODO:

-- 题 8（综合）：统计每个有参与记录的项目人数。
-- 返回 project_id、project_name、participant_count；12 行。
-- 提示：projects 连接 employee_projects 后按项目分组。
-- TODO:

-- 题 9（改错）：请区分“语法报错”和“能运行但结果错误”。
-- A. 下面写法缺少 ON，在 SQL Server 中会直接报语法错误：
-- 错误 SQL：SELECT e.employee_name, d.department_name
--           FROM dbo.employees AS e INNER JOIN dbo.departments AS d;
-- B. 若写成 INNER JOIN dbo.departments AS d ON 1 = 1，虽然能运行，
--    却会得到 20×5=100 行组合。
-- 分别说明原因，并写出按 department_id 正确连接的 SQL；应为 20 行。
-- TODO:

-- 题 10（改错）：下面条件把员工编号错误地连到部门编号。
-- 错误 SQL：SELECT e.employee_name, d.department_name
--           FROM dbo.employees AS e
--           INNER JOIN dbo.departments AS d ON d.department_id = e.employee_id;
-- 修正后应为 20 行且部门对应正确。TODO:

/*
每日自检
[ ] 我能根据主外键写 JOIN。
[ ] 我能解释每个 JOIN 的目标。
[ ] 我能预测连接后的大致行数。
[ ] 我理解漏写或连错 ON 的影响。
[ ] 我能说明本课为什么使用 INNER JOIN。
[ ] 我检查了 NULL 和一名员工多项目造成的重复显示。
[ ] 我写下了今天最容易错的知识点。
*/
