USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================

SELECT
    d.department_id,
    d.department_name,
    COUNT(p.project_id) AS project_count
FROM departments AS d
LEFT JOIN projects AS p ON p.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id ASC;

-- 为什么这样写：从部门左连接项目，计数非空项目编号。
-- 预期结果特征：每部门一行，无项目部门计数为 0。
-- 验证方法：项目数总和应等于项目总数。
-- 常见错误：使用 COUNT(*)。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    COALESCE(e.employee_name, '未分配') AS project_manager,
    p.project_status,
    p.budget
FROM projects AS p
LEFT JOIN employees AS e ON e.employee_id = p.project_manager_id
ORDER BY p.budget DESC, p.project_id ASC;

-- 为什么这样写：左连接保留无经理项目，并按预算稳定排序。
-- 预期结果特征：每项目一行，共 5 列。
-- 验证方法：检查无经理项目、预算方向和重复。
-- 常见错误：改用内连接。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    COUNT(DISTINCT ep.employee_id) AS participant_count,
    COALESCE(SUM(ep.working_hours), 0) AS total_working_hours
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name
HAVING COUNT(DISTINCT ep.employee_id) >= 3
ORDER BY participant_count DESC, p.project_id ASC;

-- 为什么这样写：HAVING 在分组后筛选参与人数。
-- 预期结果特征：只含至少 3 名参与者的项目，每项目一行。
-- 验证方法：对照参与明细并检查并列排序。
-- 常见错误：把聚合条件写在 WHERE。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    p.budget,
    p.budget * pm.management_fee AS management_fee_amount,
    CASE
        WHEN pm.investment_return_rate IS NULL THEN '缺少收益率'
        WHEN pm.investment_return_rate >= 0.085 THEN '收益率较高'
        ELSE '收益率低于 8.5%'
    END AS return_level
FROM projects AS p
LEFT JOIN project_metrics AS pm ON pm.project_id = p.project_id
ORDER BY p.project_id ASC;

-- 为什么这样写：先处理 NULL，再以 0.085 作为比较门槛。
-- 预期结果特征：所有项目保留，缺失指标单独显示。
-- 验证方法：抽查门槛两侧和 NULL。
-- 常见错误：把 0.085 当成 0.085%。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================

WITH project_voltage AS
(
    SELECT
        p.project_id,
        p.budget,
        COALESCE(pm.voltage_level, '未填写') AS voltage_level
    FROM projects AS p
    LEFT JOIN project_metrics AS pm ON pm.project_id = p.project_id
)
SELECT
    voltage_level,
    COUNT(project_id) AS project_count,
    SUM(budget) AS total_budget,
    AVG(budget) AS average_budget
FROM project_voltage
GROUP BY voltage_level
ORDER BY voltage_level ASC;

-- 为什么这样写：CTE 保持每项目一行，再按电压等级聚合。
-- 预期结果特征：每个电压等级一行，共 4 列。
-- 验证方法：项目数总和等于项目总数，并手工核对一组平均值。
-- 常见错误：在 CTE 中漏掉 budget。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================

SELECT
    d.department_id,
    d.department_name,
    COUNT(p.project_id) AS project_count
FROM departments AS d
LEFT JOIN projects AS p ON p.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY d.department_id ASC;

-- 为什么这样写：LEFT JOIN 保留部门，COUNT(项目编号) 不统计空匹配。
-- 预期结果特征：每部门一行，共 3 列。
-- 常见错误：COUNT(*) 让无项目部门计为 1。
-- 验证方法：汇总 project_count 并与项目总数比较。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    COALESCE(e.employee_name, '未分配') AS project_manager,
    p.budget
FROM projects AS p
LEFT JOIN employees AS e ON e.employee_id = p.project_manager_id
ORDER BY p.budget DESC, p.project_id ASC;

