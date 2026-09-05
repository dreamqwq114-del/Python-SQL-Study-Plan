USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

/*
阶段测试 2：第 8 天后完成
范围：INNER/LEFT JOIN、JOIN 重复、CASE、简单子查询、CTE、
EXISTS、TRY_CAST、NULL 处理。共 10 题，不提供详细提示。
*/

-- 题 1：查询员工、所属部门和城市。
-- 返回 employee_name、department_name、city；20 行。
-- TODO:

-- 题 2：查询所有项目和项目经理姓名，无经理也保留。
-- 返回 project_name、manager_name；14 行。
-- TODO:

-- 题 3：查询没有参与项目的员工。
-- 返回 employee_id、employee_name；2 行。
-- TODO:

-- 题 4：统计所有项目的参与人数，无参与项目显示 0。
-- 返回 project_name、participant_count；14 行。
-- TODO:

-- 题 5：用 CASE 把预算 >=800000 标为“高”，否则标为“普通”。
-- 返回 project_name、budget、budget_level；14 行。
-- TODO:

-- 题 6：查询高于平均工资的员工。
-- 返回 employee_name、salary。
-- TODO:

-- 题 7：使用非递归 CTE 查询所有“待启动”项目。
-- 返回 project_id、project_name、budget；4 行。
-- TODO:

-- 题 8：使用 EXISTS 查询至少参与一个项目的员工。
-- 返回 employee_id、employee_name；18 行。
-- TODO:

-- 题 9：尝试将 voltage_level 转成 INT；失败时返回 NULL。
-- 返回 voltage_level、voltage_as_int；12 行。
-- TODO:

-- 题 10（改错）：目标是保留全部项目并只匹配管理费 >0.15 的指标。
-- 错误 SQL：SELECT p.project_name, pm.management_fee
-- FROM dbo.projects AS p
-- LEFT JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
-- WHERE pm.management_fee > 0.15;
-- 修正后应保留 14 个项目，并用 ISNULL 把无匹配费用显示为 0。
-- TODO:
