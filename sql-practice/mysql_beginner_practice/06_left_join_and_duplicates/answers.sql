USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    pm.voltage_level,
    pm.management_fee
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
ORDER BY p.project_id;

-- 为什么这样写：
-- 只增加右表的管理费列，LEFT JOIN 仍保留全部项目。
-- 预期结果特征：
-- 4 列，无指标项目的两个指标列都为 NULL。
-- 验证方法：
-- 检查项目覆盖范围和右表 NULL。
-- 常见错误：
-- 为了增加列而把连接改成 INNER JOIN。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    p.project_name,
    ep.role_name
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.employee_id = ep.employee_id
LEFT JOIN projects AS p
    ON ep.project_id = p.project_id
ORDER BY
    e.employee_id,
    p.project_id;

-- 为什么这样写：
-- 角色属于员工—项目关系，因此来自中间表。
-- 预期结果特征：
-- 4 列，无项目员工的项目和角色都为 NULL。
-- 验证方法：
-- 检查无项目员工和多项目员工。
-- 常见错误：
-- 把 role_name 当成员工表字段。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
WHERE pm.project_id IS NULL
ORDER BY p.project_id;

-- 为什么这样写：
-- 右表连接键为 NULL 表示项目没有指标记录。
-- 预期结果特征：
-- 2 列，只包含无指标项目。
-- 验证方法：
-- 在 project_metrics 中核对这些项目编号不存在。
-- 常见错误：
-- 写成 pm.project_id = NULL。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    e.employee_id,
    e.employee_name,
    ep.working_hours
FROM projects AS p
INNER JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
INNER JOIN employees AS e
    ON ep.employee_id = e.employee_id
WHERE p.project_id = 1
ORDER BY e.employee_id;

-- 为什么这样写：
-- 工时属于参与关系；每行仍由项目和员工组合区分。
-- 预期结果特征：
-- 5 列，每名项目 1 的参与员工一行。
-- 验证方法：
-- 检查员工编号唯一以及工时与参与记录一致。
-- 常见错误：
-- 使用 DISTINCT 删除不同员工行。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================

SELECT
    d.department_name,
    COUNT(DISTINCT p.project_id) AS project_count,
    COUNT(ep.employee_id) AS participation_count,
    COUNT(DISTINCT ep.employee_id) AS employee_count
FROM departments AS d
LEFT JOIN projects AS p
    ON d.department_id = p.department_id
LEFT JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
GROUP BY
    d.department_id,
    d.department_name
ORDER BY d.department_id;

-- 为什么这样写：
-- 对员工编号去重，避免同一员工参加同部门多个项目时被重复计数。
-- 预期结果特征：
-- 每个部门一行，并显示三种含义不同的计数。
-- 验证方法：
-- 抽查原始参与关系，比较参与行数和不重复员工数。
-- 常见错误：
-- 用 COUNT(ep.employee_id) 作为不重复员工数。

-- ==================================================
-- 示例 6 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    pm.voltage_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
WHERE pm.voltage_level = '110kV'
ORDER BY p.project_id;

SELECT
    p.project_id,
    p.project_name,
    pm.voltage_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON pm.project_id = p.project_id
   AND pm.voltage_level = '110kV'
ORDER BY p.project_id;

-- 为什么这样写：
-- 第一条在连接后筛选，第二条只限制右表匹配，因此保留范围不同。
-- 预期结果特征：
-- 第一条只返回匹配项目；第二条保留全部项目并用 NULL 表示不匹配。
-- 验证方法：
-- 比较两个结果集的行数、项目编号和 NULL。
-- 常见错误：
-- 认为条件从 WHERE 移到 ON 不会改变结果含义。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    pm.investment_return_rate
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
ORDER BY p.project_id;

-- 为什么这样写：
-- 项目放在左边，保证无指标项目仍被保留。
-- 预期结果特征：
-- 3 列，覆盖全部项目，收益率可能为 NULL。
-- 常见错误：
-- 使用 INNER JOIN 丢掉无指标项目。
-- 验证方法：
-- 比较项目覆盖范围并检查 NULL。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    ep.project_id,
    ep.role_name
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.employee_id = ep.employee_id
ORDER BY
    e.employee_id,
    ep.project_id;

