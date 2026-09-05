USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 8 天：CTE、EXISTS 与类型转换入门
本课目标
1. 使用一次非递归 CTE，让查询分成两小步。
2. 用 EXISTS / NOT EXISTS 判断“有没有”。
3. 用 CASE、REGEXP、CAST 安全尝试转换。
4. 使用 IFNULL 替换显示用 NULL。

学习安排（建议分两次，每次 20～30 分钟）
- 第一段：示例 1～3 和题 4～6，练 CTE、EXISTS、NOT EXISTS。
- 第二段：示例 4～5 和题 7～10，练 REGEXP、CAST、IFNULL。
*/

-- 基础语法
-- WITH 名称 AS (SELECT ...) SELECT ... FROM 名称;
-- WHERE EXISTS (SELECT 1 FROM 相关表 WHERE 连接条件)
-- 先用 REGEXP 检查格式，再 CAST；格式不对时由 CASE 返回 NULL。
-- 正则表达式中：^ 表示字符串开头，$ 表示字符串结尾，
-- [0-9]+ 表示至少一个数字，? 表示前一小段可以出现 0 次或 1 次。
-- 复杂的小数检查式可以直接套用，不要求背诵。
-- IFNULL(值, 替代值)：值为 NULL 时显示替代值。

-- 可运行示例 1：CTE 先取高预算项目，再查询；预计 4 行。
WITH high_budget_projects AS
(
    SELECT project_id, project_name, budget
    FROM projects
    WHERE budget >= 800000
)
SELECT project_id, project_name, budget
FROM high_budget_projects;

-- 可运行示例 2：查询至少参加一个项目的员工；预计 18 行。
SELECT e.employee_name
FROM employees AS e
WHERE EXISTS
(
    SELECT 1 FROM employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 可运行示例 3：查询没有参与项目的员工；结果 2 行。
SELECT e.employee_name
FROM employees AS e
WHERE NOT EXISTS
(
    SELECT 1 FROM employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 可运行示例 4：先判断简单文字是不是纯整数，再安全转换。
-- 运行前先预测：'123' 会成功；'10kV' 和 '低压' 会返回 NULL。
SELECT '123' AS sample_text,
       '123' REGEXP '^[0-9]+$' AS is_integer,
       CASE WHEN '123' REGEXP '^[0-9]+$' THEN CAST('123' AS SIGNED) ELSE NULL END AS converted_value;
SELECT '10kV' AS sample_text,
       '10kV' REGEXP '^[0-9]+$' AS is_integer,
       CASE WHEN '10kV' REGEXP '^[0-9]+$' THEN CAST('10kV' AS SIGNED) ELSE NULL END AS converted_value;
SELECT '低压' AS sample_text,
       '低压' REGEXP '^[0-9]+$' AS is_integer,
       CASE WHEN '低压' REGEXP '^[0-9]+$' THEN CAST('低压' AS SIGNED) ELSE NULL END AS converted_value;

-- 可运行示例 5：没有电压信息时显示“未填写”。COALESCE 也能替换 NULL，
-- 本课重点练 IFNULL；预计 12 行，其中 1 行显示“未填写”。
SELECT metric_id, IFNULL(voltage_level, '未填写') AS voltage_display
FROM project_metrics;

-- 旧知识复习
-- 题 1：用 CASE 把工资分为 >=15000 的“高”和其他“普通”。
-- 返回 employee_name、salary_level；20 行。TODO:

-- 题 2：查询高于平均预算的项目。
-- 返回 project_name、budget；7 行。提示：标量子查询。TODO:

-- 题 3：找无指标项目。
-- 返回 project_id、project_name；结果 2 行，应为项目 13、14。
-- 提示：LEFT JOIN 后检查指标主键是否为 NULL。TODO:

-- 本课练习
-- 题 4：用 CTE 先选“进行中”项目，再显示 project_name、budget；5 行。
-- 提示：CTE 内只做筛选，外层只取列。TODO:

-- 题 5：用 EXISTS 查询至少有一名员工参与的项目。
-- 返回 project_id、project_name；12 行。TODO:

-- 题 6：用 NOT EXISTS 查询没有任何员工参与的项目。
-- 返回 project_id、project_name；2 行。TODO:

-- 题 7：尝试去掉 voltage_level 中的“kV”后转为 DECIMAL。
-- 返回 voltage_level、voltage_number；“低压”和“380V”等不能转换时为 NULL。
-- 10kV、35kV、110kV 应成功；提示：先 REPLACE，再 REGEXP 检查，最后 CAST。TODO:

-- 题 8：显示项目名称和经理编号；无经理时显示 0。
-- 返回 project_name、manager_id_display；14 行。提示：IFNULL。TODO:

-- 题 9（改错）：下面 CAST 可能把不能转换的文字变成 0 并产生警告，
-- 无法区分“真实的 0”和“转换失败”。
-- 错误 SQL：SELECT CAST(voltage_level AS SIGNED) FROM project_metrics;
-- 目标：先去掉 kV，再检查纯整数格式并转换；不符合时返回 NULL。
-- 结果 12 行；10kV、35kV、110kV 成功，380V、“低压”和 NULL 返回 NULL。TODO:

-- 题 10（改错）：下面 EXISTS 没有关联外层员工，只要关系表有一行，
-- 就会返回所有员工。
-- SELECT e.employee_name FROM employees AS e
-- WHERE EXISTS (SELECT 1 FROM employee_projects AS ep);
-- 请补上外层与内层的关联条件；应返回 18 名参与过项目的员工。TODO:

/*
每日自检
[ ] 我能写非递归 CTE、EXISTS 和安全类型转换。
[ ] 我能解释 EXISTS 检查“有没有”。
[ ] 我能预测 NOT EXISTS 返回 2 行。
[ ] 我理解为什么要先用 REGEXP 检查再 CAST。
[ ] 我能说明 EXISTS 中的连接条件。
[ ] 我检查了 NULL 和重复行。
[ ] 我写下了今天最容易错的知识点。
*/
