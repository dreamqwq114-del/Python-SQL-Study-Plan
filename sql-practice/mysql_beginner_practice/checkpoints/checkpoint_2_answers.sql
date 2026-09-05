USE mysql_beginner_practice;

-- ==================================================
-- 题 1 参考答案
-- ==================================================

SELECT
    p.project_name,
    d.department_name
FROM projects AS p
INNER JOIN departments AS d
    ON d.department_id = p.department_id;

-- 验证：每个项目匹配一个负责部门。

-- ==================================================
-- 题 2 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
WHERE pm.project_id IS NULL;

-- 验证：返回的项目在 project_metrics 中没有匹配行。

-- ==================================================
-- 题 3 参考答案
-- ==================================================

SELECT
    e.department_id,
    COUNT(DISTINCT ep.employee_id) AS distinct_employee_count
FROM employees AS e
INNER JOIN employee_projects AS ep
    ON ep.employee_id = e.employee_id
GROUP BY e.department_id
ORDER BY e.department_id;

-- 验证：同一员工参加多个项目时，在本部门只计一次。

-- ==================================================
-- 题 4 参考答案
-- ==================================================

SELECT
    project_name,
    CASE
        WHEN project_status = '已完成' THEN '结束'
        ELSE '未结束'
    END AS status_group
FROM projects;

-- 验证：每个项目一行，分类没有 NULL。

-- ==================================================
-- 题 5 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
);

-- 验证：每个返回项目至少能在 employee_projects 找到一行。

-- ==================================================
-- 题 6 参考答案
-- ==================================================

WITH metric_view AS
(
    SELECT
        p.project_name,
        pm.investment_return_rate,
        pm.voltage_level
    FROM projects AS p
    LEFT JOIN project_metrics AS pm
        ON pm.project_id = p.project_id
)
SELECT
    project_name,
    CAST(investment_return_rate AS CHAR) AS roi_text,
    COALESCE(voltage_level, '未填写') AS voltage_display
FROM metric_view;

-- 验证：所有项目都保留，NULL 电压等级显示为“未填写”。
