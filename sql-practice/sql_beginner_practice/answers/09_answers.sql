USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice'
    THROW 50001, N'安全检查失败：当前数据库不是 sql_beginner_practice。', 1;
GO

-- 题 1：NOT EXISTS 按 employee_id 关联；不产生重复。
SELECT e.employee_id, e.employee_name
FROM dbo.employees AS e
WHERE NOT EXISTS
(
    SELECT 1 FROM dbo.employee_projects AS ep
    WHERE ep.employee_id = e.employee_id
);

-- 题 2：NULL 与空字符串是两种不同状态，要分别判断。
-- 当前固定数据没有空字符串，因此只返回 city 为 NULL 的运维部。
SELECT department_name, city
FROM dbo.departments
WHERE city IS NULL OR city = N'';

-- 题 3：<> 表示不等于；job_title 非 NULL。
SELECT employee_name, job_title
FROM dbo.employees
WHERE job_title <> N'工程师';

-- 题 4：插入只发生在练习库事务中；最后回滚，不永久保存。
BEGIN TRANSACTION;
INSERT INTO dbo.departments (department_id, department_name, city)
VALUES (97, N'培训练习部', N'测试城市');
SELECT * FROM dbo.departments WHERE department_id = 97;
ROLLBACK;

-- 题 5：先用同一主键条件预览；UPDATE 有 WHERE，ROLLBACK 撤销。
SELECT employee_id, employee_name, salary
FROM dbo.employees
WHERE employee_id = 19;
BEGIN TRANSACTION;
UPDATE dbo.employees
SET salary = salary + 300
WHERE employee_id = 19;
SELECT employee_id, employee_name, salary FROM dbo.employees WHERE employee_id = 19;
ROLLBACK;

-- 题 6：预览与 UPDATE 都精确限定 project_id；NULL 不影响状态修改。
SELECT project_id, project_name, project_status
FROM dbo.projects
WHERE project_id = 10;
BEGIN TRANSACTION;
UPDATE dbo.projects
SET project_status = N'进行中'
WHERE project_id = 10;
SELECT project_id, project_name, project_status FROM dbo.projects WHERE project_id = 10;
ROLLBACK;

-- 题 7：临时行在同一事务内插入、预览、删除；最终整体回滚。
BEGIN TRANSACTION;
INSERT INTO dbo.departments (department_id, department_name, city)
VALUES (96, N'临时部门', NULL);
SELECT * FROM dbo.departments WHERE department_id = 96;
DELETE FROM dbo.departments WHERE department_id = 96;
SELECT * FROM dbo.departments WHERE department_id = 96;
ROLLBACK;

-- 题 8：SELECT 与 UPDATE 使用完全相同条件；只影响低预算待启动项目。
SELECT project_id, project_name, project_status, budget
FROM dbo.projects
WHERE project_status = N'待启动'
  AND budget < 500000;
BEGIN TRANSACTION;
UPDATE dbo.projects
SET budget = budget + 10000
WHERE project_status = N'待启动'
  AND budget < 500000;
SELECT project_id, project_name, project_status, budget
FROM dbo.projects
WHERE project_status = N'待启动'
  AND budget < 510000;
ROLLBACK;

-- 题 9：错误 SQL 无 WHERE，会清零全部工资。先预览、精确修改、回滚。
-- 错误 SQL：UPDATE dbo.employees SET salary = 0;
SELECT employee_id, employee_name, salary FROM dbo.employees WHERE employee_id = 20;
BEGIN TRANSACTION;
UPDATE dbo.employees SET salary = 0 WHERE employee_id = 20;
SELECT employee_id, employee_name, salary FROM dbo.employees WHERE employee_id = 20;
ROLLBACK;

-- 题 10：错误 SQL 无 WHERE，会尝试删除全部项目且可能受外键阻止。
-- 只预览并删除 project_id=14；该项目无参与和指标，最后仍回滚。
-- 错误 SQL：DELETE FROM dbo.projects;
SELECT project_id, project_name FROM dbo.projects WHERE project_id = 14;
BEGIN TRANSACTION;
DELETE FROM dbo.projects WHERE project_id = 14;
SELECT project_id, project_name FROM dbo.projects WHERE project_id = 14;
ROLLBACK;
