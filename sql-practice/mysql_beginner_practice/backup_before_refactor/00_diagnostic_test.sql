USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 0 天：基础诊断
目标：只检查基础能力，不使用子查询、CTE、EXISTS、REGEXP 或类型转换。
做法：在每个 TODO 下独立写 SQL；先不要看答案。
*/·

-- 题 1：查询所有部门。返回 department_id、department_name、city；约 5 行。
-- 简短提示：从 departments 选择指定列。
-- TODO:

-- 题 2：查询工资大于 12000 的员工。返回 employee_name、salary；10 行。
-- 简短提示：使用 WHERE。
-- TODO:

-- 题 3：查询没有上级的员工。返回 employee_id、employee_name；应为 1 行。
-- 简短提示：NULL 不能用等号判断。
-- TODO:

-- 题 4：按工资从高到低查询员工。返回 employee_name、salary；20 行。
-- 简短提示：使用 ORDER BY 和 DESC。
-- TODO:

-- 题 5：统计员工总数。返回一列 employee_count；1 行，值应为 20。
-- 简短提示：使用 COUNT(*)。
-- TODO:

-- 题 6：统计每个项目状态的项目数。返回 project_status、project_count；4 行。
-- 简短提示：按状态 GROUP BY。
-- TODO:

-- 题 7：查询进行中的项目。返回 project_name、project_status；5 行。
-- 简短提示：utf8mb4 数据库中，中文字符串直接使用单引号。
-- TODO:

-- 题 8：查询 2023 年及以后入职的员工。返回 employee_name、hire_date；约 6 行。
-- 简短提示：日期用单引号。
-- TODO:

-- 题 9：用最简单的 INNER JOIN 查询员工及其部门。
-- 返回 employee_name、department_name；20 行。
-- 简短提示：连接两个 department_id。
-- TODO:

-- 题 10（改错）：下面 SQL 为什么错误？修正后应返回 1 行“陈晨”。
-- 错误 SQL：SELECT employee_name FROM employees WHERE manager_id = NULL;
-- TODO：说明原因并写修正 SQL。
