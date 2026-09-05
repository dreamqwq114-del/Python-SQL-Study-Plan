USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

-- 题 1：CASE 两档分类；无 JOIN。
SELECT employee_name,
       CASE WHEN salary >= 15000 THEN '高' ELSE '普通' END AS salary_level
FROM employees;

-- 题 2：标量子查询返回一个平均预算；无 JOIN。
SELECT project_name, budget
FROM projects
WHERE budget > (SELECT AVG(budget) FROM projects);

-- 题 3：LEFT JOIN 后检查指标主键 NULL；结果为两个无指标项目。
SELECT p.project_id, p.project_name
FROM projects AS p
LEFT JOIN project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.project_id IS NULL;

-- 题 4：CTE 只是给第一步结果命名，不递归；无 JOIN。
WITH active_projects AS
(
    SELECT project_name, budget
    FROM projects
    WHERE project_status = '进行中'
)
SELECT project_name, budget
FROM active_projects;

-- 题 5：EXISTS 内层用 project_id 关联外层；只判断是否存在，不扩张行。
SELECT p.project_id, p.project_name
FROM projects AS p
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
);

-- 题 6：NOT EXISTS 保留没有关系行的项目；不会产生重复。
SELECT p.project_id, p.project_name
FROM projects AS p
WHERE NOT EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.project_id = p.project_id
);

-- 题 7：先去掉 kV，再检查是否为数字；不符合格式时为 NULL。
SELECT voltage_level,
       CASE
           WHEN REPLACE(voltage_level, 'kV', '')
                REGEXP '^[0-9]+([.][0-9]+)?$'
           THEN CAST(REPLACE(voltage_level, 'kV', '') AS DECIMAL(10, 2))
           ELSE NULL
       END AS voltage_number
FROM project_metrics;

-- 题 8：IFNULL 只替换 NULL 经理编号；无 JOIN。
SELECT project_name, IFNULL(project_manager_id, 0) AS manager_id_display
FROM projects;

-- 题 9：直接 CAST 可能把无效文字变成 0 并产生警告。
-- 错误 SQL：SELECT CAST(voltage_level AS SIGNED) FROM project_metrics;
-- 先去掉 kV，再检查纯整数格式；不符合时明确返回 NULL。
SELECT voltage_level,
       CASE
           WHEN REPLACE(voltage_level, 'kV', '') REGEXP '^[+-]?[0-9]+$'
           THEN CAST(REPLACE(voltage_level, 'kV', '') AS SIGNED)
           ELSE NULL
       END AS voltage_as_int
FROM project_metrics;

-- 题 10：错误子查询没有引用外层员工，所以对所有员工结果相同。
-- 用 employee_id 关联后，EXISTS 每名员工独立判断；不扩张重复。
SELECT e.employee_name
FROM employees AS e
WHERE EXISTS
(
    SELECT 1
    FROM employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);
