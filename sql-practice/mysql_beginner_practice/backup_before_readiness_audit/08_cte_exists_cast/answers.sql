USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================

WITH high_budget_projects AS
(
    SELECT project_id, project_name, budget
    FROM projects
    WHERE budget >= 800000
)
SELECT project_name, budget
FROM high_budget_projects
ORDER BY budget DESC, project_id ASC;

-- 为什么这样写：CTE 先筛选，再由主查询显示和稳定排序。
-- 预期结果特征：只有预算不少于 800000 的项目，共 2 列。
-- 验证方法：检查最低预算、列数和并列预算时的项目编号。
-- 常见错误：CTE 中漏掉主查询排序需要的 project_id。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================

SELECT e.employee_id, e.employee_name
FROM employees AS e
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
)
ORDER BY e.employee_id ASC;

-- 为什么这样写：对子查询逐名员工判断是否至少有一条参与记录。
-- 预期结果特征：只含有项目记录的员工，每人最多一行。
-- 验证方法：抽查参与表，并检查重复。
-- 常见错误：把 ep.project_id 与 e.employee_id 关联。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================

SELECT e.employee_id, e.employee_name
FROM employees AS e
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
)
ORDER BY e.employee_id ASC;

-- 为什么这样写：NOT EXISTS 保留找不到任何参与记录的员工。
-- 预期结果特征：每名结果员工在参与表中匹配数为 0。
-- 验证方法：用员工编号反查 employee_projects。
-- 常见错误：误写成 EXISTS。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================

SELECT
    employee_id,
    CAST(employee_id AS CHAR) AS employee_id_text,
    employee_name
FROM employees
ORDER BY employee_id ASC;

-- 为什么这样写：CAST 只把结果中的编号转换为字符。
-- 预期结果特征：原编号、文本编号和姓名共 3 列。
-- 验证方法：对照两个编号列，并检查原字段类型。
-- 常见错误：使用其他数据库的专有转换函数。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================

SELECT
    project_id,
    COALESCE(investment_return_rate, 0) AS return_rate_display
FROM project_metrics
ORDER BY project_id ASC;

-- 为什么这样写：数值列用数值 0 替代 NULL。
-- 预期结果特征：显示列没有 NULL，每条指标记录一行。
-- 验证方法：检查缺失行的显示值，再确认原字段仍为 NULL。
-- 常见错误：把数值替代值写成说明文本。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================

WITH high_salary_employees AS
(
    SELECT employee_id, employee_name, salary
    FROM employees
    WHERE salary >= 15000
)
SELECT employee_name, salary
FROM high_salary_employees
ORDER BY salary DESC, employee_id ASC;

-- 为什么这样写：CTE 筛选并保留稳定排序所需编号。
-- 预期结果特征：2 列，所有薪资都不少于 15000。
-- 常见错误：主查询引用 CTE 中未选出的 employee_id。
-- 验证方法：检查最低薪资、行数和排序。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================

SELECT p.project_id, p.project_name
FROM projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM project_metrics AS pm
    WHERE pm.project_id = p.project_id
)
ORDER BY p.project_id ASC;

-- 为什么这样写：EXISTS 逐个项目判断指标记录是否存在。
-- 预期结果特征：2 列，每个有指标项目最多一行。
-- 常见错误：漏掉内外层项目编号关联。
-- 验证方法：抽查指标表并确认无重复。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================

SELECT e.employee_id, e.employee_name, e.job_title
FROM employees AS e
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
)
ORDER BY e.employee_id ASC;

-- 为什么这样写：NOT EXISTS 找到参与表中没有匹配的员工。
-- 预期结果特征：3 列，只含未参与项目的员工。
-- 常见错误：用项目编号关联员工编号。
-- 验证方法：反查每名结果员工的参与记录数应为 0。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================

WITH active_projects AS
(
    SELECT project_id, project_name, budget
    FROM projects
    WHERE project_status = '进行中'
)
SELECT project_name, budget
FROM active_projects
ORDER BY budget DESC, project_id ASC;

-- 为什么这样写：CTE 只保留进行中项目，主查询负责显示和排序。
-- 预期结果特征：2 列，预算降序。
-- 常见错误：CTE 中漏掉 project_id。
-- 验证方法：检查状态、列数和排序。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    COALESCE(CAST(project_manager_id AS CHAR), '未分配') AS manager_display
FROM projects
ORDER BY project_id ASC;

-- 为什么这样写：先统一为字符类型，再为 NULL 提供文本。
-- 预期结果特征：所有项目保留，manager_display 没有 NULL。
-- 常见错误：直接混用数字编号和文本却不考虑显示类型。
-- 验证方法：检查无经理项目，并确认原 manager_id 未改变。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================

SELECT p.project_id, p.project_name, p.project_status
FROM projects AS p
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
)
ORDER BY p.project_id ASC;

-- 为什么这样写：NOT EXISTS 表达“没有任何参与记录”。
-- 预期结果特征：3 列，每个项目一行。
-- 常见错误：使用 EXISTS 得到相反结果。
-- 验证方法：在参与表中反查，匹配数应为 0。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================

SELECT
    project_id,
    COALESCE(voltage_level, '未填写') AS voltage_level_display,
    COALESCE(investment_return_rate, 0) AS return_rate_display
FROM project_metrics
ORDER BY project_id ASC;

-- 为什么这样写：两个可空字段按各自数据含义提供替代值。
-- 预期结果特征：3 列，显示列没有 NULL。
-- 常见错误：把数值收益率替代为文字。
-- 验证方法：对照原字段中的 NULL，确认原数据没有变化。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================

SELECT p.project_id, p.project_name
FROM projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
)
ORDER BY p.project_id ASC;

-- 是否报错：原 SQL 语法完整，通常不会报错。
-- 结果是否正确：不正确；只要参与表非空，所有项目都会通过判断。
-- 为什么这样修改：关联项目编号后，子查询才会逐个外层项目判断。
-- 预期结果特征：2 列；无参与人员的项目被排除，每个项目一行。
-- 常见错误：认为能运行就代表逻辑正确。
-- 验证方法：检查无参与人员的项目是否不在结果中。
