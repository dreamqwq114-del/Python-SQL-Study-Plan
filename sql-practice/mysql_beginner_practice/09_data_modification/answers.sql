USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 示例 1 最小修改任务参考答案
-- ==================================================

START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9011, '插入模仿部门', '测试城市');
SELECT department_id, department_name, city
FROM departments WHERE department_id = 9011;
ROLLBACK;

-- 为什么这样写：明确列和值，并用专用编号和回滚隔离练习。
-- 预期结果特征：事务中 1 行，回滚后专用行不存在。
-- 验证方法：回滚后再次按 9011 查询。
-- 常见错误：忘记回滚或使用已有主键。

-- ==================================================
-- 示例 2 最小修改任务参考答案
-- ==================================================

SELECT department_id, department_name, city
FROM departments WHERE department_id = 9012;
START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9012, '更新模仿部门', '甲城');
SELECT department_id, city FROM departments WHERE department_id = 9012;
UPDATE departments SET city = '乙城' WHERE department_id = 9012;
SELECT department_id, city FROM departments WHERE department_id = 9012;
ROLLBACK;

-- 为什么这样写：更新前后使用相同精确主键，并默认回滚。
-- 预期结果特征：只修改专用行，验证时城市为乙城。
-- 验证方法：检查目标编号、值和回滚结果。
-- 常见错误：预览与 UPDATE 的条件不同。

-- ==================================================
-- 示例 3 最小修改任务参考答案
-- ==================================================

SELECT department_id, department_name
FROM departments WHERE department_id = 9013;
START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9013, '删除模仿部门', NULL);
SELECT department_id, department_name FROM departments WHERE department_id = 9013;
DELETE FROM departments WHERE department_id = 9013;
SELECT department_id, department_name FROM departments WHERE department_id = 9013;
ROLLBACK;

-- 为什么这样写：删除只命中已预览的专用主键。
-- 预期结果特征：删除前 1 行，删除后 0 行。
-- 验证方法：检查 WHERE 和删除后的查询。
-- 常见错误：漏写 WHERE。

-- ==================================================
-- 示例 4 最小修改任务参考答案
-- ==================================================

START TRANSACTION;
SELECT DATABASE() AS current_database, COUNT(*) AS project_count
FROM projects;
COMMIT;

-- 为什么这样写：只读事务没有数据修改，可用 COMMIT 结束。
-- 预期结果特征：返回当前数据库和项目数量。
-- 验证方法：再次统计项目数，应保持不变。
-- 常见错误：把 COMMIT 当作撤销命令。

-- ==================================================
-- 示例 5 最小修改任务参考答案
-- ==================================================

SELECT department_id, department_name
FROM departments WHERE department_id = 9015;
START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9015, '修改前名称', '测试城市');
SELECT department_id, department_name FROM departments WHERE department_id = 9015;
UPDATE departments
SET department_name = '已核对部门'
WHERE department_id = 9015;
SELECT ROW_COUNT() AS affected_rows;
SELECT department_id, department_name FROM departments WHERE department_id = 9015;
ROLLBACK;

-- 为什么这样写：精确更新后立即检查受影响行数和实际值。
-- 预期结果特征：affected_rows 为 1，名称为已核对部门。
-- 验证方法：回滚后确认 9015 不存在。
-- 常见错误：执行其他语句后才查看 ROW_COUNT()。

-- ==================================================
-- 练习 1 参考答案
-- ==================================================

START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9101, '练习一部门', '南京');
SELECT department_id, department_name, city
FROM departments WHERE department_id = 9101;
ROLLBACK;
SELECT department_id, department_name, city
FROM departments WHERE department_id = 9101;

-- 为什么这样写：事务中验证新增，回滚后再次确认。
-- 预期结果特征：回滚前 1 行，回滚后 0 行。
-- 常见错误：列和值顺序错位。
-- 验证方法：比较两次查询。

-- ==================================================
-- 练习 2 参考答案
-- ==================================================

SELECT department_id, department_name, city
FROM departments WHERE department_id = 9102;
START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9102, '练习二部门', '修改前');
SELECT department_id, city FROM departments WHERE department_id = 9102;
UPDATE departments SET city = '修改后' WHERE department_id = 9102;
SELECT department_id, city FROM departments WHERE department_id = 9102;
ROLLBACK;

-- 为什么这样写：先预览目标，再精确修改并验证。
-- 预期结果特征：验证时城市为修改后，固定数据不变。
-- 常见错误：更新条件不是 9102。
-- 验证方法：检查目标行和回滚结果。

-- ==================================================
-- 练习 3 参考答案
-- ==================================================

SELECT department_id, department_name
FROM departments WHERE department_id = 9103;
START TRANSACTION;
INSERT INTO departments (department_id, department_name, city)
VALUES (9103, '练习三部门', NULL);
SELECT department_id, department_name FROM departments WHERE department_id = 9103;
DELETE FROM departments WHERE department_id = 9103;
SELECT department_id, department_name FROM departments WHERE department_id = 9103;
ROLLBACK;

