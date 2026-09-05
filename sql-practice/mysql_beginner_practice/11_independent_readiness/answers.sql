USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 第 1 题参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    project_status,
    end_date,
    budget
FROM projects
WHERE end_date IS NULL
  AND project_status IN ('待启动', '暂停')
ORDER BY
    budget DESC,
    project_id ASC;

-- 为什么这样写：
-- IS NULL 检查缺失结束日期，IN 限定两个目标状态。
-- 验证：
-- 共 5 列；end_date 全为空；预算降序且并列时编号升序。

-- ==================================================
-- 第 2 题参考答案
-- ==================================================

SELECT
    project_status,
    COUNT(*) AS project_count,
    COUNT(end_date) AS projects_with_end_date,
    AVG(budget) AS average_budget
FROM projects
GROUP BY project_status
HAVING COUNT(*) >= 3
ORDER BY
    project_count DESC,
    project_status ASC;

-- 为什么这样写：
-- COUNT(*) 统计组内全部项目，COUNT(end_date) 只统计非 NULL 日期。
-- HAVING 在分组后筛选项目数不少于 3 的状态。
-- 验证：
-- projects_with_end_date 不大于 project_count。

-- ==================================================
-- 第 3 题参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    d.department_name,
    e.employee_name AS manager_name,
    p.project_status
FROM projects AS p
INNER JOIN departments AS d
    ON d.department_id = p.department_id
INNER JOIN employees AS e
    ON e.employee_id = p.project_manager_id
ORDER BY
    d.department_id ASC,
    p.project_id ASC;

-- 为什么这样写：
-- 两个 INNER JOIN 只保留同时有部门和经理匹配的项目。
-- 验证：
-- 每个项目最多一行，无经理项目不会返回。

-- ==================================================
-- 第 4 题参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    COUNT(DISTINCT ep.employee_id) AS participant_count,
    CASE
        WHEN MAX(pm.investment_return_rate) IS NULL THEN '收益率缺失'
        ELSE '收益率已填'
    END AS roi_status
FROM projects AS p
LEFT JOIN employee_projects AS ep
    ON ep.project_id = p.project_id
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
GROUP BY
    p.project_id,
    p.project_name
HAVING COUNT(DISTINCT ep.employee_id) = 0
    OR MAX(pm.investment_return_rate) IS NULL
ORDER BY p.project_id ASC;

-- 为什么这样写：
-- LEFT JOIN 保留所有项目，DISTINCT 防止重复计数。
-- MAX(investment_return_rate) 用于判断组内收益率是否缺失。
-- 验证：
-- 每个项目一行，至少缺少参与人员或收益率中的一种。
-- 应包含有参与人员但收益率缺失的项目，证明 OR 不能误写成 AND。

-- ==================================================
-- 第 5 题参考答案
-- ==================================================

WITH project_analysis AS
(
    SELECT
        p.project_id,
        p.project_name,
        d.department_name,
        pm.investment_return_rate,
        pm.management_fee
    FROM projects AS p
    INNER JOIN departments AS d
        ON d.department_id = p.department_id
    INNER JOIN project_metrics AS pm
        ON pm.project_id = p.project_id
)
SELECT
    project_id,
    project_name,
    department_name,
    investment_return_rate,
    COALESCE(management_fee, 0) AS management_fee,
    CASE
        WHEN investment_return_rate >
             (
                 SELECT AVG(investment_return_rate)
                 FROM project_metrics
                 WHERE investment_return_rate IS NOT NULL
             )
        THEN '高于平均'
        ELSE '未高于平均'
    END AS roi_level
FROM project_analysis
WHERE investment_return_rate >
      (
          SELECT AVG(investment_return_rate)
          FROM project_metrics
          WHERE investment_return_rate IS NOT NULL
      )
ORDER BY
    investment_return_rate DESC,
    project_id ASC;

-- 为什么这样写：
-- CTE 先组织三张表，标量子查询计算非空 ROI 平均值。
-- WHERE 只保留严格高于平均值的项目。
-- 验证：
-- ROI 无 NULL，每行标签为“高于平均”，每个项目最多一行。

-- ==================================================
-- 第 6 题参考答案
-- ==================================================

USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

START TRANSACTION;

INSERT INTO departments
    (department_id, department_name, city)
VALUES
    (9301, '独立测评部门', '测试城市A');

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

UPDATE departments
SET city = '测试城市B'
WHERE department_id = 9301;

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

DELETE FROM departments
WHERE department_id = 9301;

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

ROLLBACK;

SELECT
    department_id,
    department_name,
    city
FROM departments
WHERE department_id = 9301;

-- 为什么这样写：
-- UPDATE 和 DELETE 前都使用相同主键条件预览。
-- 所有修改在同一事务中，并以 ROLLBACK 结束。
-- 验证：
-- 最后查询应为 0 行，verify_database.sql 仍应显示 PASS。
