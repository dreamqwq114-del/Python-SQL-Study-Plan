# Python–SQL 桥接输入契约

SQL 端完成 `mysql_beginner_practice/12_python_sql_bridge/assessment.sql` 后，把查询结果从 IDE 导出为 CSV，再用 Python 分析。不要在 SQL 服务器上使用 `INTO OUTFILE`，以免把服务器文件权限问题混入学习目标。

Python 端的 CSV 至少应包含：

`project_id`, `project_name`, `department_name`, `project_status`, `budget`, `participant_count`, `total_working_hours`

导入后必须完成以下检查：

1. `project_id` 应唯一，并说明行数是否等于基线项目数 14；
2. `participant_count` 和 `total_working_hours` 应为数值，不能把无参与项目误删；
3. 按 `project_status` 汇总项目数和预算，比较 SQL 结果与 Python 结果；
4. 报告预算最高项目、无参与人员项目，以及每个状态的项目数；
5. 如果 SQL 导出与 Python 汇总不一致，先定位粒度、连接方向或重复问题，不要直接删除重复行。

建议提交物：SQL 作答文件、导出的 CSV、Python 分析脚本、两端的行数/金额核对记录。