-- 为什么这样写：DELETE 只删除已预览的专用行。
-- 预期结果特征：删除前 1 行，删除后 0 行。
-- 常见错误：遗漏 FROM 或 WHERE。
-- 验证方法：核对删除前后结果。

-- ==================================================
-- 练习 4 参考答案
-- ==================================================

START TRANSACTION;
INSERT INTO employees
    (employee_id, employee_name, department_id, job_title,
     salary, hire_date, manager_id)
VALUES
    (9104, '练习员工', 5, '练习职位',
     6000.00, '2026-01-15', 5);
SELECT employee_id, employee_name, department_id, job_title,
       salary, hire_date, manager_id
FROM employees WHERE employee_id = 9104;
ROLLBACK;
SELECT employee_id FROM employees WHERE employee_id = 9104;

-- 为什么这样写：所有必填值和已有外键目标都明确提供。
-- 预期结果特征：回滚前 1 行，回滚后 0 行。
-- 常见错误：日期格式错误或使用不存在的部门。
-- 验证方法：检查全部字段和回滚后的结果。

-- ==================================================
-- 练习 5 参考答案
-- ==================================================

SELECT project_id, project_name, project_status
FROM projects WHERE project_id = 9105;
START TRANSACTION;
INSERT INTO projects
    (project_id, project_name, department_id, project_manager_id,
     project_status, budget, start_date, end_date)
VALUES
    (9105, '事务练习项目', 1, 6,
     '待启动', 100000.00, '2026-02-01', NULL);
SELECT project_id, project_status FROM projects WHERE project_id = 9105;
UPDATE projects
SET project_status = '进行中'
WHERE project_id = 9105;
SELECT ROW_COUNT() AS affected_rows;
SELECT project_id, project_status FROM projects WHERE project_id = 9105;
ROLLBACK;

-- 为什么这样写：专用项目满足约束，更新只命中其主键。
-- 预期结果特征：影响 1 行，验证状态为进行中。
-- 常见错误：遗漏必填列或使用不存在的外键。
-- 验证方法：检查受影响行数、状态和回滚。

-- ==================================================
-- 练习 6 参考答案
-- ==================================================

SELECT metric_id, project_id
FROM project_metrics WHERE project_id = 14;
START TRANSACTION;
INSERT INTO project_metrics
    (metric_id, project_id, management_fee,
     investment_return_rate, voltage_level)
VALUES
    (9114, 14, 0.12, 0.0500, '10kV');
SELECT metric_id, project_id, management_fee,
       investment_return_rate, voltage_level
FROM project_metrics WHERE project_id = 14;
ROLLBACK;
SELECT metric_id, project_id
FROM project_metrics WHERE project_id = 14;

-- 为什么这样写：先确认唯一项目指标不存在，再临时插入并回滚。
-- 预期结果特征：事务中 1 行，回滚后 0 行。
-- 常见错误：把 metric_id 和 project_id 混为一列。
-- 验证方法：比较事务前、中、后三次结果。

-- ==================================================
-- 练习 7 参考答案
-- ==================================================

SELECT employee_id, project_id
FROM employee_projects
WHERE employee_id = 9107 AND project_id = 1;
START TRANSACTION;
INSERT INTO employees
    (employee_id, employee_name, department_id, job_title,
     salary, hire_date, manager_id)
VALUES
    (9107, '参与练习员工', 5, '练习职位',
     6000.00, '2026-01-20', 5);
INSERT INTO employee_projects
    (employee_id, project_id, role_name, working_hours)
VALUES
    (9107, 1, '练习角色', 8.00);
SELECT employee_id, project_id, role_name, working_hours
FROM employee_projects
WHERE employee_id = 9107 AND project_id = 1;
DELETE FROM employee_projects
WHERE employee_id = 9107 AND project_id = 1;
SELECT employee_id, project_id
FROM employee_projects
WHERE employee_id = 9107 AND project_id = 1;
ROLLBACK;

-- 为什么这样写：先满足外键，再用复合主键精确删除。
-- 预期结果特征：删除前 1 行，删除后 0 行。
-- 常见错误：WHERE 只限制项目编号，误删其他参与人员。
-- 验证方法：检查两个键和固定参与数据。

-- ==================================================
-- 练习 8 参考答案
-- ==================================================

SELECT employee_id, employee_name, salary
FROM employees
WHERE employee_id = 7;

START TRANSACTION;
UPDATE employees
SET salary = salary + 500
WHERE employee_id = 7;
SELECT ROW_COUNT() AS affected_rows;
SELECT employee_id, employee_name, salary
FROM employees
WHERE employee_id = 7;
ROLLBACK;

SELECT employee_id, employee_name, salary
FROM employees
WHERE employee_id = 7;

-- 是否报错：危险 SQL 语法通常不报错。
-- 结果是否正确：不正确；它会修改所有员工。
-- 为什么这样修改：预览和 UPDATE 都精确限定员工 7，并在验证后回滚。
-- 预期结果特征：affected_rows 为 1，事务中薪资增加 500，回滚后恢复。
-- 常见错误：认为语句成功就是目标正确。
-- 验证方法：比较事务前、中、后的员工 7 薪资。
