USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================
SELECT
    COUNT(*) AS employee_count,
    COUNT(manager_id) AS employees_with_manager
FROM employees;
-- 为什么这样写：星号统计所有员工，字段计数忽略 manager_id 为 NULL 的行。
-- 预期结果特征：1 行 2 列，第二个计数不大于第一个。
-- 验证方法：用 manager_id IS NULL 的行数解释差值。
-- 常见错误：写 COUNT('manager_id')。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================
SELECT
    SUM(budget) AS total_budget,
    AVG(budget) AS average_budget,
    MIN(budget) AS minimum_budget,
    MAX(budget) AS maximum_budget
FROM projects;
-- 为什么这样写：四个函数分别汇总同一预算列。
-- 预期结果特征：1 行 4 列，平均值位于最小值和最大值之间。
-- 验证方法：检查四列数值关系。
-- 常见错误：聚合 project_name。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================
SELECT job_title, COUNT(*) AS employee_count
FROM employees
GROUP BY job_title
ORDER BY employee_count DESC, job_title ASC;
-- 为什么这样写：每个职位成一组，先按人数、再按职位稳定排序。
-- 预期结果特征：每种职位一行。
-- 验证方法：各职位计数相加应等于员工总数。
-- 常见错误：忘记 GROUP BY job_title。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================
SELECT
    project_status,
    COUNT(*) AS project_count,
    SUM(budget) AS total_budget
FROM projects
WHERE start_date >= '2023-01-01'
GROUP BY project_status
ORDER BY total_budget DESC;
-- 为什么这样写：先改日期下限，再按每组总预算降序。
-- 预期结果特征：每个参与汇总的状态一行。
-- 验证方法：核对参与项目日期和总预算方向。
-- 常见错误：把 WHERE 放到 GROUP BY 后。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================
SELECT department_id, AVG(salary) AS average_salary
FROM employees
GROUP BY department_id
HAVING AVG(salary) >= 12000
ORDER BY department_id ASC;
-- 为什么这样写：平均薪资是分组后条件，所以使用 HAVING。
-- 预期结果特征：每行一个部门，平均薪资至少 12000。
-- 验证方法：检查每组平均值下限。
-- 常见错误：在 WHERE 中使用 AVG(salary)。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================
SELECT COUNT(*) AS employee_count
FROM employees;
-- 为什么这样写：COUNT(*) 统计 employees 的全部行。
-- 预期结果特征：1 行 1 列。
-- 常见错误：使用可空字段进行计数。
-- 验证方法：与员工明细行数比较。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================
SELECT
    SUM(budget) AS total_budget,
    AVG(budget) AS average_budget
FROM projects;
-- 为什么这样写：两个聚合函数分别得到预算总和与平均值。
-- 预期结果特征：1 行 2 列。
-- 常见错误：忘记 AS 别名。
-- 验证方法：确认平均值位于预算范围内。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================
SELECT project_status, COUNT(*) AS project_count
FROM projects
GROUP BY project_status
ORDER BY project_count DESC, project_status ASC;
-- 为什么这样写：每个状态一组，先按计数再按状态排序。
-- 预期结果特征：每种状态一行。
-- 常见错误：缺少 GROUP BY。
-- 验证方法：各组计数之和应等于项目总数。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================
SELECT
    department_id,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary
FROM employees
GROUP BY department_id
ORDER BY department_id ASC;
-- 为什么这样写：每个部门分别求薪资最小值和最大值。
-- 预期结果特征：每部门一行，共 3 列。
-- 常见错误：在 SELECT 中加入 employee_name。
-- 验证方法：检查每组 minimum_salary 不大于 maximum_salary。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================
SELECT
    department_id,
    COUNT(*) AS project_count,
    SUM(budget) AS total_budget
FROM projects
WHERE project_status = '进行中'
GROUP BY department_id
ORDER BY department_id ASC;
-- 为什么这样写：WHERE 先排除其他状态，再按部门汇总。
-- 预期结果特征：每个有进行中项目的部门一行。
-- 常见错误：把状态条件写在 HAVING 中代替普通筛选。
-- 验证方法：计数之和与进行中项目明细数比较。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================
SELECT
    job_title,
    COUNT(*) AS employee_count,
    AVG(salary) AS average_salary
FROM employees
GROUP BY job_title
HAVING AVG(salary) >= 12000
ORDER BY average_salary DESC, job_title ASC;
-- 为什么这样写：按职位分组后，用 HAVING 筛选组平均值。
-- 预期结果特征：每行一个达标职位，平均薪资降序。
-- 常见错误：在 WHERE 中使用 AVG。
-- 验证方法：检查每个平均值和并列时职位顺序。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================
SELECT
    COUNT(*) AS metric_count,
    COUNT(management_fee) AS fee_count,
    COUNT(investment_return_rate) AS return_count,
    COUNT(voltage_level) AS voltage_count
FROM project_metrics;
-- 为什么这样写：星号统计全部指标行，字段计数分别忽略各自的 NULL。
-- 预期结果特征：1 行 4 列，三个非空计数不大于总数。
-- 常见错误：以为所有字段非空计数必须相同。
-- 验证方法：用各字段 IS NULL 的数量核对差值。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================
SELECT department_id, COUNT(*) AS employee_count
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 4;
-- 是否报错：原 SQL 会因在 WHERE 中使用聚合函数而报错。
-- 结果是否正确：无法得到目标结果；WHERE 阶段还没有分组计数。
-- 如何修改：先 GROUP BY，再用 HAVING 筛选 COUNT(*)。
-- 修改后特征：每行一个部门，employee_count 至少为 4。
-- 常见错误：只把 HAVING 改名却仍放在 GROUP BY 前。
-- 验证方法：检查每个计数，并与部门员工明细核对。
