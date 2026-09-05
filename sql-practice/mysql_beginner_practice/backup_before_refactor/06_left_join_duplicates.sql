USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 6 天：LEFT JOIN 与重复行
本课目标
1. 区分 INNER JOIN 与 LEFT JOIN。
2. 找到没有匹配记录的行。
3. 理解一对多、多对多为什么增加结果行。
4. 检查重复来自哪张关系表。
本课不使用子查询、CTE、EXISTS。
*/

-- 基础语法
-- 左表 LEFT JOIN 右表 ON 连接条件：左表所有行都保留。
-- 找无匹配：LEFT JOIN 后检查右表主键 IS NULL。

-- 可运行示例 1：保留全部项目，没有经理时 manager_name 为 NULL；14 行。
SELECT p.project_name, e.employee_name AS manager_name
FROM projects AS p
LEFT JOIN employees AS e ON e.employee_id = p.project_manager_id;

-- 可运行示例 2：找没有参与任何项目的员工；2 行。
SELECT e.employee_id, e.employee_name
FROM employees AS e
LEFT JOIN employee_projects AS ep ON ep.employee_id = e.employee_id
WHERE ep.employee_id IS NULL;

-- 可运行示例 3：项目 1 出现 6 行，因为它有 6 条参与关系。
SELECT p.project_name, ep.employee_id
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
WHERE p.project_id = 1;

-- 可运行示例 4：每个项目的参与人数；无参与项目也保留，COUNT(右表主键) 为 0。
SELECT p.project_id, p.project_name, COUNT(ep.employee_id) AS participant_count
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name;

-- 旧知识复习
-- 题 1：查询员工及所属部门，返回 employee_name、department_name；20 行。
-- 提示：INNER JOIN。TODO:

-- 题 2：统计每个有参与记录项目的人数。
-- 返回 project_id、project_name、participant_count；12 行。
-- 提示：INNER JOIN 后按项目分组。TODO:

-- 题 3：查询没有结束日期的项目并按预算降序。
-- 返回 project_name、budget、end_date；6 行，end_date 均为 NULL。
-- 提示：先用 IS NULL 筛选，再按 budget DESC 排序。TODO:

-- 本课练习
-- 题 4：保留所有部门并显示员工姓名。
-- 返回 department_name、employee_name；一部门多员工会出现多行。
-- 提示：departments 放左边。TODO:

-- 题 5：找没有员工参与的项目。
-- 返回 project_id、project_name；2 行，应为项目 13、14。
-- 提示：LEFT JOIN 后检查右表主键。TODO:

-- 题 6：找没有项目指标的项目。
-- 返回 project_id、project_name；2 行，应为项目 13、14。
-- TODO:

-- 题 7：显示全部项目及经理姓名；14 行，其中一个 manager_name 为 NULL。
-- 提示：如果用 INNER JOIN 会丢失项目 14。TODO:

-- 题 8（综合）：统计每位员工参与的项目数，未参与者显示 0。
-- 返回 employee_id、employee_name、project_count；20 行。
-- 提示：员工放左边，COUNT 右表非空主键。TODO:

-- 题 9（改错）：目标是保留所有项目，但下面 WHERE 会去掉无指标项目。
-- 错误 SQL：SELECT p.project_name, pm.management_fee
-- FROM projects AS p
-- LEFT JOIN project_metrics AS pm ON pm.project_id = p.project_id
-- WHERE pm.management_fee > 0.15;
-- 请解释为什么像 INNER JOIN，并修改连接位置，使全部项目仍保留；
-- 不满足费用条件的右表列显示 NULL。TODO:

-- 题 10（改错）：下面查询既把员工重复统计，又漏掉无项目员工。
-- SELECT d.department_name, COUNT(*) AS employee_count
-- FROM departments AS d
-- INNER JOIN employees AS e ON e.department_id = d.department_id
-- INNER JOIN employee_projects AS ep ON ep.employee_id = e.employee_id
-- GROUP BY d.department_name;
-- 目标：统计部门员工人数，不受一个员工参加多个项目影响。
-- 返回 department_name、employee_count；5 行，财务部和运维部都应为 4。
-- 提示：先删除完成目标不需要的 employee_projects JOIN；再思考可选去重写法。TODO:

/*
每日自检
[ ] 我能写 LEFT JOIN 找无匹配记录。
[ ] 我能解释一对多为什么增加行。
[ ] 我能预测项目 1 会出现 6 行。
[ ] 我理解右表条件放 WHERE 的影响。
[ ] 我能说明何时用 INNER JOIN 或 LEFT JOIN。
[ ] 我检查了 NULL 和重复计数。
[ ] 我写下了今天最容易错的知识点。
*/
