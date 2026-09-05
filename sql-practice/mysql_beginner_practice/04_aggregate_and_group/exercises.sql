USE mysql_beginner_practice;

SELECT DATABASE() AS current_database;

-- ==================================================
-- 练习 1：统计员工总数
-- ==================================================
-- 难度：模仿
-- 目标：
-- 统计 employees 的总行数，结果列标题为 employee_count。
-- 应返回：
-- 1 行 1 列；统计所有员工。
-- 使用知识：
-- COUNT(*)
-- 验证方式：
-- 与员工明细行数比较。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select
    count(*) as employee_count
from employees


-- ==================================================
-- 练习 2：汇总项目预算
-- ==================================================
-- 难度：模仿
-- 目标：
-- 查询项目预算的总和与平均值，列标题为 total_budget、average_budget。
-- 应返回：
-- 1 行 2 列。
-- 使用知识：
-- SUM、AVG
-- 验证方式：
-- 平均值应在最小预算和最大预算之间。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select
    AVG(budget) as average_budget ,
    SUM(budget) as total_budget
from projects;



-- ==================================================
-- 练习 3：统计各项目状态数量
-- ==================================================
-- 难度：基础变形
-- 目标：
-- 按 project_status 分组统计项目数，列标题为 project_count。
-- 按项目数降序，数量相同时按状态升序。
-- 应返回：
-- 每种状态一行，共 2 列。
-- 使用知识：
-- GROUP BY、COUNT、ORDER BY
-- 验证方式：
-- 各组计数之和应等于项目总数。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select
    project_status,
    count(*) as project_count
from projects
group by project_status






-- ==================================================
-- 练习 4：统计各部门薪资范围
-- ==================================================
-- 难度：基础变形
-- 目标：
-- 按 department_id 分组，显示最低薪资和最高薪资，
-- 列标题为 minimum_salary、maximum_salary；按部门编号升序。
-- 应返回：
-- 每个已有员工的部门一行，共 3 列。
-- 使用知识：
-- GROUP BY、MIN、MAX
-- 验证方式：
-- 每组最小值不应大于最大值。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select
    department_id ,
    max(salary) as minimu_salary ,
    min(salary) as maximum_salary
from employees
order by  department_id asc




-- ==================================================
-- 练习 5：汇总进行中项目预算
-- ==================================================
-- 难度：基础变形
-- 目标：
-- 只对“进行中”项目按 department_id 分组，
-- 显示项目数和预算总和，列标题为 project_count、total_budget；
-- 按部门编号升序。
-- 应返回：
-- 每个有进行中项目的部门一行，共 3 列。
-- 使用知识：
-- WHERE、GROUP BY、COUNT、SUM
-- 验证方式：
-- 计数之和等于进行中项目数，总预算不含其他状态。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select
    count(department_id) as project_count ,
    sum(budget) as total_budget
from projects
where project_status = '进行中'
group by department_id
order by projects.department_id asc ;




-- ==================================================
-- 练习 6：查找平均薪资较高的职位
-- ==================================================
-- 难度：独立
-- 目标：
-- 按 job_title 分组，保留平均薪资至少 12000 的职位。
-- 显示职位、人数、平均薪资，列标题为 employee_count、average_salary。
-- 按平均薪资降序，平均值相同时按职位升序。
-- 应返回：
-- 每个满足条件的职位一行，共 3 列。
-- 使用知识：
-- GROUP BY、AVG、COUNT、HAVING
-- 验证方式：
-- 检查每组平均薪资下限和排序。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select
       job_title ,
       count(employee_id) as employee_count ,
       avg(salary) as average_salary
from employees
group by job_title having avg(salary) >= 12000
order by average_salary desc , job_title asc ;



-- ==================================================
-- 练习 7：核对指标空值数量
-- ==================================================
-- 难度：独立
-- 目标：
-- 用一条查询同时显示 project_metrics 总行数、
-- management_fee 非空数量、investment_return_rate 非空数量、
-- voltage_level 非空数量。
-- 列标题依次为 metric_count、fee_count、return_count、voltage_count。
-- 应返回：
-- 1 行 4 列；各非空计数不大于总行数。
-- 使用知识：
-- COUNT(*)、COUNT(column)、NULL
-- 验证方式：
-- 比较四个计数，并用空值含义解释差值。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写 SQL：
select



-- ==================================================
-- 练习 8：改正分组后人数筛选
-- ==================================================
-- 难度：改错
-- 目标：
-- 原意是按部门统计人数，只保留至少 4 名员工的部门。
-- 错误 SQL（会报错）：
-- SELECT department_id, COUNT(*) AS employee_count
-- FROM employees
-- WHERE COUNT(*) >= 4
-- GROUP BY department_id;
-- 请回答：
-- 1. 原 SQL 是否报错？
-- 2. 为什么聚合条件不能放在这里？
-- 3. 应如何修改？为什么？
-- 4. 修改后结果应有什么特征？
-- 应返回：
-- 每个符合条件的部门一行，employee_count 至少为 4。
-- 使用知识：
-- GROUP BY、WHERE 与 HAVING
-- 验证方式：
-- 检查每组计数，并确认没有人数不足的部门。
-- 提示：
-- 卡住后打开本章 hints.md；不要提前打开 answers.sql。
-- 在下方填写修改后的 SQL 和解释：



-- 本章结束自检：
-- [ ] 我先完成了 lesson.md 中的所有示例
-- [ ] 我没有看答案完成至少 6 道题
-- [ ] 我能解释每条 SQL 的作用
-- [ ] 我检查了返回列数
-- [ ] 我检查了返回行数
-- [ ] 我检查了 NULL 和重复
-- [ ] 我把真正做错的题记录进 mistake_log.md
