USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 7 天：CASE 与简单子查询
本课目标
1. 用 CASE WHEN 给结果分类。
2. 使用只返回一个值的标量子查询。
3. 使用 IN 子查询。
4. 对 NULL 做简单显示处理。
*/

-- 基础语法
-- CASE WHEN 条件 THEN 结果 ELSE 结果 END AS 别名
-- WHERE 列 > (SELECT AVG(列) FROM 表)
-- WHERE 列 IN (SELECT 列 FROM 表 WHERE 条件)

-- 可运行示例 1：按工资分为高、中、基础三档。
SELECT employee_name, salary,
       CASE
           WHEN salary >= 15000 THEN '高'
           WHEN salary >= 10000 THEN '中'
           ELSE '基础'
       END AS salary_level
FROM employees;

-- 可运行示例 2：查询高于公司平均工资的员工。
SELECT employee_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 可运行示例 3：查询属于上海部门的员工。
SELECT employee_name, department_id
FROM employees
WHERE department_id IN
(
    SELECT department_id FROM departments WHERE city = '上海'
);

-- 可运行示例 4：用 CASE 标记结束日期是否确定。
SELECT project_name,
       CASE WHEN end_date IS NULL THEN '未确定' ELSE '已确定' END AS end_date_status
FROM projects;

-- 旧知识复习
-- 题 1：找没有参与项目的员工。
-- 返回 employee_id、employee_name；2 行，应为员工 19、20。
-- 提示：员工放左边，检查右表主键是否为 NULL。TODO:

-- 题 2：保留全部项目和经理姓名。
-- 返回 project_name、manager_name；14 行，其中项目 14 的经理为 NULL。
-- 提示：项目放左边，用 LEFT JOIN 连接经理员工。TODO:

-- 题 3：查询城市为 NULL 或空字符串的部门，复习两者的区别。
-- 返回 department_name、city；当前 1 行，只有 NULL，没有空字符串。
-- 提示：分别写 IS NULL 与 = ''，再用 OR 连接。TODO:

-- 本课练习
-- 题 4：把项目预算分为“高预算”（>=800000）和“普通预算”。
-- 返回 project_name、budget、budget_level；14 行。提示：CASE。
-- TODO:

-- 题 5：查询高于全部项目平均预算的项目。
-- 返回 project_name、budget；7 行。提示：标量子查询。
-- TODO:

-- 题 6：查询项目状态为“进行中”的项目经理。
-- 返回 employee_id、employee_name；项目经理可能重复，结果应去重。
-- 提示：project_manager_id 放进 IN 子查询，并注意 NULL。TODO:

-- 题 7：把 manager_id 为 NULL 显示成 0，否则显示原 manager_id。
-- 返回 employee_name、manager_display；20 行。提示：先用 CASE。
-- TODO:

-- 题 8（综合）：查询工资高于公司平均工资、且职位为“工程师”的员工。
-- 返回 employee_name、job_title、salary；3 行。
-- 提示：沿用一个返回 AVG(salary) 的标量子查询，再加职位条件。
-- TODO:

-- 题 9（改错）：标量子查询必须返回一个值，下面子查询返回多行。
-- 错误 SQL：SELECT employee_name FROM employees
-- WHERE department_id = (SELECT department_id FROM departments);
-- 目标：查询上海部门的员工。请选择适合多值结果的运算符。TODO:

-- 题 10（改错）：下面 CASE 顺序会让 18000 也先命中“中”。
-- CASE WHEN salary >= 10000 THEN '中'
--      WHEN salary >= 15000 THEN '高' ELSE '基础' END
-- 请调整条件顺序，返回 employee_name、salary、salary_level。TODO:

/*
每日自检
[ ] 我能写简单 CASE 和子查询。
[ ] 我能解释子查询返回一个值还是多值。
[ ] 我能预测分类和筛选结果。
[ ] 我理解 CASE 从上到下判断。
[ ] 我能说明查询中是否需要 JOIN。
[ ] 我检查了 NULL 和重复经理。
[ ] 我写下了今天最容易错的知识点。
*/
