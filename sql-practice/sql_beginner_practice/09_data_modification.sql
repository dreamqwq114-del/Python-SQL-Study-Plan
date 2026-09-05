USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

/*
第 9 天：数据修改与事务
本课目标
1. 理解 INSERT、UPDATE、DELETE。
2. 修改前先 SELECT 预览范围。
3. 使用事务并默认 ROLLBACK。
4. 知道 COMMIT 会永久保存，ROLLBACK 会撤销。
请逐段选中执行，不要一次运行整个文件。
*/

-- 基础语法
-- BEGIN TRANSACTION; ... ROLLBACK;
-- 只有确认要永久保存时才把 ROLLBACK 改为 COMMIT；本课不要改。

-- 可运行示例 1：插入临时部门，再撤销；事务内查询 1 行，回滚后应为 0 行。
BEGIN TRANSACTION;
INSERT INTO dbo.departments (department_id, department_name, city)
VALUES (99, N'临时练习部', N'测试城市');
SELECT * FROM dbo.departments WHERE department_id = 99;
ROLLBACK;
SELECT * FROM dbo.departments WHERE department_id = 99; -- 回滚后 0 行

-- 可运行示例 2：先预览，再更新，再撤销；预览 1 行，事务内工资多 500，
-- 回滚后工资恢复原值。
SELECT employee_id, employee_name, salary
FROM dbo.employees
WHERE employee_id = 20;
BEGIN TRANSACTION;
UPDATE dbo.employees
SET salary = salary + 500
WHERE employee_id = 20;
SELECT employee_id, employee_name, salary FROM dbo.employees WHERE employee_id = 20;
ROLLBACK;
SELECT employee_id, employee_name, salary
FROM dbo.employees
WHERE employee_id = 20; -- 回滚后恢复原工资 5000

-- 可运行示例 3：先插入临时行，删除前预览 1 行，删除后查询 0 行；
-- 最终回滚后临时插入也不存在。
BEGIN TRANSACTION;
INSERT INTO dbo.departments (department_id, department_name, city)
VALUES (98, N'待删除练习部', NULL);
SELECT * FROM dbo.departments WHERE department_id = 98;
DELETE FROM dbo.departments WHERE department_id = 98;
SELECT * FROM dbo.departments WHERE department_id = 98;
ROLLBACK;
SELECT * FROM dbo.departments WHERE department_id = 98; -- 回滚后仍为 0 行

-- 旧知识复习
-- 题 1：用 NOT EXISTS 查询未参与项目的员工。
-- 返回 employee_id、employee_name；2 行，应为员工 19、20。TODO:

-- 题 2：查询 city 为 NULL 或空字符串的部门。
-- 返回 department_name、city；当前 1 行，只有 NULL，没有空字符串。
-- 提示：分别写 IS NULL 与 = N''，再用 OR 连接。TODO:

-- 题 3：查询职位不是“工程师”的员工。
-- 返回 employee_name、job_title；17 行。提示：使用 NOT 或 <>。TODO:

-- 本课练习：所有答案都必须限制在练习库，并默认 ROLLBACK。
-- 题 4：在事务中插入 department_id=97 的“培训练习部”，查询确认后回滚。
-- 返回确认查询 1 行；回滚后应不存在。提示：BEGIN、INSERT、SELECT、ROLLBACK。
-- TODO:

-- 题 5：先 SELECT 预览 employee_id=19，再在事务中把工资增加 300，
-- 查询修改结果，最后回滚。所有 WHERE 必须精确限定 employee_id。
-- TODO:

-- 题 6：先 SELECT 预览 project_id=10，再在事务中把状态改为“进行中”，
-- 查询修改结果，最后回滚。TODO:

-- 题 7：在同一事务中先插入 department_id=96 的临时部门，
-- 再 SELECT 预览并 DELETE 该行，最后 ROLLBACK。TODO:

-- 题 8（综合）：先预览所有“待启动”项目；在事务中把预算低于 500000
-- 的待启动项目预算增加 10000；查询核对后 ROLLBACK。
-- 预览和 UPDATE 必须使用完全相同的 WHERE。TODO:

-- 题 9（改错）：危险 SQL：UPDATE dbo.employees SET salary = 0;
-- 说明危险原因。目标只修改 employee_id=20，必须先 SELECT，
-- 再放入事务，最后 ROLLBACK。TODO:

-- 题 10（改错）：危险 SQL：DELETE FROM dbo.projects;
-- 不要运行。说明为什么危险。目标是练习删除 project_id=14，但它有部门外键、
-- 没有参与或指标记录；必须先 SELECT，在事务中精确 DELETE，最后 ROLLBACK。
-- TODO:

/*
每日自检
[ ] 我能独立写 INSERT、UPDATE、DELETE 的基础结构。
[ ] 我能解释每次修改目标。
[ ] 我先预测并 SELECT 受影响行。
[ ] 我理解无 WHERE 的危险。
[ ] 我确认只使用 sql_beginner_practice。
[ ] 我检查了 NULL、外键和修改范围。
[ ] 我知道 COMMIT 永久保存、ROLLBACK 撤销。
*/
