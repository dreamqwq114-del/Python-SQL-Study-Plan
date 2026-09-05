USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    e.job_title,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON e.department_id = d.department_id
ORDER BY e.employee_id;

-- 为什么这样写：
-- 只在原结果列中增加 e.job_title，连接关系不变。
-- 预期结果特征：
-- 4 列，每名匹配员工一行。
-- 验证方法：
-- 检查列标题、员工编号顺序和行数。
-- 常见错误：
-- 把 job_title 误写成部门表字段。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    p.project_status,
    d.department_name
FROM projects AS p
INNER JOIN departments AS d
    ON p.department_id = d.department_id
ORDER BY p.project_id;

-- 为什么这样写：
-- project_status 来自项目表，原连接和排序无需改变。
-- 预期结果特征：
-- 4 列，每个匹配项目一行。
-- 验证方法：
-- 检查项目编号顺序以及是否有异常重复。
-- 常见错误：
-- 写成 d.project_status。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    p.project_status,
    e.employee_name AS manager_name
FROM projects AS p
INNER JOIN employees AS e
    ON p.project_manager_id = e.employee_id
ORDER BY p.project_id;

-- 为什么这样写：
-- 增加项目表中的状态列，不改变经理连接条件。
-- 预期结果特征：
-- 4 列，只包含能匹配经理的项目。
-- 验证方法：
-- 与项目总数比较行数，确认无经理项目未出现。
-- 常见错误：
-- 为了增加列而错误修改 ON。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_name,
    d.department_name,
    e.employee_name AS manager_name,
    p.budget
FROM projects AS p
INNER JOIN departments AS d
    ON p.department_id = d.department_id
INNER JOIN employees AS e
    ON p.project_manager_id = e.employee_id
ORDER BY
    p.budget DESC,
    p.project_name ASC;

-- 为什么这样写：
-- 预算来自项目表；两条连接关系保持不变，再按题意排序。
-- 预期结果特征：
-- 4 列，预算降序，同预算时项目名称升序。
-- 验证方法：
-- 检查排序、行数和无经理项目是否被排除。
-- 常见错误：
-- 把排序列写成部门或员工字段。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================

SELECT
    p.project_name,
    p.project_status,
    e.employee_name,
    ep.role_name,
    ep.working_hours
FROM employee_projects AS ep
INNER JOIN projects AS p
    ON ep.project_id = p.project_id
INNER JOIN employees AS e
    ON ep.employee_id = e.employee_id
ORDER BY
    p.project_id,
    e.employee_id;

-- 为什么这样写：
-- 只增加项目状态列；中间表的两条连接条件不变。
-- 预期结果特征：
-- 5 列，每行仍代表一条员工—项目关系。
-- 验证方法：
-- 与参与关系总数比较行数，检查项目名称重复的原因。
-- 常见错误：
-- 增加列时误删一个 JOIN。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON e.department_id = d.department_id
ORDER BY e.employee_id;

-- 为什么这样写：
-- 员工的 department_id 外键对应部门的 department_id 主键。
-- 预期结果特征：
-- 3 列，每名匹配员工一行。
-- 常见错误：
-- 连接员工编号和部门编号。
-- 验证方法：
-- 检查员工编号顺序、行数和部门对应关系。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================

SELECT
    p.project_name,
    p.project_status,
    d.department_name
FROM projects AS p
INNER JOIN departments AS d
    ON p.department_id = d.department_id
ORDER BY p.project_id;

-- 为什么这样写：
-- 项目的部门外键用于找到所属部门名称。
-- 预期结果特征：
-- 3 列，每个匹配项目一行。
-- 常见错误：
-- 不限定 department_id 来自哪张表。
-- 验证方法：
-- 与项目总数比较行数，并检查重复。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================

SELECT
    p.project_name,
    e.employee_name AS manager_name,
    p.budget
FROM projects AS p
INNER JOIN employees AS e
    ON p.project_manager_id = e.employee_id
ORDER BY
    p.budget DESC,
    p.project_id ASC;

-- 为什么这样写：
-- 项目经理编号指向员工编号；INNER JOIN 排除无经理项目。
-- 预期结果特征：
-- 3 列，预算降序，行数少于项目总数。
-- 常见错误：
-- 把 project_id 与 employee_id 相连。
-- 验证方法：
-- 检查排序、NULL、行数以及被排除的项目。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    d.department_name,
    e.employee_name AS manager_name
FROM projects AS p
INNER JOIN departments AS d
    ON p.department_id = d.department_id
INNER JOIN employees AS e
    ON p.project_manager_id = e.employee_id
ORDER BY p.project_id;

-- 为什么这样写：
-- 项目分别通过两个外键连接部门和经理。
-- 预期结果特征：
-- 4 列，每个部门和经理都匹配的项目一行。
-- 常见错误：
-- 两个 JOIN 使用同一连接条件。
-- 验证方法：
-- 逐一核对连接条件，并检查遗漏和重复。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================

SELECT
    p.project_name,
    e.employee_name,
    ep.working_hours
FROM employee_projects AS ep
INNER JOIN projects AS p
    ON ep.project_id = p.project_id
INNER JOIN employees AS e
    ON ep.employee_id = e.employee_id
ORDER BY
    p.project_id,
    e.employee_id;

-- 为什么这样写：
-- 中间表分别保存项目和员工外键，也保存该关系的工时。
-- 预期结果特征：
-- 3 列，每行是一条参与关系。
-- 常见错误：
-- 把项目名称重复误判为错误数据。
-- 验证方法：
-- 与参与关系行数比较，并检查员工—项目组合。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================

SELECT
    e.employee_id,
    e.employee_name,
    p.project_name,
    ep.role_name
FROM employees AS e
INNER JOIN employee_projects AS ep
    ON e.employee_id = ep.employee_id
INNER JOIN projects AS p
    ON ep.project_id = p.project_id
ORDER BY
    e.employee_id,
    p.project_id;

-- 为什么这样写：
-- INNER JOIN 只返回有参与记录的员工，中间表提供参与角色。
-- 预期结果特征：
-- 4 列，同一员工可有多行，无项目员工不出现。
-- 常见错误：
-- 使用 DISTINCT 抹掉不同项目关系。
-- 验证方法：
-- 检查无项目员工、重复原因和排序。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================

SELECT
    p.project_id,
    p.project_name,
    pm.management_fee,
    pm.investment_return_rate
FROM projects AS p
INNER JOIN project_metrics AS pm
    ON p.project_id = pm.project_id
ORDER BY p.project_id;

-- 为什么这样写：
-- project_metrics.project_id 指向项目主键，INNER JOIN 只保留有指标记录的项目。
-- 预期结果特征：
-- 4 列，行数少于项目总数；指标值本身可能为 NULL。
-- 常见错误：
-- 认为连接成功就保证每个指标字段都非 NULL。
-- 验证方法：
-- 检查缺失项目、行数和指标列中的 NULL。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================

SELECT
    e.employee_name,
    d.department_name
FROM employees AS e
INNER JOIN departments AS d
    ON e.department_id = d.department_id;

-- 是否报错：
-- 原 SQL 字段和语法存在，通常不会报错。
-- 结果是否正确：
-- 不正确。员工编号与部门编号不是“员工属于部门”的关系。
-- 如何修改：
-- 用员工的 department_id 外键连接部门的 department_id 主键。
-- 修改后特征：
-- 2 列，每名有匹配部门的员工一行。
-- 预期结果特征：
-- 行数合理，员工对应正确部门。
-- 常见错误：
-- 认为字段类型相同就可以连接。
-- 验证方法：
-- 比较员工总数并抽查多个部门的员工。