-- 为什么这样写：
-- LEFT JOIN 保留无项目员工；项目编号和角色都在中间表。
-- 预期结果特征：
-- 4 列，一名员工可多行，无项目员工右表列为 NULL。
-- 常见错误：
-- 使用 INNER JOIN 排除无项目员工。
-- 验证方法：
-- 检查无项目员工和重复原因。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
WHERE pm.project_id IS NULL
ORDER BY p.project_id;

-- 为什么这样写：
-- 项目保留后，右表连接键为空表示没有指标行。
-- 预期结果特征：
-- 2 列，只包含无指标项目。
-- 常见错误：
-- 检查允许为空的 investment_return_rate，误选已有指标的项目。
-- 验证方法：
-- 在指标表中核对项目编号不存在。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    e.job_title
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.employee_id = ep.employee_id
WHERE ep.employee_id IS NULL
ORDER BY e.employee_id;

-- 为什么这样写：
-- 中间表员工编号为空说明没有任何参与记录。
-- 预期结果特征：
-- 3 列，只包含无项目员工。
-- 常见错误：
-- 写成 e.employee_id IS NULL。
-- 验证方法：
-- 在 employee_projects 中核对这些员工编号不存在。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================

SELECT
    d.department_name,
    COUNT(DISTINCT p.project_id) AS project_count
FROM departments AS d
LEFT JOIN projects AS p
    ON d.department_id = p.department_id
LEFT JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
GROUP BY
    d.department_id,
    d.department_name
ORDER BY d.department_id;

-- 为什么这样写：
-- 参与表会重复项目编号，DISTINCT 保证每个项目只计一次。
-- 预期结果特征：
-- 2 列，每个部门一行。
-- 常见错误：
-- 使用 COUNT(p.project_id) 导致多人项目重复计数。
-- 验证方法：
-- 与 projects 直接按部门统计的结果比较。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    COUNT(ep.project_id) AS project_count
FROM employees AS e
LEFT JOIN employee_projects AS ep
    ON e.employee_id = ep.employee_id
GROUP BY
    e.employee_id,
    e.employee_name
ORDER BY e.employee_id;

-- 为什么这样写：
-- COUNT(ep.project_id) 不统计无匹配时产生的 NULL，所以无项目员工为 0。
-- 预期结果特征：
-- 3 列，每名员工一行。
-- 常见错误：
-- 使用 COUNT(*) 使无项目员工被计为 1。
-- 验证方法：
-- 抽查无项目和多项目员工。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    COUNT(DISTINCT ep.employee_id) AS employee_count
FROM projects AS p
LEFT JOIN employee_projects AS ep
    ON p.project_id = ep.project_id
GROUP BY
    p.project_id,
    p.project_name
ORDER BY
    employee_count DESC,
    p.project_id ASC;

-- 为什么这样写：
-- LEFT JOIN 保留无参与项目，对员工编号去重后按项目分组。
-- 预期结果特征：
-- 3 列，每个项目一行，无参与项目为 0。
-- 常见错误：
-- 使用 INNER JOIN 丢掉零参与项目。
-- 验证方法：
-- 检查零值、项目覆盖范围和降序。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================

SELECT
    p.project_name,
    pm.voltage_level
FROM projects AS p
LEFT JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
   AND pm.voltage_level = '110kV';

-- 是否报错：
-- 原 SQL 语法完整，通常不会报错。
-- 结果是否正确：
-- 不正确。WHERE 会排除右表为 NULL 的行，无法保留全部项目。
-- 如何修改：
-- 把电压条件移到 ON，限制右表匹配而不删除左表行。
-- 修改后特征：
-- 全部项目保留；只有 110kV 匹配显示值，其余为 NULL。
-- 预期结果特征：
-- 2 列，项目覆盖范围与项目总数一致。
-- 常见错误：
-- 保留 WHERE 条件并以为 LEFT JOIN 一定保留全部左表行。
-- 验证方法：
-- 比较项目覆盖范围，检查非 110kV 项目的右表列。
