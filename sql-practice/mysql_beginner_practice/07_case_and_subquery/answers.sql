USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================

SELECT
    project_name,
    budget,
    CASE
        WHEN budget >= 900000 THEN '高预算'
        WHEN budget >= 500000 THEN '中预算'
        ELSE '低预算'
    END AS budget_level
FROM projects
ORDER BY
    budget DESC,
    project_id ASC;

-- 为什么这样写：
-- 只调整高预算门槛，仍先判断更高门槛。
-- 预期结果特征：
-- 3 列，每个项目一个预算等级。
-- 验证方法：
-- 抽查 900000 和 500000 附近的值。
-- 常见错误：
-- 把中预算条件写在高预算条件前。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    end_date,
    CASE
        WHEN end_date IS NULL THEN '待确定'
        ELSE '已确定'
    END AS end_date_status
FROM projects
ORDER BY project_id;

-- 为什么这样写：
-- 只更换显示标签，空值判断和原字段保持不变。
-- 预期结果特征：
-- 4 列，空日期显示“待确定”。
-- 验证方法：
-- 分别抽查空和非空日期，确认原字段未修改。
-- 常见错误：
-- 写成 end_date = NULL。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================

SELECT
    project_name,
    budget,
    (
        SELECT AVG(budget)
        FROM projects
    ) AS average_budget
FROM projects
ORDER BY project_id;

-- 为什么这样写：
-- 子查询聚合全部项目预算并只返回一个平均值。
-- 预期结果特征：
-- 3 列，每个项目一行，平均预算列每行相同。
-- 验证方法：
-- 单独运行子查询，确认一行一列。
-- 常见错误：
-- 子查询直接返回 budget 明细。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================

SELECT
    employee_id,
    employee_name,
    salary
FROM employees
WHERE salary < (
    SELECT AVG(salary)
    FROM employees
)
ORDER BY
    salary ASC,
    employee_id ASC;

-- 为什么这样写：
-- 小于平均值使用 `<`，升序让最低薪资先显示。
-- 预期结果特征：
-- 3 列，每行薪资严格低于平均值。
-- 验证方法：
-- 单独计算平均值并检查最大返回薪资。
-- 常见错误：
-- 只改排序方向，没有把比较符改成 `<`。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================

SELECT
    employee_id,
    employee_name,
    department_id
FROM employees
WHERE department_id IN (
    SELECT department_id
    FROM projects
    WHERE budget >= 1000000
)
ORDER BY employee_id;

-- 为什么这样写：
-- 只提高子查询预算门槛，外层仍按部门编号集合筛选。
-- 预期结果特征：
-- 3 列，只包含门槛内项目所属部门的员工。
-- 验证方法：
-- 先运行子查询，再核对每名员工部门编号。
-- 常见错误：
-- 子查询返回项目编号而不是部门编号。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================

SELECT
    employee_name,
    salary,
    CASE
        WHEN salary >= 15000 THEN '较高'
        ELSE '普通'
    END AS salary_level
FROM employees
ORDER BY employee_id;

-- 为什么这样写：
-- 一个 WHEN 处理门槛，ELSE 覆盖其余员工。
-- 预期结果特征：
-- 3 列，每名员工一行且都有分类。
-- 常见错误：
-- 使用 `>` 导致正好 15000 分类错误。
-- 验证方法：
-- 抽查边界值和两类结果。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================

SELECT
    metric_id,
    voltage_level,
    CASE
        WHEN voltage_level IS NULL THEN '缺失'
        ELSE '已填写'
    END AS voltage_status
FROM project_metrics
ORDER BY metric_id;

-- 为什么这样写：
-- IS NULL 正确识别空电压等级。
-- 预期结果特征：
-- 3 列，每条指标记录一行。
-- 常见错误：
-- 使用 voltage_level = NULL。
-- 验证方法：
-- 分别检查 NULL 和非 NULL 样本。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================

SELECT
    project_id,
    management_fee,
    CASE
        WHEN management_fee IS NULL THEN '未知'
        WHEN management_fee >= 0.20 THEN '较高'
        ELSE '普通'
    END AS fee_level
FROM project_metrics
ORDER BY project_id;

-- 为什么这样写：
-- 先单独处理 NULL，再判断数值门槛，ELSE 覆盖其他数值。
-- 预期结果特征：
-- 3 列，每条指标记录都有清楚分类。
-- 常见错误：
-- 没有处理 NULL，使结果分类含义不清。
-- 验证方法：
-- 抽查 NULL、0.20 和较低值。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    budget
FROM projects
WHERE budget > (
    SELECT AVG(budget)
    FROM projects
)
ORDER BY
    budget DESC,
    project_id ASC;

-- 为什么这样写：
-- 子查询返回一个平均预算，外层返回严格高于它的项目。
-- 预期结果特征：
-- 3 列，每个预算都高于平均值。
-- 常见错误：
-- 子查询返回多行预算。
-- 验证方法：
-- 单独运行平均值并检查外层最低预算。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================

SELECT
    department_id,
    department_name
FROM departments
WHERE department_id IN (
    SELECT department_id
    FROM projects
    WHERE budget >= 1000000
)
ORDER BY department_id;

-- 为什么这样写：
-- 子查询返回符合预算条件的部门编号集合，外层查询部门明细。
-- 预期结果特征：
-- 2 列，每个符合条件的部门一行。
-- 常见错误：
-- 子查询返回项目编号。
-- 验证方法：
-- 比较子查询编号与外层部门编号。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================

SELECT
    project_id,
    project_name,
    project_status,
    CASE
        WHEN project_status = '已完成' THEN '已结束'
        WHEN end_date IS NULL THEN '日期待定'
        ELSE '有计划日期'
    END AS progress_label
FROM projects
ORDER BY project_id;

-- 为什么这样写：
-- CASE 从上到下匹配，所以先处理业务优先级更高的已完成状态。
-- 预期结果特征：
-- 4 列，每个项目只命中一个标签。
-- 常见错误：
-- 先判断日期，导致已完成项目被错误分类。
-- 验证方法：
-- 分别抽查三个分支和边界情况。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================

SELECT
    employee_id,
    employee_name,
    department_id
FROM employees
WHERE department_id IN (
    SELECT p.department_id
    FROM projects AS p
    INNER JOIN project_metrics AS pm
        ON p.project_id = pm.project_id
    WHERE pm.investment_return_rate >= 0.0850
)
ORDER BY employee_id;

-- 为什么这样写：
-- 子查询先找高收益项目所属部门，外层按部门筛选员工。
-- 预期结果特征：
-- 3 列，每名符合条件的员工一行。
-- 常见错误：
-- 子查询返回收益率和部门编号两列。
-- 验证方法：
-- 单独运行子查询并核对员工部门，检查重复。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================

SELECT
    employee_name,
    salary
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
);

-- 是否报错：
-- 原子查询返回多行薪资，MySQL 会报告子查询返回多于一行。
-- 结果是否正确：
-- 无法得到目标结果，因为 `>` 右侧需要一个值。
-- 如何修改：
-- 使用 AVG 把所有薪资汇总为一行一列的平均值。
-- 修改后特征：
-- 2 列，每行薪资严格高于公司平均薪资。
-- 预期结果特征：
-- 返回部分员工，不包含等于或低于平均值者。
-- 常见错误：
-- 只加 LIMIT 1，得到任意一个员工薪资而不是平均值。
-- 验证方法：
-- 单独运行子查询并逐行比较外层薪资。
