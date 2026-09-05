/*
用途：创建独立练习数据库、5 张练习表和固定测试数据。
安全边界：只允许创建和使用 sql_beginner_practice。
本脚本不包含 DROP DATABASE、DROP TABLE，也不连接任何业务数据库。
*/

USE master;
GO

IF DB_ID(N'sql_beginner_practice') IS NULL
BEGIN
    CREATE DATABASE sql_beginner_practice;
END;
GO

USE sql_beginner_practice;
GO

IF DB_NAME() <> N'sql_beginner_practice'
BEGIN
    THROW 50001, N'安全检查失败：当前数据库不是 sql_beginner_practice。', 1;
END;
GO

-- 1. 部门表
IF OBJECT_ID(N'dbo.departments', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.departments
    (
        department_id   INT           NOT NULL PRIMARY KEY,
        department_name NVARCHAR(50)  NOT NULL,
        city            NVARCHAR(50)  NULL
    );
END;
GO

-- 2. 员工表：manager_id 自关联 employees.employee_id
IF OBJECT_ID(N'dbo.employees', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.employees
    (
        employee_id   INT            NOT NULL PRIMARY KEY,
        employee_name NVARCHAR(50)   NOT NULL,
        department_id INT            NOT NULL,
        job_title      NVARCHAR(50)   NOT NULL,
        salary         DECIMAL(10, 2) NOT NULL,
        hire_date      DATE           NOT NULL,
        manager_id     INT            NULL,
        CONSTRAINT FK_employees_departments
            FOREIGN KEY (department_id) REFERENCES dbo.departments(department_id),
        CONSTRAINT FK_employees_manager
            FOREIGN KEY (manager_id) REFERENCES dbo.employees(employee_id)
    );
END;
GO

-- 3. 项目表
IF OBJECT_ID(N'dbo.projects', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.projects
    (
        project_id         INT             NOT NULL PRIMARY KEY,
        project_name       NVARCHAR(100)   NOT NULL,
        department_id      INT             NOT NULL,
        project_manager_id INT             NULL,
        project_status     NVARCHAR(20)    NOT NULL,
        budget             DECIMAL(12, 2)  NOT NULL,
        start_date         DATE            NOT NULL,
        end_date           DATE            NULL,
        CONSTRAINT FK_projects_departments
            FOREIGN KEY (department_id) REFERENCES dbo.departments(department_id),
        CONSTRAINT FK_projects_manager
            FOREIGN KEY (project_manager_id) REFERENCES dbo.employees(employee_id)
    );
END;
GO

-- 4. 项目指标表
IF OBJECT_ID(N'dbo.project_metrics', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.project_metrics
    (
        metric_id             INT           NOT NULL PRIMARY KEY,
        project_id            INT           NOT NULL,
        management_fee        DECIMAL(5, 2) NULL,
        investment_return_rate DECIMAL(7, 4) NULL,
        voltage_level         NVARCHAR(20)  NULL,
        CONSTRAINT UQ_project_metrics_project
            UNIQUE (project_id),
        CONSTRAINT FK_project_metrics_projects
            FOREIGN KEY (project_id) REFERENCES dbo.projects(project_id)
    );
END;
GO

-- 5. 员工与项目关系表：联合主键
IF OBJECT_ID(N'dbo.employee_projects', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.employee_projects
    (
        employee_id  INT            NOT NULL,
        project_id   INT            NOT NULL,
        role_name    NVARCHAR(50)   NOT NULL,
        working_hours DECIMAL(8, 2) NOT NULL,
        CONSTRAINT PK_employee_projects
            PRIMARY KEY (employee_id, project_id),
        CONSTRAINT FK_employee_projects_employees
            FOREIGN KEY (employee_id) REFERENCES dbo.employees(employee_id),
        CONSTRAINT FK_employee_projects_projects
            FOREIGN KEY (project_id) REFERENCES dbo.projects(project_id)
    );
END;
GO

-- 固定数据作为一个整体写入：任一批失败时全部回滚，避免留下半套数据。
-- 如果表中已有不完整练习数据，本脚本不会删除它，而会在末尾停止并提醒。
SET XACT_ABORT ON;
BEGIN TRY
    BEGIN TRANSACTION;

-- 固定部门数据：5 个部门，包含重复城市和一个 NULL 城市
IF NOT EXISTS (SELECT 1 FROM dbo.departments)
BEGIN
    INSERT INTO dbo.departments (department_id, department_name, city)
    VALUES
        (1, N'项目管理部', N'上海'),
        (2, N'技术部',     N'苏州'),
        (3, N'财务部',     N'上海'),
        (4, N'市场部',     N'杭州'),
        (5, N'运维部',     NULL);
END;

-- 先插入无上级负责人，再插入直接向他汇报的负责人，避免自关联顺序不清楚
IF NOT EXISTS (SELECT 1 FROM dbo.employees)
BEGIN
    INSERT INTO dbo.employees
        (employee_id, employee_name, department_id, job_title, salary, hire_date, manager_id)
    VALUES
        (1, N'陈晨', 1, N'总监',     22000.00, '2018-03-12', NULL);

    INSERT INTO dbo.employees
        (employee_id, employee_name, department_id, job_title, salary, hire_date, manager_id)
    VALUES
        (2, N'王伟', 2, N'部门经理', 19000.00, '2019-05-20', 1),
        (3, N'李娜', 3, N'部门经理', 18500.00, '2019-08-15', 1),
        (4, N'赵强', 4, N'部门经理', 18000.00, '2020-01-10', 1),
        (5, N'孙悦', 5, N'部门经理', 17500.00, '2020-06-18', 1);

    INSERT INTO dbo.employees
        (employee_id, employee_name, department_id, job_title, salary, hire_date, manager_id)
    VALUES
        (6,  N'周敏', 1, N'项目经理', 15000.00, '2021-02-01', 1),
        (7,  N'吴涛', 1, N'项目专员',  9500.00, '2023-07-10', 6),
        (8,  N'郑洁', 1, N'项目专员',  9800.00, '2022-11-21', 6),
        (9,  N'冯宇', 2, N'工程师',   13500.00, '2021-09-13', 2),
        (10, N'何静', 2, N'工程师',   12800.00, '2022-04-25', 2),
        (11, N'高峰', 2, N'测试工程师',11500.00, '2023-01-16', 2),
        (12, N'林雪', 2, N'工程师',   13000.00, '2020-12-07', 2),
        (13, N'罗翔', 3, N'会计',     10500.00, '2021-03-22', 3),
        (14, N'梁婷', 3, N'财务分析师',12500.00, '2022-08-08', 3),
        (15, N'宋阳', 4, N'市场专员',  9200.00, '2023-05-04', 4),
        (16, N'唐莉', 4, N'市场专员',  9000.00, '2024-02-19', 4),
        (17, N'许凯', 5, N'运维工程师',11000.00, '2021-11-11', 5),
        (18, N'韩梅', 5, N'运维工程师',10800.00, '2022-12-12', 5),
        (19, N'曹磊', 5, N'助理',      7200.00, '2024-06-03', 5),
        (20, N'邓芳', 3, N'实习生',    5000.00, '2025-01-06', 3);
END;

-- 14 个项目；项目 14 没有项目经理；项目 13、14 没有员工参与
IF NOT EXISTS (SELECT 1 FROM dbo.projects)
BEGIN
    INSERT INTO dbo.projects
        (project_id, project_name, department_id, project_manager_id, project_status, budget, start_date, end_date)
    VALUES
        (1,  N'智慧园区一期',   2, 2,    N'进行中', 1200000.00, '2024-01-15', '2026-06-30'),
        (2,  N'成本控制平台',   3, 3,    N'已完成',  650000.00, '2022-03-01', '2023-12-31'),
        (3,  N'客户数据整合',   4, 4,    N'进行中',  820000.00, '2024-05-20', '2026-03-31'),
        (4,  N'设备巡检升级',   5, 5,    N'暂停',    480000.00, '2023-09-01', NULL),
        (5,  N'项目看板改造',   1, 6,    N'已完成',  300000.00, '2023-02-10', '2023-10-20'),
        (6,  N'移动审批系统',   2, 2,    N'进行中',  900000.00, '2024-07-01', '2026-08-31'),
        (7,  N'预算预测模型',   3, 3,    N'待启动',  550000.00, '2026-03-01', NULL),
        (8,  N'市场活动分析',   4, 4,    N'已完成',  260000.00, '2022-06-15', '2022-12-15'),
        (9,  N'机房节能改造',   5, 5,    N'进行中',  760000.00, '2024-02-01', '2025-11-30'),
        (10, N'供应商评估',     1, 6,    N'暂停',    350000.00, '2024-08-12', NULL),
        (11, N'数据质量治理',   2, 2,    N'待启动', 1100000.00, '2026-04-01', NULL),
        (12, N'财务共享试点',   3, 3,    N'进行中',  680000.00, '2024-10-10', '2026-12-31'),
        (13, N'品牌焕新计划',   4, 4,    N'待启动',  420000.00, '2026-05-01', NULL),
        (14, N'备用机房规划',   5, NULL, N'待启动',  510000.00, '2026-06-01', NULL);
END;

-- 12 条指标；项目 13、14 没有指标；记录 11、12 含 NULL
IF NOT EXISTS (SELECT 1 FROM dbo.project_metrics)
BEGIN
    INSERT INTO dbo.project_metrics
        (metric_id, project_id, management_fee, investment_return_rate, voltage_level)
    VALUES
        (1,  1,  0.20, 0.0815, N'10kV'),
        (2,  2,  0.15, 0.0900, N'380V'),
        (3,  3,  0.25, 0.0708, N'低压'),
        (4,  4,  0.10, 0.0600, N'35kV'),
        (5,  5,  0.15, 0.0750, N'380V'),
        (6,  6,  0.20, 0.0850, N'110kV'),
        (7,  7,  0.10, 0.0650, N'10kV'),
        (8,  8,  0.25, 0.0950, N'低压'),
        (9,  9,  0.20, 0.0820, N'35kV'),
        (10, 10, 0.15, 0.0700, N'380V'),
        (11, 11, NULL, 0.0880, N'110kV'),
        (12, 12, 0.20, NULL,   NULL);
END;

-- 37 条员工项目关系；员工 19、20 未参与项目；项目 1 有 6 名员工
IF NOT EXISTS (SELECT 1 FROM dbo.employee_projects)
BEGIN
    INSERT INTO dbo.employee_projects
        (employee_id, project_id, role_name, working_hours)
    VALUES
        (2, 1, N'项目经理', 160), (6, 1, N'协调', 90), (9, 1, N'开发', 180),
        (10, 1, N'开发', 170), (11, 1, N'测试', 120), (17, 1, N'运维', 80),
        (1, 2, N'监督', 20), (3, 2, N'项目经理', 110), (13, 2, N'会计', 130),
        (14, 2, N'分析', 150),
        (4, 3, N'项目经理', 120), (15, 3, N'调研', 100), (16, 3, N'调研', 95),
        (9, 3, N'开发', 140), (5, 4, N'项目经理', 90), (17, 4, N'运维', 160),
        (18, 4, N'运维', 150), (6, 5, N'项目经理', 100), (7, 5, N'协调', 80),
        (8, 5, N'记录', 75), (2, 6, N'项目经理', 100), (10, 6, N'开发', 180),
        (11, 6, N'测试', 150), (12, 6, N'开发', 170), (3, 7, N'项目经理', 40),
        (14, 7, N'分析', 60), (4, 8, N'项目经理', 90), (15, 8, N'市场', 140),
        (16, 8, N'市场', 130), (5, 9, N'项目经理', 100), (17, 9, N'运维', 180),
        (18, 9, N'运维', 175), (6, 10, N'项目经理', 70), (7, 10, N'协调', 85),
        (2, 11, N'项目经理', 55), (12, 11, N'开发', 65), (3, 12, N'项目经理', 80);
END;

    -- 固定基线断言：不满足时回滚本次写入并停止，不自动删除学习者数据。
    IF (SELECT COUNT(*) FROM dbo.departments) <> 5
       OR (SELECT COUNT(*) FROM dbo.employees) <> 20
       OR (SELECT COUNT(*) FROM dbo.projects) <> 14
       OR (SELECT COUNT(*) FROM dbo.project_metrics) <> 12
       OR (SELECT COUNT(*) FROM dbo.employee_projects) <> 37
       OR (SELECT COUNT(*) FROM dbo.employees AS e
           WHERE NOT EXISTS
           (
               SELECT 1 FROM dbo.employee_projects AS ep
               WHERE ep.employee_id = e.employee_id
           )) <> 2
       OR (SELECT COUNT(*) FROM dbo.projects AS p
           WHERE NOT EXISTS
           (
               SELECT 1 FROM dbo.employee_projects AS ep
               WHERE ep.project_id = p.project_id
           )) <> 2
       OR (SELECT COUNT(*) FROM dbo.projects AS p
           WHERE NOT EXISTS
           (
               SELECT 1 FROM dbo.project_metrics AS pm
               WHERE pm.project_id = p.project_id
           )) <> 2
    BEGIN
        THROW 50002, N'练习数据不是固定基线。为保护已有数据，脚本未自动删除或重置，请只在全新的 sql_beginner_practice 中初始化。', 1;
    END;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    THROW;
END CATCH;
GO

-- 初始化核对：应为 5、20、14、12、37
SELECT N'departments' AS table_name, COUNT(*) AS row_count FROM dbo.departments
UNION ALL
SELECT N'employees', COUNT(*) FROM dbo.employees
UNION ALL
SELECT N'projects', COUNT(*) FROM dbo.projects
UNION ALL
SELECT N'project_metrics', COUNT(*) FROM dbo.project_metrics
UNION ALL
SELECT N'employee_projects', COUNT(*) FROM dbo.employee_projects;

-- 关键练习数据核对
SELECT COUNT(*) AS employees_without_projects
FROM dbo.employees AS e
LEFT JOIN dbo.employee_projects AS ep ON ep.employee_id = e.employee_id
WHERE ep.employee_id IS NULL;

SELECT COUNT(*) AS projects_without_employees
FROM dbo.projects AS p
LEFT JOIN dbo.employee_projects AS ep ON ep.project_id = p.project_id
WHERE ep.project_id IS NULL;

SELECT COUNT(*) AS projects_without_metrics
FROM dbo.projects AS p
LEFT JOIN dbo.project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.project_id IS NULL;
