USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 2 天：筛选基础
本课目标
1. 用 WHERE 只保留需要的行。
2. 组合 AND、OR、NOT。
3. 使用 IN、BETWEEN、LIKE 和 NULL 条件。
4. 理解 NULL 不是空字符串。
*/

-- 基础语法
-- SELECT 列 FROM 表 WHERE 条件;
-- WHERE 列 IN (值1, 值2)
-- WHERE 列 BETWEEN 下限 AND 上限
-- WHERE 列 LIKE '开头%'
-- WHERE 列 IS NULL

-- 可运行示例 1：工资至少 15000 的员工；结果 6 行。
SELECT employee_name, salary FROM employees WHERE salary >= 15000;

-- 可运行示例 2：进行中或暂停的项目；结果 7 行。
SELECT project_name, project_status
FROM projects
WHERE project_status IN ('进行中', '暂停');

-- 可运行示例 3：姓名以“王”开头；结果 1 行。
SELECT employee_name FROM employees WHERE employee_name LIKE '王%';

-- 可运行示例 4：没有结束日期的项目；结果 6 行。NULL 不是空字符串。
SELECT project_name, end_date FROM projects WHERE end_date IS NULL;

-- 旧知识复习
-- 题 1：查询工资最高的 2 名员工。返回 employee_name、salary；2 行。
-- 提示：LIMIT 配合 ORDER BY。TODO:

-- 题 2：查询不重复的部门城市。返回 city；约 4 行，其中包含一个 NULL。
-- 提示：DISTINCT。TODO:

-- 题 3：查询项目名称、预算和预算的 20%（别名 estimated_cost）。
-- 返回 14 行。提示：计算列和 AS。TODO:

-- 本课练习
-- 题 4：查询工资在 9000 到 12000 之间（含边界）的员工。
-- 返回 employee_name、salary；8 行。提示：BETWEEN。
-- TODO:

-- 题 5：查询技术部或财务部的员工编号和部门编号。
-- 返回 employee_id、department_id；约 9 行。提示：IN。
-- TODO:

-- 题 6：查询 2024 年及以后入职且工资低于 8000 的员工。
-- 返回 employee_name、hire_date、salary；2 行。提示：两个条件用 AND。
-- TODO:

-- 题 7：查询职位不是“工程师”的员工。
-- 返回 employee_name、job_title；结果少于 20 行。提示：NOT 或 <>。
-- TODO:

-- 题 8：查询没有结束日期的“待启动”项目。
-- 返回 project_name、project_status、end_date；4 行。提示：IS NULL 和 AND。
-- TODO:

-- 题 9（改错）：下面条件把所有高薪员工都选中，还选中所有市场部员工。
-- 错误 SQL：SELECT employee_name, department_id, salary FROM employees
--           WHERE department_id = 2 OR department_id = 4 AND salary >= 12000;
-- 目标：只查询“技术部或市场部”中工资至少 12000 的员工；5 行。
-- 提示：AND 比 OR 先计算，需要括号。TODO:

-- 题 10（改错）：WHERE end_date = NULL 为什么永远得不到正确结果？
-- 修正后返回所有没有结束日期的项目，共 6 行。
-- 提示：使用专门的 NULL 判断。TODO:

/*
每日自检
[ ] 我能不看答案写出基础筛选。
[ ] 我能解释每个筛选条件。
[ ] 我能预测结果范围。
[ ] 我理解 = NULL 的错误原因。
[ ] 我能说明本课还没有使用 JOIN。
[ ] 我检查了 NULL、AND 与 OR。
[ ] 我写下了今天最容易错的知识点。
*/
