USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

/*
第 10 天：综合项目经营分析
本课目标
1. 把前 9 天知识组合起来。
2. 正确保留 NULL 和无匹配项目。
3. 防止 JOIN 造成重复计数。
4. 能解释并验证结果，而不只写出 SQL。
本课共 12 题。第一轮 45～60 分钟先做题 1～8；
题 9～12 留到第二轮巩固，不要为了赶时间直接看答案。
*/

-- 基础语法提醒：先确认“每行代表什么”，再决定 INNER/LEFT JOIN、
-- GROUP BY、COUNT 和 NULL 处理。不强制使用 CTE 或 EXISTS。

-- 可运行示例 1：分别查看 5 张表行数，作为结果核对基线。
-- 依次应为 5、20、14、12、37；这里不用尚未教学的合并语法。
SELECT COUNT(*) AS department_count FROM departments;
SELECT COUNT(*) AS employee_count FROM employees;
SELECT COUNT(*) AS project_count FROM projects;
SELECT COUNT(*) AS metric_count FROM project_metrics;
SELECT COUNT(*) AS employee_project_count FROM employee_projects;

-- 可运行示例 2：全部项目和参与人数；14 行，项目 13、14 为 0。
SELECT p.project_id, p.project_name, COUNT(ep.employee_id) AS participant_count
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
GROUP BY p.project_id, p.project_name;

-- 可运行示例 3：全部项目和经理；项目 14 的经理为“未分配”。
SELECT p.project_name, IFNULL(e.employee_name, '未分配') AS manager_name
FROM projects AS p
LEFT JOIN employees AS e ON e.employee_id = p.project_manager_id;

-- 旧知识复习（题 1～3）：先复习分组、平均值和 LEFT JOIN，再进入综合分析。

-- 题 1：统计每个部门的员工数量。
-- 返回 department_name、employee_count；5 行。提示：部门与员工连接后分组。
-- TODO:

-- 题 2：统计每个部门的平均工资。
-- 返回 department_name、average_salary；5 行。提示：AVG 与 GROUP BY。
-- TODO:

-- 题 3：显示每个项目及项目经理。
-- 返回 project_name、manager_name；14 行，无经理显示“未分配”。
-- 错误 SQL：SELECT p.project_name, e.employee_name
-- FROM projects AS p
-- INNER JOIN employees AS e ON e.employee_id = p.project_manager_id;
-- 说明它为什么只返回 13 行，再改为能保留无经理项目的写法。TODO:

-- 题 4（含改错）：统计每个项目的参与人数。
-- 返回 project_name、participant_count；14 行，无参与者为 0。
-- 错误思路 A：LEFT JOIN 后使用 COUNT(*)，会把无参与项目也计成 1。
-- 错误思路 B：参与关系尚未按项目汇总时，又连接其他一对多明细，
-- 可能让同一参与者重复出现。请先只连接参与关系，并说明计数字段为何选
-- ep.employee_id；若以后确实加入另一张一对多明细，再考虑预先聚合或去重。
-- TODO:

-- 题 5：查询没有参与任何项目的员工。
-- 返回 employee_id、employee_name；2 行。可用 LEFT JOIN 或 NOT EXISTS。
-- TODO:

-- 题 6：查询没有任何员工参与的项目。
-- 返回 project_id、project_name；2 行。结果应为项目 13、14。
-- TODO:

-- 题 7：查询管理费大于 0.15 的项目。
-- 返回 project_name、management_fee；6 行。NULL 管理费不满足条件。
-- TODO:

-- 题 8：查询投资收益率高于全部非 NULL 收益率平均值的项目。
-- 返回 project_name、investment_return_rate；结果少于 12 行。
-- 提示：AVG 自动忽略 NULL，使用标量子查询。TODO:

-- 题 9：按项目状态统计数量。
-- 返回 project_status、project_count；4 行。TODO:

-- 题 10：把投资收益率显示为百分比数值。
-- 返回 project_name、return_percentage；12 行指标记录，NULL 仍为 NULL。
-- 提示：乘以 100，不必拼接百分号。TODO:

-- 题 11：按收益率分档：>=0.0850 为“高”，>=0.0700 为“中”，
-- 低于 0.0700 为“低”，NULL 为“未知”。
-- 返回 project_name、investment_return_rate、return_level；12 行。
-- 提示：先判断 NULL，再按从高到低顺序写 CASE。TODO:

-- 题 12（最终综合）：每个项目返回一行，列为：
-- project_name、department_name、manager_name、participant_count、
-- management_fee、investment_return_rate、voltage_level、project_status。
-- 必须保留没有经理或没有指标的项目，因此最终应为 14 行。
-- 提示：先把 employee_projects 按 project_id 聚合成参与人数，再连接其他表；
-- 可使用一个非递归 CTE。使用 LEFT JOIN 保留无经理、无指标项目。
-- 完成后必须在注释中回答：
-- A. 一对多 JOIN 为什么会出现重复行？
-- B. 如何用基础计数核对 14 个项目是否全部保留？
-- C. 如何确认参与人数没有因其他 JOIN 被重复统计？
-- D. 无经理或无指标的数据为什么应该保留？
-- TODO:

/*
每日自检
[ ] 我能独立组合基础语句。
[ ] 我能解释每行代表一个项目还是一条关系。
[ ] 我能预测最终应有 14 行。
[ ] 我理解重复计数的来源。
[ ] 我能说明 INNER JOIN 与 LEFT JOIN 的选择。
[ ] 我检查了 NULL、重复行和无匹配项目。
[ ] 我写下了今天最容易错的知识点。
*/