-- 为什么这样写：经理可能为空，因此从项目左连接员工。
-- 预期结果特征：所有项目，每项目一行，共 4 列。
-- 常见错误：用部门编号连接员工。
-- 验证方法：检查无经理项目、行数和预算排序。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================

SELECT
    project_status,
    COUNT(project_id) AS project_count,
    SUM(budget) AS total_budget
FROM projects
GROUP BY project_status
HAVING COUNT(project_id) >= 3
ORDER BY total_budget DESC, project_status ASC;

-- 为什么这样写：先按状态聚合，再用 HAVING 筛选项目数。
-- 预期结果特征：每种符合条件状态一行，共 3 列。
-- 常见错误：把 COUNT 条件写在 WHERE。
-- 验证方法：对照每种状态的项目明细和预算。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    p.project_status,
    COUNT(DISTINCT ep.employee_id) AS participant_count
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name, p.project_status
HAVING COUNT(DISTINCT ep.employee_id) >= 3
ORDER BY participant_count DESC, p.project_id ASC;

-- 为什么这样写：按项目分组并对员工编号去重计数。
-- 预期结果特征：每个符合条件项目一行，共 4 列。
-- 常见错误：遗漏状态分组列。
-- 验证方法：对照参与明细，检查项目 1 等多人项目。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    project_status,
    end_date,
    CASE
        WHEN project_status = '暂停' THEN '需关注'
        WHEN end_date IS NULL THEN '日期待定'
        ELSE '正常检查'
    END AS risk_label
FROM projects
ORDER BY project_id ASC;

-- 为什么这样写：CASE 按题目顺序优先标记暂停项目。
-- 预期结果特征：所有项目，每项目一行，共 5 列。
-- 常见错误：用 end_date = NULL。
-- 验证方法：分别抽查三类项目。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================

SELECT
    d.department_id,
    d.department_name,
    COUNT(p.project_id) AS project_count,
    COALESCE(SUM(p.budget), 0) AS total_budget
FROM departments AS d
LEFT JOIN projects AS p ON p.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY total_budget DESC, d.department_id ASC;

-- 为什么这样写：只在部门与项目粒度聚合，避免人员连接放大预算。
-- 预期结果特征：每部门一行，共 4 列。
-- 常见错误：再连接参与表后直接 SUM(budget)。
-- 验证方法：项目数总和及预算总和与项目表核对。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    p.project_status,
    CASE
        WHEN NOT EXISTS
        (
            SELECT 1
            FROM employee_projects AS ep
            WHERE ep.project_id = p.project_id
        ) THEN '无人参与'
        ELSE '已有人员'
    END AS participant_status,
    CASE
        WHEN NOT EXISTS
        (
            SELECT 1
            FROM project_metrics AS pm
            WHERE pm.project_id = p.project_id
        ) THEN '无指标'
        ELSE '已有指标'
    END AS metric_status
FROM projects AS p
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
)
OR NOT EXISTS
(
    SELECT 1
    FROM project_metrics AS pm
    WHERE pm.project_id = p.project_id
)
ORDER BY p.project_id ASC;

-- 为什么这样写：两个存在性判断不会制造一对多重复，OR 保留任一资料缺失项目。
-- 预期结果特征：每项目一行，共 5 列。
-- 常见错误：把 OR 写成 AND，漏掉只缺一类资料的项目。
-- 验证方法：分别反查参与表和指标表。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    budget AS project_budget
FROM projects
ORDER BY project_id ASC;

-- 是否报错：原 SQL 语法通常不报错。
-- 结果是否正确：不正确；多人项目的预算被按参与记录重复求和，
-- 且无参与人员项目因内连接而丢失。
-- 为什么这样修改：题目只需要项目本身的预算，无需连接或聚合。
-- 预期结果特征：所有项目，每项目一行，预算等于 projects 原值。
-- 常见错误：用 DISTINCT 或 MAX 掩盖不必要的连接。
-- 验证方法：抽查项目 1，并检查无参与人员项目仍在。
