USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================
SELECT employee_name, hire_date
FROM employees
ORDER BY hire_date DESC;
-- 为什么这样写：DESC 让较晚日期排在前面。
-- 预期结果特征：2 列，日期从晚到早。
-- 验证方法：检查相邻日期是否递减。
-- 常见错误：只改文字理解，没有修改 ASC。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================
SELECT employee_name, department_id, salary
FROM employees
ORDER BY department_id ASC, salary ASC;
-- 为什么这样写：部门仍升序，同部门内薪资改为升序。
-- 预期结果特征：同一部门中低薪在前。
-- 验证方法：选择一个部门检查其全部薪资。
-- 常见错误：把部门方向也一起改掉。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================
SELECT employee_name, hire_date
FROM employees
WHERE hire_date < '2022-01-01'
ORDER BY hire_date DESC, employee_id ASC;
-- 为什么这样写：严格早于使用 <，DESC 让符合条件中的较晚日期在前。
-- 预期结果特征：无 2022-01-01 及之后日期。
-- 验证方法：检查边界和相邻日期。
-- 常见错误：使用 <=，错误包含边界。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================
SELECT project_name, budget
FROM projects
WHERE budget >= 700000
ORDER BY budget ASC, project_id ASC;
-- 为什么这样写：先筛选下限，再将达标预算从低到高排列。
-- 预期结果特征：预算都达标且升序。
-- 验证方法：检查最小预算和排序方向。
-- 常见错误：把筛选方向也改为 <=。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================
SELECT project_name, project_status, start_date, end_date
FROM projects
WHERE project_status = '进行中'
ORDER BY start_date DESC, project_id ASC;
-- 为什么这样写：文本条件改为进行中，DESC 表示较晚开始日期在前。
-- 预期结果特征：状态统一，开始日期降序。
-- 验证方法：检查状态和相邻日期。
-- 常见错误：对 end_date 排序。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================
SELECT employee_name, salary
FROM employees
ORDER BY salary ASC;
-- 为什么这样写：ASC 表示薪资从低到高。
-- 预期结果特征：2 列，所有员工，薪资升序。
-- 常见错误：使用 DESC。
-- 验证方法：检查所有相邻薪资。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================
SELECT project_name, start_date
FROM projects
ORDER BY start_date DESC;
-- 为什么这样写：DESC 让较晚开始的项目排在前面。
-- 预期结果特征：2 列，日期从晚到早。
-- 常见错误：按 end_date 排序。
-- 验证方法：检查相邻开始日期。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================
SELECT employee_name, department_id, hire_date
FROM employees
ORDER BY department_id ASC, hire_date ASC, employee_name ASC;
-- 为什么这样写：三个规则按部门、日期、姓名的优先级排列。
-- 预期结果特征：部门升序；同部门日期升序；同日姓名升序。
-- 常见错误：排序列间漏写逗号。
-- 验证方法：寻找同部门和同日期的行逐层检查。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================
SELECT project_name, start_date
FROM projects
WHERE start_date >= '2024-01-01'
ORDER BY start_date ASC, project_id ASC;
-- 为什么这样写：>= 包含边界，随后日期和编号均升序。
-- 预期结果特征：没有早于 2024-01-01 的日期。
-- 常见错误：日期漏写单引号。
-- 验证方法：检查最早日期、整体方向和同日编号。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================
SELECT project_name, project_status, budget
FROM projects
WHERE project_status = '暂停'
  AND budget < 500000
ORDER BY budget DESC;
-- 为什么这样写：两个筛选条件同时成立，再将结果预算降序。
-- 预期结果特征：状态均为暂停，预算严格低于上限。
-- 常见错误：用 OR 扩大结果范围。
-- 验证方法：检查状态、最大预算和方向。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================
SELECT employee_id, employee_name, hire_date
FROM employees
WHERE hire_date BETWEEN '2022-01-01' AND '2023-12-31'
ORDER BY hire_date DESC, employee_id ASC;
-- 为什么这样写：BETWEEN 包含两个日期端点，排序先日期后编号。
-- 预期结果特征：日期在范围内且从晚到早。
-- 常见错误：把两个日期位置写反。
-- 验证方法：检查日期范围、方向及同日编号。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================
SELECT project_name, start_date, end_date, budget
FROM projects
WHERE project_status = '已完成'
  AND end_date IS NOT NULL
ORDER BY end_date DESC, budget DESC, project_name ASC;
-- 为什么这样写：先保证完成且有结束日期，再按三个优先级排序。
-- 预期结果特征：4 列，无 NULL 结束日期。
-- 常见错误：只筛选状态，不检查 end_date。
-- 验证方法：检查 NULL、日期方向以及并列预算和名称。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================
SELECT employee_id, employee_name, hire_date
FROM employees
WHERE hire_date >= '2020-01-01'
ORDER BY hire_date ASC, employee_id ASC;
-- 是否报错：原 SQL 通常不会报错。
-- 结果是否正确：不正确；DESC 将较晚日期放前，且同日顺序未定义。
-- 如何修改：改用 ASC，并增加 employee_id ASC。
-- 修改后特征：日期不早于边界，最早在前，同日编号升序。
-- 常见错误：只改排序方向，遗漏并列规则。
-- 验证方法：检查第一行、相邻日期和同日编号。
