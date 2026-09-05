/*
用途：在 XAMPP 的 MariaDB/MySQL 中创建独立练习数据库、5 张表和固定数据。
安全边界：只创建和使用 sql_beginner_practice。
本脚本不包含 DROP DATABASE 或 DROP TABLE，不操作其他数据库。
实际验证环境：MariaDB 10.4.32（XAMPP）。
*/

CREATE DATABASE IF NOT EXISTS sql_beginner_practice
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sql_beginner_practice;
SELECT DATABASE() AS current_database;

CREATE TABLE IF NOT EXISTS departments
(
    department_id   INT          NOT NULL,
    department_name VARCHAR(50)  NOT NULL,
    city            VARCHAR(50)  NULL,
    PRIMARY KEY (department_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS employees
(
    employee_id   INT           NOT NULL,
    employee_name VARCHAR(50)   NOT NULL,
    department_id INT           NOT NULL,
    job_title     VARCHAR(50)   NOT NULL,
    salary        DECIMAL(10,2) NOT NULL,
    hire_date     DATE          NOT NULL,
    manager_id    INT           NULL,
    PRIMARY KEY (employee_id),
    CONSTRAINT FK_employees_departments
        FOREIGN KEY (department_id) REFERENCES departments(department_id),
    CONSTRAINT FK_employees_manager
        FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS projects
(
    project_id         INT           NOT NULL,
    project_name       VARCHAR(100)  NOT NULL,
    department_id      INT           NOT NULL,
    project_manager_id INT           NULL,
    project_status     VARCHAR(20)   NOT NULL,
    budget             DECIMAL(12,2) NOT NULL,
    start_date         DATE          NOT NULL,
    end_date           DATE          NULL,
    PRIMARY KEY (project_id),
    CONSTRAINT FK_projects_departments
        FOREIGN KEY (department_id) REFERENCES departments(department_id),
    CONSTRAINT FK_projects_manager
        FOREIGN KEY (project_manager_id) REFERENCES employees(employee_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS project_metrics
(
    metric_id              INT          NOT NULL,
    project_id             INT          NOT NULL,
    management_fee         DECIMAL(5,2) NULL,
    investment_return_rate DECIMAL(7,4) NULL,
    voltage_level          VARCHAR(20)  NULL,
    PRIMARY KEY (metric_id),
    CONSTRAINT UQ_project_metrics_project UNIQUE (project_id),
    CONSTRAINT FK_project_metrics_projects
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS employee_projects
(
    employee_id  INT           NOT NULL,
    project_id   INT           NOT NULL,
    role_name    VARCHAR(50)   NOT NULL,
    working_hours DECIMAL(8,2) NOT NULL,
    PRIMARY KEY (employee_id, project_id),
    CONSTRAINT FK_employee_projects_employees
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    CONSTRAINT FK_employee_projects_projects
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 固定数据使用同一事务写入。
-- 重复运行会更新相同主键/唯一键，但不会删除额外练习行，不是“自动重置”。
-- 只有脚本末尾 baseline_status 显示 PASS 时，才可以继续课程。
START TRANSACTION;

INSERT INTO departments (department_id, department_name, city)
VALUES
    (1, '项目管理部', '上海'),
    (2, '技术部',     '苏州'),
    (3, '财务部',     '上海'),
    (4, '市场部',     '杭州'),
    (5, '运维部',     NULL)
ON DUPLICATE KEY UPDATE
    department_name = VALUES(department_name),
    city = VALUES(city);

-- 先写入无上级员工，满足自关联外键。
INSERT INTO employees
    (employee_id, employee_name, department_id, job_title, salary, hire_date, manager_id)
VALUES
    (1, '陈晨', 1, '总监', 22000.00, '2018-03-12', NULL)
ON DUPLICATE KEY UPDATE
    employee_name = VALUES(employee_name),
    department_id = VALUES(department_id),
    job_title = VALUES(job_title),
    salary = VALUES(salary),
    hire_date = VALUES(hire_date),
    manager_id = VALUES(manager_id);

INSERT INTO employees
    (employee_id, employee_name, department_id, job_title, salary, hire_date, manager_id)
VALUES
    (2,  '王伟', 2, '部门经理', 19000.00, '2019-05-20', 1),
    (3,  '李娜', 3, '部门经理', 18500.00, '2019-08-15', 1),
    (4,  '赵强', 4, '部门经理', 18000.00, '2020-01-10', 1),
    (5,  '孙悦', 5, '部门经理', 17500.00, '2020-06-18', 1),
    (6,  '周敏', 1, '项目经理', 15000.00, '2021-02-01', 1),
    (7,  '吴涛', 1, '项目专员',  9500.00, '2023-07-10', 6),
    (8,  '郑洁', 1, '项目专员',  9800.00, '2022-11-21', 6),
    (9,  '冯宇', 2, '工程师',   13500.00, '2021-09-13', 2),
    (10, '何静', 2, '工程师',   12800.00, '2022-04-25', 2),
    (11, '高峰', 2, '测试工程师',11500.00, '2023-01-16', 2),
    (12, '林雪', 2, '工程师',   13000.00, '2020-12-07', 2),
    (13, '罗翔', 3, '会计',     10500.00, '2021-03-22', 3),
    (14, '梁婷', 3, '财务分析师',12500.00, '2022-08-08', 3),
    (15, '宋阳', 4, '市场专员',  9200.00, '2023-05-04', 4),
    (16, '唐莉', 4, '市场专员',  9000.00, '2024-02-19', 4),
    (17, '许凯', 5, '运维工程师',11000.00, '2021-11-11', 5),
    (18, '韩梅', 5, '运维工程师',10800.00, '2022-12-12', 5),
    (19, '曹磊', 5, '助理',      7200.00, '2024-06-03', 5),
    (20, '邓芳', 3, '实习生',    5000.00, '2025-01-06', 3)
ON DUPLICATE KEY UPDATE
    employee_name = VALUES(employee_name),
    department_id = VALUES(department_id),
    job_title = VALUES(job_title),
    salary = VALUES(salary),
    hire_date = VALUES(hire_date),
    manager_id = VALUES(manager_id);

INSERT INTO projects
    (project_id, project_name, department_id, project_manager_id,
     project_status, budget, start_date, end_date)
VALUES
    (1,  '智慧园区一期', 2, 2,    '进行中', 1200000.00, '2024-01-15', '2026-06-30'),
    (2,  '成本控制平台', 3, 3,    '已完成',  650000.00, '2022-03-01', '2023-12-31'),
    (3,  '客户数据整合', 4, 4,    '进行中',  820000.00, '2024-05-20', '2026-03-31'),
    (4,  '设备巡检升级', 5, 5,    '暂停',    480000.00, '2023-09-01', NULL),
    (5,  '项目看板改造', 1, 6,    '已完成',  300000.00, '2023-02-10', '2023-10-20'),
    (6,  '移动审批系统', 2, 2,    '进行中',  900000.00, '2024-07-01', '2026-08-31'),
    (7,  '预算预测模型', 3, 3,    '待启动',  550000.00, '2026-03-01', NULL),
    (8,  '市场活动分析', 4, 4,    '已完成',  260000.00, '2022-06-15', '2022-12-15'),
    (9,  '机房节能改造', 5, 5,    '进行中',  760000.00, '2024-02-01', '2025-11-30'),
    (10, '供应商评估',   1, 6,    '暂停',    350000.00, '2024-08-12', NULL),
    (11, '数据质量治理', 2, 2,    '待启动', 1100000.00, '2026-04-01', NULL),
    (12, '财务共享试点', 3, 3,    '进行中',  680000.00, '2024-10-10', '2026-12-31'),
    (13, '品牌焕新计划', 4, 4,    '待启动',  420000.00, '2026-05-01', NULL),
    (14, '备用机房规划', 5, NULL, '待启动',  510000.00, '2026-06-01', NULL)
ON DUPLICATE KEY UPDATE
    project_name = VALUES(project_name),
    department_id = VALUES(department_id),
    project_manager_id = VALUES(project_manager_id),
    project_status = VALUES(project_status),
    budget = VALUES(budget),
    start_date = VALUES(start_date),
    end_date = VALUES(end_date);

INSERT INTO project_metrics
    (metric_id, project_id, management_fee, investment_return_rate, voltage_level)
VALUES
    (1,  1,  0.20, 0.0815, '10kV'),
    (2,  2,  0.15, 0.0900, '380V'),
    (3,  3,  0.25, 0.0708, '低压'),
    (4,  4,  0.10, 0.0600, '35kV'),
    (5,  5,  0.15, 0.0750, '380V'),
    (6,  6,  0.20, 0.0850, '110kV'),
    (7,  7,  0.10, 0.0650, '10kV'),
    (8,  8,  0.25, 0.0950, '低压'),
    (9,  9,  0.20, 0.0820, '35kV'),
    (10, 10, 0.15, 0.0700, '380V'),
    (11, 11, NULL, 0.0880, '110kV'),
    (12, 12, 0.20, NULL,   NULL)
ON DUPLICATE KEY UPDATE
    project_id = VALUES(project_id),
    management_fee = VALUES(management_fee),
    investment_return_rate = VALUES(investment_return_rate),
    voltage_level = VALUES(voltage_level);

INSERT INTO employee_projects
    (employee_id, project_id, role_name, working_hours)
VALUES
    (2, 1, '项目经理', 160), (6, 1, '协调', 90), (9, 1, '开发', 180),
    (10, 1, '开发', 170), (11, 1, '测试', 120), (17, 1, '运维', 80),
    (1, 2, '监督', 20), (3, 2, '项目经理', 110), (13, 2, '会计', 130),
    (14, 2, '分析', 150),
    (4, 3, '项目经理', 120), (15, 3, '调研', 100), (16, 3, '调研', 95),
    (9, 3, '开发', 140), (5, 4, '项目经理', 90), (17, 4, '运维', 160),
    (18, 4, '运维', 150), (6, 5, '项目经理', 100), (7, 5, '协调', 80),
    (8, 5, '记录', 75), (2, 6, '项目经理', 100), (10, 6, '开发', 180),
    (11, 6, '测试', 150), (12, 6, '开发', 170), (3, 7, '项目经理', 40),
    (14, 7, '分析', 60), (4, 8, '项目经理', 90), (15, 8, '市场', 140),
    (16, 8, '市场', 130), (5, 9, '项目经理', 100), (17, 9, '运维', 180),
    (18, 9, '运维', 175), (6, 10, '项目经理', 70), (7, 10, '协调', 85),
    (2, 11, '项目经理', 55), (12, 11, '开发', 65), (3, 12, '项目经理', 80)
ON DUPLICATE KEY UPDATE
    role_name = VALUES(role_name),
    working_hours = VALUES(working_hours);

COMMIT;

-- 总基线检查：必须显示 PASS。FAIL 时请停止，不要继续做题。
SELECT CASE
           WHEN (SELECT COUNT(*) FROM departments) = 5
            AND (SELECT COUNT(*) FROM employees) = 20
            AND (SELECT COUNT(*) FROM projects) = 14
            AND (SELECT COUNT(*) FROM project_metrics) = 12
            AND (SELECT COUNT(*) FROM employee_projects) = 37
            AND (SELECT COUNT(*) FROM project_metrics
                 WHERE metric_id = project_id) = 12
            AND (SELECT COUNT(*) FROM employees AS e
                 WHERE NOT EXISTS
                 (
                     SELECT 1 FROM employee_projects AS ep
                     WHERE ep.employee_id = e.employee_id
                 )) = 2
            AND (SELECT COUNT(*) FROM projects AS p
                 WHERE NOT EXISTS
                 (
                     SELECT 1 FROM employee_projects AS ep
                     WHERE ep.project_id = p.project_id
                 )) = 2
            AND (SELECT COUNT(*) FROM projects AS p
                 WHERE NOT EXISTS
                 (
                     SELECT 1 FROM project_metrics AS pm
                     WHERE pm.project_id = p.project_id
                 )) = 2
           THEN 'PASS'
           ELSE 'FAIL：练习库不是固定基线，请停止并检查，不要直接继续课程'
       END AS baseline_status;

-- 明细核对：依次应为 5、20、14、12、37。
SELECT 'departments' AS table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'employees', COUNT(*) FROM employees
UNION ALL
SELECT 'projects', COUNT(*) FROM projects
UNION ALL
SELECT 'project_metrics', COUNT(*) FROM project_metrics
UNION ALL
SELECT 'employee_projects', COUNT(*) FROM employee_projects;

SELECT COUNT(*) AS employees_without_projects
FROM employees AS e
LEFT JOIN employee_projects AS ep ON ep.employee_id = e.employee_id
WHERE ep.employee_id IS NULL;

SELECT COUNT(*) AS projects_without_employees
FROM projects AS p
LEFT JOIN employee_projects AS ep ON ep.project_id = p.project_id
WHERE ep.project_id IS NULL;

SELECT COUNT(*) AS projects_without_metrics
FROM projects AS p
LEFT JOIN project_metrics AS pm ON pm.project_id = p.project_id
WHERE pm.project_id IS NULL;
