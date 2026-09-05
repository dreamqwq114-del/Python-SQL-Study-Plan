USE sql_beginner_practice;
GO
IF DB_NAME() <> N'sql_beginner_practice' THROW 50001, N'当前数据库错误。', 1;
GO

-- 题 1：LEFT JOIN 后检查右表主键 NULL；每个未参与员工一行。
SELECT e.employee_id, e.employee_name
FROM dbo.employees AS e
LEFT JOIN dbo.employee_projects AS ep ON ep.employee_id = e.employee_id
WHERE ep.employee_id IS NULL;

-- 题 2：LEFT JOIN 保留无经理项目；经理为空时姓名为 NULL。
SELECT p.project_name, e.employee_name AS manager_name
FROM dbo.projects AS p
LEFT JOIN dbo.employees AS e ON e.employee_id = p.project_manager_id;

-- 题 3：<> 表示不等于；job_title 非 NULL，因此不会漏掉未知值。
SELECT employee_name, job_title
FROM dbo.employees
WHERE job_title <> N'工程师';

-- 题 4：CASE 从上到下判断；无 JOIN，budget 非 NULL。
SELECT project_name, budget,
       CASE WHEN budget >= 800000 THEN N'高预算' ELSE N'普通预算' END AS budget_level
FROM dbo.projects;

-- 题 5：标量子查询只返回一个平均值；无 JOIN，AVG 忽略 NULL。
SELECT project_name, budget
FROM dbo.projects
WHERE budget > (SELECT AVG(budget) FROM dbo.projects);

-- 题 6：IN 接受子查询多值；DISTINCT 防止同一经理因多个项目重复。
-- NULL project_manager_id 不会匹配员工主键。
SELECT DISTINCT e.employee_id, e.employee_name
FROM dbo.employees AS e
WHERE e.employee_id IN
(
    SELECT p.project_manager_id
    FROM dbo.projects AS p
    WHERE p.project_status = N'进行中'
);

-- 题 7：CASE 明确处理 NULL；无 JOIN。
SELECT employee_name,
       CASE WHEN manager_id IS NULL THEN 0 ELSE manager_id END AS manager_display
FROM dbo.employees;

-- 题 8：标量子查询只返回公司平均工资，再同时筛选职位。
-- 无 JOIN，不产生重复；salary 与 job_title 均非 NULL。
SELECT employee_name, job_title, salary
FROM dbo.employees
WHERE salary >
(
    SELECT AVG(salary)
    FROM dbo.employees
)
AND job_title = N'工程师';

-- 题 9：错误原因是 = 右侧标量子查询返回多个部门编号。
-- IN 可接受多个上海部门编号；无 JOIN。
SELECT employee_name
FROM dbo.employees
WHERE department_id IN
(
    SELECT department_id
    FROM dbo.departments
    WHERE city = N'上海'
);

-- 题 10：CASE 先判断更高门槛，否则高薪会提前命中“中”。
SELECT employee_name, salary,
       CASE
           WHEN salary >= 15000 THEN N'高'
           WHEN salary >= 10000 THEN N'中'
           ELSE N'基础'
       END AS salary_level
FROM dbo.employees;
