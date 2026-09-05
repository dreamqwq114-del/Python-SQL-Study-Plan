USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'mysql_beginner_practice'
  AND table_name IN
      ('departments', 'employees', 'projects', 'project_metrics', 'employee_projects')
ORDER BY table_name;

SELECT 'departments' AS table_name, COUNT(*) AS row_count FROM departments
UNION ALL
SELECT 'employees', COUNT(*) FROM employees
UNION ALL
SELECT 'projects', COUNT(*) FROM projects
UNION ALL
SELECT 'project_metrics', COUNT(*) FROM project_metrics
UNION ALL
SELECT 'employee_projects', COUNT(*) FROM employee_projects;

SELECT
    SUM(city IS NULL) AS departments_with_null_city
FROM departments;

SELECT
    SUM(end_date IS NULL) AS projects_with_null_end_date,
    SUM(project_manager_id IS NULL) AS projects_without_manager
FROM projects;

SELECT CASE
           WHEN DATABASE() = 'mysql_beginner_practice'
            AND (SELECT COUNT(*) FROM departments) = 5
            AND (SELECT COUNT(*) FROM employees) = 20
            AND (SELECT COUNT(*) FROM projects) = 14
            AND (SELECT COUNT(*) FROM project_metrics) = 12
            AND (SELECT COUNT(*) FROM employee_projects) = 37
            AND (SELECT COUNT(*) FROM departments WHERE city IS NULL) = 1
            AND (SELECT COUNT(*) FROM projects WHERE end_date IS NULL) = 6
            AND (SELECT COUNT(*) FROM projects WHERE project_manager_id IS NULL) = 1
            AND (SELECT COUNT(*) FROM employees AS e
                 WHERE NOT EXISTS
                 (
                     SELECT 1
                     FROM employee_projects AS ep
                     WHERE ep.employee_id = e.employee_id
                 )) = 2
            AND (SELECT COUNT(*) FROM projects AS p
                 WHERE NOT EXISTS
                 (
                     SELECT 1
                     FROM employee_projects AS ep
                     WHERE ep.project_id = p.project_id
                 )) = 2
            AND (SELECT COUNT(*) FROM projects AS p
                 WHERE NOT EXISTS
                 (
                     SELECT 1
                     FROM project_metrics AS pm
                     WHERE pm.project_id = p.project_id
                 )) = 2
           THEN 'PASS'
           ELSE 'FAIL：练习库不是固定基线，请停止并检查'
       END AS baseline_status;
